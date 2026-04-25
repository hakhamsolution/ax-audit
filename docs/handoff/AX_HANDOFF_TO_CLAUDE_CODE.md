# AX_HANDOFF_TO_CLAUDE_CODE

Version: 2026-04-26 v3
Status: execution handoff reflecting Decision 15 (AI-proposer / Human-approver); WB2 deadline revised after the 2026-04-26 cycle pass that resolved the GitHub plan-gate via public-flip and recorded the Owner decision to defer Track A token rotation
Audience: Codex (proposer) and Claude Code (γ gate reviewer), plus any other AI agent declared in PHASE0 §15.5.
Patch record:
- v1 (2026-04-18) written under Deputy Owner hybrid model; revoked same day
- v2 (2026-04-18) aligned with Decision 15
- v3 (2026-04-26) revises WB2 deadline from 2026-04-21 to 2026-05-08 by Owner decision; defines the `main` branch-protection ruleset as the first WB2 deliverable, executed end-to-end under γ gate (Codex proposer + distinct Claude Code reviewer + 강은구 approver) so that this protection round itself counts toward the K4 KPI

This document is an execution launcher, not a new policy.

## 1. Mission

Close Phase 0 and stand up the two Owner-absence canonicals so the Decision 15 governance model activated on 2026-04-19 is backed by real infrastructure, not just policy text.

Scope ends at KPI satisfaction in §3. Phase 1 (control plane establishment) is a separate cycle — out of scope.

## 2. Hard scope rules

1. Do not author new policy documents.
2. Do not extend schemas. Schema change is a γ gate action.
3. Do not re-open closed decisions (γ two-canonical structure, Decision 15 AI-proposer/Human-approver, rotate_secret R1/R2 split, Owner-absence response windows). Reference them rather than revising.
4. Improvements discovered during execution → `backlog.md` one-line entry. Not worked this cycle.
5. If a Work Block exposes a genuine blocker needing policy revision, stop and surface to 강은구. Do not invent a patch.

## 3. KPIs — cycle ends when all four are true

| KPI | Current | Target | Measurement |
|---|---|---|---|
| K1 PHASE0 §16 exit criteria done | 6 of 13 | 13 of 13 | direct checklist verification |
| K2 Decision 15 adoption checklist done | partial | all items from ADR §16 | cross-document consistency check |
| K3 Phase A automation (Notion → Git, Slack, Telegram) working | not built | built + verified | `OA-20260419-000` test declaration triggers all three mirrors within sync window |
| K4 γ gate workflow verified end-to-end | not verified | verified | one real γ gate action (e.g., a non-critical change_guard_rule test) runs through Codex proposal → Claude Code review → 강은구 approval without manual patching |

When all four read "done", stop. Do not continue improving.

## 4. Roles and this handoff

### 4.1 Humans
- 강은구: Owner, sole operational Approver
- 원혜연: Deputy Owner (dormant), Business Work Partner

### 4.2 AI agents in this cycle
- **Codex** = Proposer. Primary executor. Drafts changes as PRs with diff, rationale, policy references. Executes bash/git/API on 강은구's direction. Cannot approve.
- **Claude Code** = Reviewer (γ gate). Independent AI instance. Reviews PRs for γ gate action classes. Posts review comment with pass / borderline / fail and policy citations. Cannot approve. Cannot propose the same action it is reviewing.
- **Other agents** (n8n runners, future automation): declared in PHASE0 §15.5 with primary role before privileged access.

### 4.3 Rule for AI agents
AI agent receiving an instruction from 강은구 **does not execute directly**. It proposes. 강은구's instruction is a request to propose, not an approval. Approval requires a PR review gesture (GitHub PR approval, signed commit, or explicit message in audit log).

For γ gate action classes (R2 secret, change_guard_rule, change_secret_backend, retire_legacy_component, change_architecture_definition):
- Proposer creates PR
- Reviewer AI (distinct session, distinct context) independently reviews and posts policy conformance comment
- 강은구 reviews both the diff and the reviewer's comment, then approves or rejects
- Only after 강은구 approval, proposer executes merge

For non-γ privileged actions (promote_automation, demote_automation, R1 rotation, restart, rollback):
- Proposer creates PR
- 강은구 reviews and approves
- Proposer executes merge

Active-failure containment demotion: proposer may execute without approval but must post the action to the audit log within 5 minutes and create a retrospective review request for 강은구 within 1 hour.

## 5. Active document map

