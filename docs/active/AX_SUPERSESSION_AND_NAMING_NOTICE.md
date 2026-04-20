# AX_SUPERSESSION_AND_NAMING_NOTICE

Version: 2026-04-18 v6
Status: mandatory interpretation notice
Patch record:
v6 reflects Decision 15 (AI-proposer / Human-approver) adoption and Decision 14 (Deputy Owner hybrid model) revocation.

## 1. Active-source rule

The active document set with current versions is:

| Document | Version |
|---|---|
| AX_SYSTEM_DEFINITIONS | v2 |
| AX_ARCHITECTURE_DECISIONS | v4 |
| AX_OPERATIONS_POLICY | v5 |
| AX_MIGRATION_EXECUTION | v2 |
| AX_AVAILABILITY_AND_RBAC | v4 |
| AX_PHASE0_INVENTORY_TEMPLATE | v5 |
| AX_GUARD_FAILMODE_AND_RUNTIME_POLICY | v1 |
| AX_DATA_TENANCY_AND_RETENTION_POLICY | v1 |
| AX_OWNER_ABSENCE_LOG_DESTINATION_POLICY | v3 |
| AX_OWNER_ABSENCE_LOG_SCHEMA_DESIGN | v1 |

These documents supersede AX_AGENT_SYSTEM_FINAL (2026-04-18).

## 2. Historical-source rule

AX_AGENT_SYSTEM_FINAL (2026-04-18) is retained only as historical context. Must not be used as authoritative design source when it conflicts with active set.

Archive location: `docs/archive/AX_AGENT_SYSTEM_FINAL_2026-04-18.md` or equivalent clearly marked path.

## 3. Patch archive rule

Adopted patches are archived after content verified embedded in active set.

Archive location: `docs/archive/patches/`.

Currently archived patches:
- `docs/archive/patches/AX_DEPUTY_OWNER_PATCH.md` — **revoked** 2026-04-18 by ADR Decision 15. Retained for audit trail. Must not be used as active design reference.

## 4. Canonical naming rule

### Core agents
hq-router, research-core, automation-dev, ops-platform, business-content, comms-admin, archive-memory, governance-audit.

### Specialists
vet-research-specialist, codegen-specialist, incident-specialist.

### Roles (human)
Mandatory: Owner, Deputy Owner (dormant), Operator, Approver, Requester.
Optional: Viewer.
Business-side (out of AX governance scope): Business Work Partner.

### Roles (AI)
Proposer — AI agent authorized to draft privileged actions.
Reviewer — independent AI agent used in γ gate cross-check for high-risk action classes.

### Current role holders (as of 2026-04-18)
- Owner: 강은구
- Deputy Owner (dormant): 원혜연
- Approver (operational): 강은구
- Approver (formal, dormant): 원혜연
- Operator: 강은구 primary; 원혜연 available
- Business Work Partner: 원혜연
- Proposer (default): Codex
- Reviewer (default, γ gate): Claude Code

## 5. Deprecated names

From historical document:
- ops-guard; content-marketing; recovery-auditor; failure-analysis-specialist; research-specialist

From revoked decisions:
- "Deputy Owner hybrid model" (Decision 14)
- "self-approval forbidden rule" (replaced by proposer-approver separation rule)
- "four-eyes required" (replaced by γ gate)

## 6. Interpretation rule for new sessions

If a new session sees both historical document and active set: prefer active set; treat historical names as aliases only; do not revive deprecated names; do not generalize veterinary research into a generic research specialist unless a new ADR explicitly authorizes it.

If a new session sees an adopted (or revoked) patch file alongside active set: prefer active set for runtime interpretation; use patch file only as audit record of the decision.

If a new session sees AX_DEPUTY_OWNER_PATCH: it is **revoked** — do not apply any of its rules. Use ADR Decision 15 (AX_ARCHITECTURE_DECISIONS §15).

## 7. Alias map

ops-guard -> ops-platform
content-marketing -> business-content
recovery-auditor -> governance-audit
failure-analysis-specialist -> incident-specialist
research-specialist -> vet-research-specialist
"four-eyes required" (historical) -> "γ gate" (current)
"self-approval forbidden" (historical) -> "proposer-approver separation" (current)

## 8. Single source of truth notes

- Action-to-role authority matrix: AX_AVAILABILITY_AND_RBAC §5.3
- Owner-absence declaration definition: AX_AVAILABILITY_AND_RBAC §5.5
- Owner-absence log destination, schema, broadcast automation, dual-outage fallback: AX_OWNER_ABSENCE_LOG_DESTINATION_POLICY
- Owner-absence log field schema: AX_OWNER_ABSENCE_LOG_SCHEMA_DESIGN
- Proposer-approver separation rule: AX_AVAILABILITY_AND_RBAC §5.4
- γ gate semantics: AX_AVAILABILITY_AND_RBAC §5.3.1
- Decision 15 (governance model): AX_ARCHITECTURE_DECISIONS §15
- Decision 14 (revoked, audit reference): AX_ARCHITECTURE_DECISIONS §14 + `docs/archive/patches/AX_DEPUTY_OWNER_PATCH.md`
- Tenant isolation and data class definitions: AX_DATA_TENANCY_AND_RETENTION_POLICY
- Guard fail-open / fail-closed action classes: AX_GUARD_FAILMODE_AND_RUNTIME_POLICY §5
- Current humans and role assignments: AX_PHASE0_INVENTORY_TEMPLATE §15

Other documents may reference these but must not restate them.

## 9. Practical instruction

When generating new plans, prompts, migration guides, or agent maps:
- use only canonical names from this notice
- mark historical names as deprecated when cross-referencing old artifacts
- reference single sources of truth in §8 instead of restating their contents
- treat Notion and Git as two replicated canonicals of one central audit log; Slack + Telegram are alert mirrors only
- **under Decision 15: AI agents propose, 강은구 approves; never invent a second human approver; never route privileged actions through a human proposer to bypass the pipeline**
