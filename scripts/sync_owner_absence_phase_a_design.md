# Phase A automation — paper design

Version: 2026-04-30 v1
Status: handoff v3 §7 WB5 step 1 deliverable. Paper-only spec; no production wiring yet.
Audience: Codex (proposer), Claude Code (γ-gate-recommended reviewer), 강은구 (approver).

This document is the design artifact for the WB5 first step ("Codex drafts workflow on paper first; 강은구 reviews"). It is not a new policy; it operationalizes already-decided policy:

- Owner-absence canonical destinations (`AX_OWNER_ABSENCE_LOG_DESTINATION_POLICY` v3): Notion + Git as two replicated canonicals; Slack + Telegram as alert mirrors.
- KPI K3: a test declaration must propagate to all three mirrors within the policy sync window.
- Existing artifact: `scripts/sync_owner_absence_phase_a.py` already validates records and fans out, but is not yet driven by a Notion trigger.

## 1. Goal

Replace the current manual dual-canonical entry with an automated Notion → Git, Slack, Telegram propagation that satisfies the policy sync window on every real declaration.

## 2. Topology

```
Notion DB row (canonical)
    │  (create or update event)
    │
    ▼
 Notion webhook ─────────────► n8n (vmi3124683:5678, openclaw user, since Apr22)
                                │
                                │  (1) normalize Notion page → record JSON v1.0
                                │  (2) call sync_owner_absence_phase_a.py --record-stdin
                                │
                                ▼
                       sync_owner_absence_phase_a.py
                                │
                ┌──────────────┴───────────────┐
                │                              │
                ▼                              ▼
   Git canonical (append-only         Slack alert mirror
   audit/owner_absence.jsonl,         (#000-대표-똘똘이,
   pushed via App identity            via Owner-Absence webhook
   on the ax-audit repo)              env: OWNER_ABSENCE_SLACK_WEBHOOK_URL)
                │
                ▼
   Telegram alert mirror
   (group `ABEL` -1003286171878,
   via @SN_ocle_bot, env:
   OWNER_ABSENCE_TELEGRAM_BOT_TOKEN +
   OWNER_ABSENCE_TELEGRAM_CHAT_ID)
```

## 3. Trigger contract

Notion DB id: `421644f9-3db4-4f18-b50e-b6e35c019f25` (`AX 소유자 부재 신고`).

The webhook fires on:
- new page (declaration draft created)
- page property update (any of the v1.0 schema fields, especially `ratification_status` or `sync_state`)

The webhook payload is normalized by n8n into a record matching `audit/owner_absence.schema.json`. Field mapping is listed in §4 below.

## 4. Field mapping (Notion property → record key)

The Notion DB carries the v1.0 schema verbatim, so the mapping is identity for most fields. The bridge only:
- coerces Notion's `select` / `multi_select` / `rich_text` into plain strings;
- converts `date` properties to ISO-8601 with `+09:00` offset (KST);
- fills `linked_actions` from the relation property as an array of declaration IDs (empty array if none);
- always sets `canonical_source` = `"notion"`;
- preserves `created_at` if present, otherwise initializes to the page `created_time`;
- updates `last_updated_at` to the webhook event time.

If the bridge fails to map any required field, it MUST stop and emit a schema-failure alert (see §6) — never write a partial record.

## 5. n8n workflow shape (sandbox-first)

n8n project name: `ax-phase-a-sandbox` (purged before production promotion).

Nodes, in order:

