# AX_OWNER_ABSENCE_LOG_DESTINATION_POLICY

Version: 2026-04-18 v3
Status: operating policy for Owner-absence declaration logging
Patch record:
- v1 proposed Notion canonical + 3 mirrors (Option α)
- v2 adopted γ two-canonical per Owner decision 2026-04-18
- v3 adjusted for Decision 15 (AI-proposer / Human-approver): Owner-absence queues proposals; declaration records add proposer/reviewer fields; dormant Deputy Owner note added

## 1. Purpose

Defines where Owner-absence declarations are recorded, how the multi-channel record stays consistent, and how the record aligns with AX_AVAILABILITY_AND_RBAC §5.5 central audit log.

## 2. Owner decision (2026-04-18)

Owner-absence declarations are recorded in four destinations, structured as two canonical stores and two alert mirrors.

| Destination | Role | Reason |
|---|---|---|
| Notion database | canonical — structured | searchable, structured schema, retention review, human-readable |
| Git append-only file | canonical — immutable | tamper-evident, audit-grade, survives SaaS outage, independent failure mode from Notion |
| Slack admin channel | alert mirror | real-time visibility; not audit evidence |
| Telegram | alert mirror | mobile-reach urgency; not audit evidence |

Two canonicals are replicated copies of the same central audit log, not two independent logs.

## 3. Canonical consistency rule

### 3.1 Equal authority
Notion and Git are both authoritative. A declaration is valid when it exists in at least one canonical with a well-formed record.

### 3.2 Conflict resolution
When Notion and Git contain different records for the same declaration_id: the record with later append timestamp is authoritative; earlier record retained as prior-version history; discrepancy registered as audit incident reviewed by governance-audit; if timestamps equal, manual resolution by 강은구 required and logged.

### 3.3 Independent failure modes
Notion failure modes: SaaS outage; API rate limit; account lockout; schema migration error; vendor policy change.
Git failure modes: repo access failure; credential rotation gap; push conflict; runner outage.
Simultaneous failure is major incident; dual-outage fallback in §8.

## 4. Required declaration schema

Every Owner-absence declaration must contain:

| Field | Required value |
|---|---|
| declaration_id | unique, format `OA-YYYYMMDD-NNN` |
| declared_by | Owner (if pre-planned); AI agent (if reactive, with independent verification) |
| declared_by_agent_id | AI agent identifier if reactive, else null |
| verifier_agent_id | independent AI identifier confirming reactive unreachability, else null |
| start_time | ISO 8601 timestamp |
| expected_end_time | ISO 8601 or null (open-ended) |
| trigger_condition | reference to AX_AVAILABILITY_AND_RBAC §5.5 list |
| response_window_used | general / emergency / overnight_non_emergency |
| scope | full / partial:<description> |
| ratification_status | pending / ratified / reversed |
| ratified_at | ISO 8601 or null |
| linked_actions | list of audit log entry IDs for queued proposals |
| queue_depth_at_declaration | integer — number of pending proposals at declaration time |
| queue_depth_at_ratification | integer — number processed on return |
| canonical_source | notion / git |
| sync_state | pending / synced / conflict |

v3 additions vs v2: `declared_by_agent_id`, `verifier_agent_id`, `queue_depth_at_declaration`, `queue_depth_at_ratification`. These fields support the Decision 15 model where Owner-absence detection may be initiated by an AI agent and where the proposal queue is a measurable metric.

### 4.1 Storage format
- Notion: one row per declaration with fields above as columns.
- Git: one JSONL line per declaration appended to `audit/owner_absence.jsonl`. Append-only. Correction by appending a new line with same declaration_id and updated values; the later line wins per §3.2.

## 5. Write path rules

### 5.1 Primary write
Declaring actor writes to one canonical:
- default primary: Notion (online, working hours)
- alternative primary: Git (Notion unavailable, off-network, or mobile path)

Reactive declaration by AI agent: the agent writes the declaration after independent verification of 강은구's unreachability (e.g., two failed attempts via separate channels). Verification details logged in `verifier_agent_id`.

### 5.2 Canonical sync
After primary write, declaration synchronized to the other canonical. Until broadcast automation exists, sync is manual within 15 minutes (general/overnight), 5 minutes (emergency).

### 5.3 Mirror broadcast
After declaration present in at least one canonical, alert mirrors sent to Slack and Telegram. Alert mirrors informational; may lag beyond canonical sync.

### 5.4 Write authority
Only 강은구 (pre-planned) or authorized AI agents (reactive with verification) may write declaration records. Automation may only write as sync agent between canonicals, not as originator.

## 6. Broadcast automation

### 6.1 Target state
At full maturity:
- trigger A: new Notion row → mirror to Git, Slack, Telegram
- trigger B: new Git JSONL line (push hook or polling) → mirror to Notion, Slack, Telegram
- trigger C: updated Notion row → new JSONL line in Git with updated record + Slack/Telegram update
- trigger D: amended Git record → update Notion row + Slack/Telegram update
- conflict detection: divergent record in canonical B while writing to A → sync_state = conflict; alert governance-audit; resolution per §3.2