Read on every session:
- `CLAUDE.md` (project root, auto-loaded)
- `docs/active/AX_SUPERSESSION_AND_NAMING_NOTICE.md` (version truth + single-source-of-truth index)
- `docs/active/AX_AVAILABILITY_AND_RBAC.md` (authority matrix, Owner-absence, proposer-approver separation)
- `docs/active/AX_ARCHITECTURE_DECISIONS.md` (Decision 15 model)
- `docs/active/AX_PHASE0_INVENTORY_TEMPLATE.md` (§16 exit criteria, §15.5 AI agents, §15.6 follow-ups)

Consult when task domain matches:
- secrets, automation lifecycle, metrics, runtime platform → `docs/active/AX_OPERATIONS_POLICY.md`
- tenant separation, data classes, retention → `docs/active/AX_DATA_TENANCY_AND_RETENTION_POLICY.md`
- guard fail-open/fail-closed, borderline handling → `docs/active/AX_GUARD_FAILMODE_AND_RUNTIME_POLICY.md` *(not in handoff package at transfer time — see `backlog.md` → `gaps_at_handoff`)*
- Owner-absence log structure, broadcast automation, dual-outage fallback, queue behavior → `docs/active/AX_OWNER_ABSENCE_LOG_DESTINATION_POLICY.md`
- Owner-absence log field schema → `docs/active/AX_OWNER_ABSENCE_LOG_SCHEMA_DESIGN.md`
- architectural do-not-resurrect list, core-agent target → `docs/active/AX_ARCHITECTURE_DECISIONS.md`
- definitions of GoClaw, Hermes, core agent, specialist, layers → `docs/active/AX_SYSTEM_DEFINITIONS.md`
- migration phase plan → `docs/active/AX_MIGRATION_EXECUTION.md`

Audit record (not runtime):
- `docs/archive/patches/AX_DEPUTY_OWNER_PATCH.md` — **REVOKED**. Do not apply its rules.

## 6. Repository layout assumption

```
<repo-root>/
├── CLAUDE.md
├── backlog.md
├── docs/
│   ├── active/
│   │   ├── AX_SYSTEM_DEFINITIONS.md            (v2)
│   │   ├── AX_ARCHITECTURE_DECISIONS.md        (v4, Decision 15)
│   │   ├── AX_OPERATIONS_POLICY.md             (v5)
│   │   ├── AX_MIGRATION_EXECUTION.md           (v2)
│   │   ├── AX_AVAILABILITY_AND_RBAC.md         (v4)
│   │   ├── AX_PHASE0_INVENTORY_TEMPLATE.md     (v5)
│   │   ├── AX_GUARD_FAILMODE_AND_RUNTIME_POLICY.md (v1, missing — see backlog)
│   │   ├── AX_DATA_TENANCY_AND_RETENTION_POLICY.md (v1)
│   │   ├── AX_OWNER_ABSENCE_LOG_DESTINATION_POLICY.md (v3)
│   │   ├── AX_OWNER_ABSENCE_LOG_SCHEMA_DESIGN.md (v1)
│   │   └── AX_SUPERSESSION_AND_NAMING_NOTICE.md (v6)
│   ├── handoff/
│   │   └── AX_HANDOFF_TO_CLAUDE_CODE.md        (v2, this file)
│   └── archive/
│       ├── AX_AGENT_SYSTEM_FINAL_2026-04-18.md
│       └── patches/
│           └── AX_DEPUTY_OWNER_PATCH.md        (REVOKED)
├── audit/
│   ├── owner_absence.jsonl                     (created in WB1)
│   ├── owner_absence.schema.json               (created in WB1)
│   └── README.md                               (created in WB1)
└── scripts/
    ├── init_owner_absence_log.sh
    └── init_notion_owner_absence_db.py
```

## 7. Work blocks

### WB1 — Activation readiness

**Deadline**: activation was 2026-04-19; complete WB1 as early as possible, any outstanding items promoted to highest priority.

**Purpose**: make the declaration mechanism real; surface exposed secrets; first live γ gate and non-γ proposer-approver workflows.

**Track A — Secrets exposure scan** (Codex proposer, 강은구 approver)
- Human input needed: list of AX-adjacent repositories to scan.
- Codex actions: scan each repo with `git log --all -p` regex for secret patterns; inspect `.env*` files (report presence, do not echo contents to chat); draft a secrets inventory table as a PR updating PHASE0 §9.
- 강은구 approval: PR review and approve after verifying the scan scope.
- If exposed secrets are found: rotation is an R1 (Codex proposes rotation, 강은구 approves) or R2 (γ gate: Codex proposes, Claude Code reviews policy, 강은구 approves).
- Success: §9 populated, every detected secret classified R1/R2 with rotation status.