1. **Webhook** — POST endpoint that receives Notion event. Path: `/owner-absence-sandbox` (will become `/owner-absence` after promote).
2. **Function: normalize** — JS that produces the v1.0 record JSON per §4.
3. **HTTP Request: schema validate** — local call to `python3 scripts/validate_owner_absence.py --schema-file ... --record-stdin` (or run script via Execute Command node). Stops on non-zero exit.
4. **Execute Command: append + fanout** — `OWNER_ABSENCE_SLACK_WEBHOOK_URL=... OWNER_ABSENCE_TELEGRAM_BOT_TOKEN=... OWNER_ABSENCE_TELEGRAM_CHAT_ID=... python3 scripts/sync_owner_absence_phase_a.py --record-stdin --apply`.
5. **Git push** (separate node or inside step 4): the script appends to `audit/owner_absence.jsonl`; n8n then pushes the change as `hakham-dex[bot]` (using a short-lived installation token issued via the App). On a push, branch protection still requires a PR review, so the push goes to a dedicated branch `phase-a-sync/<declaration-id>` and a PR is auto-opened with body = the appended record. **Approval and merge remain human-gated** even for automated propagation, per Decision 15.
6. **Error path** — on any node failure, send a structured alert to Slack (#000-대표-똘똘이) and Telegram (group ABEL) using the same fanout helpers, but with body `phase-a-sync-failed`. Webhook returns 5xx so Notion can retry per its retry policy.

## 6. Sandbox plan

1. Build the workflow under the n8n `ax-phase-a-sandbox` project.
2. Use a fabricated record set with declaration IDs `OA-SANDBOX-001..010`. Mark them clearly as test data; never push to the production Git canonical or the production Slack/Telegram channels.
3. Sandbox endpoints during dry-run:
   - Slack: a private test channel (Owner-only).
   - Telegram: a private test chat with @SN_ocle_bot.
   - Git: a fork branch on `ax-audit` named `sandbox/owner-absence` that is NEVER merged.
4. Run a full sequence: create a Notion sandbox row → expect record propagated to all three test endpoints within the sync window → mark `ratified` in Notion → expect a second record append (status update) and another fanout.
5. Purge sandbox records before promote: delete fork branch, delete sandbox Notion rows, archive sandbox Slack/Telegram messages, drop the n8n project after production promote works.

## 7. Promote_automation gate

Promote is a non-γ `promote_automation` action under PHASE0 §15.3:
- Codex (or this design's primary AI) opens the promote PR.
- A distinct Claude Code reviewer session reviews the workflow export and the secret-handling for policy conformance.
- 강은구 approves.
- Codex/AI flips the n8n workflow from sandbox to production (rename project to `ax-phase-a-prod`, point Notion webhook to the production endpoint, swap secret env values).
- The first real production declaration must propagate to all three mirrors within the sync window — this is the K3 KPI proof.

## 8. Out of scope (explicit)

- Phase B (two-way sync with conflict detection) — separate cycle.
- SOPS+age secret backend migration — referenced from PHASE0 §9, separate work.
- Token rotation — Owner-deferred 2026-04-26.
- Schema changes — γ gate; not part of Phase A.
- Multi-tenant fanout — current design serves a single tenant (강은구).

## 9. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Notion webhook misses an event | Notion's retry policy + n8n idempotency on `(declaration_id, last_updated_at)` |
| n8n down | Cron fallback that polls Notion every 5 minutes for unsynced rows; runs only if the webhook path has no traffic in the last sync window |
| Git push hits protected `main` directly | Push to feature branch + auto-open PR; never bypass protection |
| Slack/Telegram credential leak | Secrets remain in n8n credential store + host env; never committed; key custody migrates to SOPS+age in a later cycle |
| Schema drift between Notion and `owner_absence.schema.json` | Validate every record against the schema before append; fail closed |
| First production declaration fails K3 | Sandbox dry-run must succeed twice in a row before promote |

## 10. Open items for next PR

- Capture concrete Slack webhook URL and Telegram chat ID for the AX path (Owner provides during promote, not in this PR).
- Decide whether the auto-opened PR per declaration is squash-merged automatically after Owner approval or batched daily.
- Confirm n8n credential isolation (do not reuse the Codex OAuth env values).

## 11. Cross-references

- handoff v3 §7 WB5
- `AX_OWNER_ABSENCE_LOG_DESTINATION_POLICY` v3
- `AX_OWNER_ABSENCE_LOG_SCHEMA_DESIGN` v1
- existing `scripts/sync_owner_absence_phase_a.py`
- existing `scripts/validate_owner_absence.py`
- backlog `cycle_log` entry for 2026-04-30 host inventory (n8n already running on the host)
