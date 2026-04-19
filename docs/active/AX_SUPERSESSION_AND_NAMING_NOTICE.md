# AX_SUPERSESSION_AND_NAMING_NOTICE

Version: 2026-04-20 v9
Status: mandatory interpretation notice
Patch record:
v5 reflects the γ confirmation of Owner-absence log destination and the resulting version bumps in PHASE0 and OWNER_ABSENCE_LOG.
- v6 reflects the recovered `AX_GUARD_FAILMODE_AND_RUNTIME_POLICY` document and `AX_PHASE0_INVENTORY_TEMPLATE` v5.
- v7 reflects `AX_PHASE0_INVENTORY_TEMPLATE` v7 after live credential-layout proof and GitHub remote identification.
- v8 reflects `AX_PHASE0_INVENTORY_TEMPLATE` v8 after GitHub HTTPS bootstrap and remote initialization.
- v9 reflects `AX_PHASE0_INVENTORY_TEMPLATE` v9 after GitHub billing/plan gate evidence was captured.

## 1. Active-source rule

The active document set with current versions is:

| Document | Version |
|---|---|
| AX_SYSTEM_DEFINITIONS | v2 |
| AX_ARCHITECTURE_DECISIONS | v3 |
| AX_OPERATIONS_POLICY | v4 |
| AX_MIGRATION_EXECUTION | v2 |
| AX_AVAILABILITY_AND_RBAC | v3 |
| AX_PHASE0_INVENTORY_TEMPLATE | v9 |
| AX_GUARD_FAILMODE_AND_RUNTIME_POLICY | v1 |
| AX_DATA_TENANCY_AND_RETENTION_POLICY | v1 |
| AX_OWNER_ABSENCE_LOG_DESTINATION_POLICY | v2 |

These documents supersede AX_AGENT_SYSTEM_FINAL (2026-04-18).

## 2. Historical-source rule

AX_AGENT_SYSTEM_FINAL (2026-04-18) is retained only as historical context.
It must not be used as the authoritative design source when it conflicts with the active set.

Archive location for the historical document must be:
`docs/archive/AX_AGENT_SYSTEM_FINAL_2026-04-18.md`
or an equivalent clearly marked archive path.

## 3. Patch archive rule

Adopted patches are archived after their content has been verified to be embedded in the active set.

Archive location for adopted patches must be:
`docs/archive/patches/`

Currently archived patches:
- `docs/archive/patches/AX_DEPUTY_OWNER_PATCH_2026-04-18_v1.md` (adopted into AVAILABILITY v3, OPS v4, ADR v3 Decision 14, PHASE0 v4, OWNER_ABSENCE_LOG v2; activation 2026-04-19)

A patch may be referenced from the active documents but the active documents must not depend on the patch file for runtime interpretation.

## 4. Canonical naming rule

Active canonical names are:

### Core agents
- hq-router
- research-core
- automation-dev
- ops-platform
- business-content
- comms-admin
- archive-memory
- governance-audit

### Specialists
- vet-research-specialist
- codegen-specialist
- incident-specialist

### Roles
Mandatory:
- Owner
- Deputy Owner
- Operator
- Approver
- Requester

Optional:
- Viewer

### Current role holders (as of 2026-04-18)
- Owner: 강은구
- Deputy Owner: 원혜연
- Approver: 강은구, 원혜연
- Operator: 강은구, 원혜연

## 5. Deprecated names from the historical document

- ops-guard
- content-marketing
- recovery-auditor
- failure-analysis-specialist
- research-specialist

## 6. Interpretation rule for new sessions

If a new session sees both the historical document and the active set:
- prefer the active set,
- treat the historical names as aliases only,
- do not revive deprecated names as new design decisions,
- do not generalize veterinary research into a generic research specialist unless a new ADR explicitly authorizes it.

If a new session sees an adopted patch file alongside the active set:
- prefer the active set for runtime interpretation,
- use the patch file only as the audit record of the decision.

## 7. Alias map

ops-guard -> ops-platform
content-marketing -> business-content
recovery-auditor -> governance-audit
failure-analysis-specialist -> incident-specialist
research-specialist -> vet-research-specialist

## 8. Single source of truth notes

- Action-to-role authority matrix: AX_AVAILABILITY_AND_RBAC §5.3
- Owner-absence declaration definition: AX_AVAILABILITY_AND_RBAC §5.5
- Owner-absence log destination, schema, broadcast automation, and dual-outage fallback: AX_OWNER_ABSENCE_LOG_DESTINATION_POLICY
- Self-approval rule: AX_AVAILABILITY_AND_RBAC §5.4
- Tenant isolation and data class definitions: AX_DATA_TENANCY_AND_RETENTION_POLICY
- Guard fail-open / fail-closed action classes: AX_GUARD_FAILMODE_AND_RUNTIME_POLICY §5
- Current humans and role assignments: AX_PHASE0_INVENTORY_TEMPLATE §15

Other documents may reference these but must not restate them.

## 9. Practical instruction

When generating new plans, prompts, migration guides, or agent maps:
- use only canonical names from this notice,
- mark historical names as deprecated when cross-referencing old artifacts,
- reference the single sources of truth in §8 instead of restating their contents,
- treat Notion and Git as two replicated canonicals of one central audit log for Owner-absence declarations, and treat Slack + Telegram as alert mirrors only.