**Track B — Git canonical initialization** (Codex proposer, 강은구 approver)
- Human input: target repository (create `ax-audit` or use existing).
- Codex actions: create repo directory structure per §6; run `scripts/init_owner_absence_log.sh` from repo root; stage and commit on feature branch; open PR.
- 강은구 approval: review PR and approve.
- Success: `audit/owner_absence.jsonl`, `audit/owner_absence.schema.json`, `audit/README.md` merged via PR.

**Track C — Notion canonical initialization** (Codex proposer, 강은구 approver)
- Human input: Notion parent page ID, integration token (via env var, never logged), access list.
- Codex actions: run `scripts/init_notion_owner_absence_db.py --dry-run` to show payload; after 강은구 provides token, run for real; verify schema parity.
- Alternative: 강은구 creates DB manually in Notion UI; Codex runs `--verify`.
- 강은구 approval: approve the dry-run payload before execution (no PR required — execution is a one-shot API call, but the payload is reviewed in chat or log).
- Success: Notion DB exists; schema aligned; views created; access granted to 원혜연 (Full read for situational awareness) and governance-audit role (Read).

**WB1 completion gate**:
- Track A: §9 populated, rotation plan for each exposed secret
- Track B: PR merged, first non-γ proposer-approver workflow verified
- Track C: Notion DB created and schema-verified
- End-to-end smoke test: declaration `OA-20260419-000` written to both canonicals, marked ratified as test record, logs show proposer = Codex, approver = 강은구

### WB2 — Access realignment

**Deadline**: 2026-05-08 (revised 2026-04-26 by Owner decision; original was 2026-04-21).

**Purpose**: align technical access with Decision 15 model.

**Steps** (Codex proposer for each change, Claude Code reviewer for γ gate changes, 강은구 approver):
1. **First deliverable (γ gate end-to-end, doubles as K4 KPI proof):** Codex drafts a configuration PR that turns on `main` branch protection for `hakhamsolution/ax-audit` with at minimum: require a pull-request review before merge, require status check `validate` to pass, disallow direct push to `main`, and enforce the rule for repository administrators. The PR body must include the exact `gh api PUT /repos/hakhamsolution/ax-audit/branches/main/protection` call (or `gh api PUT /repos/hakhamsolution/ax-audit/rulesets/{id}` if rulesets are preferred) and the expected post-state from `gh api .../branches/main/protection`. A distinct Claude Code reviewer session (not the proposing session) posts a policy-conformance comment citing PHASE0 §15.3 (`change_guard_rule` is γ gate) and §14 (technical enforcement currently policy-only). 강은구 approves and Codex applies the protection, then captures the post-state proof into PHASE0 §14 / `backlog.md`.
2. Codex inventories every repo, secret store, data path where 강은구 or 원혜연 has direct write access.
3. For 원혜연: since her role is Business Work Partner and dormant Deputy, most direct write accesses should be reduced to read-only, except specific business-data paths where she needs write for work accept/modify. Codex drafts a reduction PR; 강은구 approves.
4. For 강은구: Codex ensures that for the remaining γ gate action classes, direct single-actor execution is technically prevented on the rest of the infrastructure (Slack/Telegram admin paths, Notion canonical, OpenClaw host runner, secret stores). Codex drafts configuration PR; Claude Code reviews (γ gate changes to access enforcement); 강은구 approves.
5. Codex records before/after in `backlog.md` under `access_realignment_log`.

**Success**: any γ gate action attempted as single-actor on the infrastructure is blocked technically, not just by policy. The first deliverable additionally proves K4 (γ gate workflow verified end-to-end) without manufacturing a synthetic test case.

### WB3 — Current-state inventory

**Deadline**: 2026-04-25.

**Purpose**: fill PHASE0 §4, §5, §6, §7, §8, §10, §12, §13, §14, §15.5.

**Strategy**: one inventory pass per section, starting from legacy handoff facts (21 agents, 57 skills, 38 bindings, 4 hooks).

**Priority order**:
1. §15.5 AI agents — most urgent since Codex is actively executing; no audit basis without this
2. §5 channel ownership map
3. §12 session-truth locations
4. §4 agent inventory
5. §6 tool map
6. §7 hook map
7. §8 wrapper/script inventory
8. §10 missing asset list
9. §13 fallback paths
10. §14 approval paths (note proposer type column — populate from §15.3 proposer-approver register)

**Process**: Codex drafts inventory rows as PRs; 강은구 approves per section.