### 6.2 Phased build
Phase A (target: within 30 days of activation, 2026-05-19)
- one-way sync: Notion → Git, Slack, Telegram
- manual entry in Git allowed but rare
- covers the common case where declarations originate in Notion

Phase B (target: within 60 days of activation, 2026-06-18)
- two-way sync: Git → Notion also supported
- conflict detection and alerting
- full §6.1 conformance

### 6.3 Runtime platform
Recommended: n8n or GitHub Actions per AX_OPERATIONS_POLICY §9. GitHub Actions for Git → Notion (native to Git events). n8n for Notion → Git (Notion webhook + Git commit via small worker).

## 7. Owner-absence queue behavior

Under Decision 15, 강은구 is the sole approver. Owner-absence means the approval queue holds pending proposals.

### 7.1 Queue behavior
- AI proposers continue to generate proposals during Owner-absence
- Each proposal tagged with the active declaration_id
- Proposals wait for 강은구's return
- Exception: active-failure containment demotion executes without approval and is reviewed afterward (per AX_AVAILABILITY_AND_RBAC §5.3 notes on demote_automation)

### 7.2 Dormant Deputy Owner note
원혜연 holds Deputy Owner authority formally. Default behavior during Owner-absence is **not** to activate Deputy authority; the queue simply waits. Activation is reserved for exceptional scenarios with procedure pending definition (AX_AVAILABILITY_AND_RBAC §5.5.1). If activation occurs, it must be logged as a first-of-kind event and used to codify the procedure.

### 7.3 Queue overflow
If the queue grows beyond a threshold (baseline: 20 pending proposals or a single proposal blocked more than 24 hours on a P1 path):
- governance-audit raises the condition as an incident
- 강은구 is notified via all available channels
- if still unresolved and business continuity is blocked, the dormant Deputy Owner activation procedure may be invoked (first-time use codifies the procedure)

## 8. Dual-outage fallback

When both Notion and Git are unavailable simultaneously:
- declaration may be posted to Slack or Telegram as temporary record
- temporary record migrated into both canonicals as soon as either is restored
- outage registered as audit incident
- emergency actions requiring Owner-absence authorization may proceed in the dual-outage window only if declarer commits to backfilling both canonicals within 24 hours of restoration

Dual outage rare due to independent failure modes (§3.3). More than once per quarter triggers canonical structure review.

## 9. Access control

| Destination | Write access | Read access |
|---|---|---|
| Notion database | 강은구, authorized AI agents (sync role), AI agent (reactive write with verification) | 강은구, 원혜연, governance-audit |
| Git append-only file | 강은구 manual commit; automation (sync role) | 강은구, 원혜연, governance-audit |
| Slack admin channel | broadcast automation + 강은구 + 원혜연 (manual alert) | 강은구, 원혜연, Operator, Approver |
| Telegram | broadcast automation + 강은구 + 원혜연 | 강은구, 원혜연 |

Requesters and Viewers have no access to Owner-absence declaration records.

## 10. Schema alignment requirement

Two canonicals require aligned schemas.

- Any change to Notion schema must be reflected in Git JSONL field set and vice versa.
- Schema changes are γ gate (change_architecture_definition-adjacent) and require AI proposal + independent AI review + 강은구 approval.
- `schema_version` field on every record makes migration history visible.

## 11. Retention

Owner-absence records are Class B per AX_DATA_TENANCY_AND_RETENTION_POLICY §4. Retention reviewed every 180 days. Records tied to Class D data use the stricter Class D schedule of linked data. Git append-only file retained indefinitely unless governance-audit approves compaction.

## 12. Audit integration

Every action under declared Owner-absence includes declaration_id in central audit log entry. Join key between declarations and authorized actions.

governance-audit responsibilities (ADR §11) applied directly:
- audit of Owner-absence declarations — verify each exists in both canonicals with aligned records
- audit of proposer-approver separation — verify every completed action has distinct proposer and approver entities
- audit of γ gate completion — verify reviewer entry exists for γ gate action classes
- audit of post-hoc processing — verify every queued proposal is processed on 강은구's return
- audit of canonical consistency — review any `conflict` sync_state and confirm resolution
- audit of manual override incidents — verify any human direct modification was logged with rationale

## 13. Alignment with AX_AVAILABILITY_AND_RBAC §5.5

§5.5 requires central audit log, no separate continuity log.

This policy interprets "central audit log" as "one logical log, replicated across two canonicals with consistency guarantees." Not a separate continuity log because: Notion and Git contain same content by design; any divergence is incident to resolve, not design feature; Slack and Telegram are explicitly non-audit alert surfaces.

If governance-audit determines the two-canonical structure has drifted into two parallel independent logs, structure must collapse back to single canonical and this policy revised.

## 14. Review and revision

Review when: Phase A automation goes live; Phase B automation goes live; a canonical is added, removed, or replaced; dual outage occurs more than once per quarter; quarterly minimum.

## 15. Instruction to future sessions

Notion and Git are canonical. Slack and Telegram are alert mirrors. Two canonicals are replicated copies of one log. Manual propagation is interim. If Notion and Git drift into independent-log behavior, escalate to governance-audit.

Under Decision 15, Owner-absence queues proposals rather than activating a Deputy. Dormant Deputy exists for exceptional cases with procedure pending.