**Success**: §16 exit criteria entries for §4–§15 all read "done".

### WB4 — Skill classification

**Deadline**: 2026-05-02.

**Purpose**: classify 57 skills.

**Process**: Codex drafts classification table as PR; 강은구 approves per batch (or per skill for ambiguous cases).

**Success**: §11 fully populated; K1 KPI at 13 of 13.

### WB5 — Phase A automation

**Deadline**: 2026-05-19 per AX_OWNER_ABSENCE_LOG_DESTINATION_POLICY §6.2.

**Purpose**: replace manual dual-canonical entry with automated Notion → Git, Slack, Telegram broadcast.

**Architecture** (policy §6.1):
- Notion webhook triggers on new or updated row
- n8n workflow (or GitHub Action) receives, validates against schema, appends to Git JSONL, posts to Slack, posts to Telegram
- schema failure → alert, no sync

**Steps**:
1. Codex drafts workflow on paper first; 강은구 reviews.
2. Codex builds in sandbox with test IDs `OA-SANDBOX-NNN`; purged before production.
3. Codex dry-runs with fabricated test record.
4. Claude Code reviews the workflow for policy conformance (this is a `promote_automation` action in the audit sense; proposer = Codex, reviewer not strictly required but recommended given the sync's audit role).
5. 강은구 approves promote_automation.
6. Codex promotes to production.
7. First real production declaration must propagate to all three mirrors within the sync window.

**Success**: K3 KPI reaches "built + verified". Manual dual-canonical entry retires.

## 8. Human-in-the-loop gates — consolidated

| Gate | Who decides | When | How it is logged |
|---|---|---|---|
| every PR | 강은구 | before merge | PR review record |
| γ gate reviewer comment | Claude Code | before 강은구 approval | PR review comment |
| Notion integration token | 강은구 | before script run | env var only; not logged in repo |
| access reduction approval | 강은구 | before each change in WB2 | `backlog.md` → `access_realignment_log` |
| agent target_state decision | 강은구 (원혜연 consulted for business-touching agents) | per agent in WB3 | inline in §4 table |
| skill classification edge cases | 강은구 | per item in WB4 | inline in §11 table |
| promote_automation for Phase A | 강은구 | before production in WB5 | declaration log + PR record |
| Owner-absence declaration | 강은구 if pre-planned; Codex with independent verification if reactive | as occurs | AX_OWNER_ABSENCE_LOG_DESTINATION_POLICY §4 |

Any other gate discovered: stop, surface, record in `backlog.md` under `newly_discovered_gates`. Do not invent authority.

## 9. Reporting format

At the end of every Work Block:

```
WB<n> status: <done | blocked | partial>
KPIs moved: <K1 6→7, K2 ..., ...>
Human input pending: <list or "none">
Blockers: <list or "none">
Proposer-approver violations detected: <count + details or "none">
γ gate reviewer disagreements: <count + details or "none">
Next: WB<n+1> or "cycle complete"
```

Do not auto-continue if there are unresolved human-input items or blockers.

## 10. Cycle completion

When all four KPIs (§3) are "done":
1. Final consistency check: PHASE0 §16, ADR §16 transition obligations, K3 and K4 verified by real flows.
2. Append cycle-closed note to `backlog.md` with timestamp and KPI snapshot.
3. Post cycle-complete report.
4. Do not start Phase 1 in the same conversation. Phase 1 requires new scope definition, fresh 강은구 approval, potentially a new handoff.

## 11. What to do when in doubt

1. Check active document set (§5).
2. Check this handoff for explicit rule.
3. Still ambiguous → stop, ask 강은구. Do not invent policy.
4. If 강은구's answer contradicts active docs → flag contradiction explicitly, wait for confirmation before acting.

## 12. Anti-patterns to avoid

- proposing to add a new `.md` file "to clarify things"
- merging policy documents because of overlap
- updating a document version number without a corresponding policy change
- treating 강은구's verbal instruction as "approved — execute directly" (must go through PR)
- AI agent approving AI proposal (only 강은구 approves)
- Codex reviewing its own γ gate PR (reviewer must be distinct instance)
- silently deferring a pending KPI by marking it done-with-asterisk
- starting Phase 1 because WB5 feels close to done
- reviving Decision 14 (Deputy Owner hybrid model) — it is revoked
- reviving "four-eyes required" or "self-approval forbidden" terminology — use γ gate and proposer-approver separation
- inventing a "fast path" that bypasses the PR pipeline for emergencies (except the documented active-failure containment demotion)
