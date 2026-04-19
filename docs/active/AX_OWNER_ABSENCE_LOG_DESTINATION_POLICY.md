# AX_OWNER_ABSENCE_LOG_DESTINATION_POLICY

Version: 2026-04-18 v2
Status: operating policy for Owner-absence declaration logging
Patch record:
- v1 proposed Notion canonical + 3 mirrors (Option α) as default pending Owner confirmation
- v2 adopts two-canonical structure (Option γ) per Owner decision 2026-04-18

## 1. Purpose

This document defines where Owner-absence declarations are recorded, how the multi-channel record stays consistent, and how the record aligns with AX_AVAILABILITY_AND_RBAC §5.5 which mandates a central audit log.

## 2. Owner decision (2026-04-18)

Owner-absence declarations are recorded in four destinations, structured as two canonical stores and two alert mirrors.

| Destination | Role | Reason |
|---|---|---|
| Notion database | canonical — structured | searchable, structured schema, supports retention review, human-readable |
| Git append-only file | canonical — immutable | tamper-evident, audit-grade, survives SaaS outage, independent failure mode from Notion |
| Slack admin channel | alert mirror | real-time visibility to operators; not audit evidence |
| Telegram | alert mirror | mobile-reach urgency; not audit evidence |

The two canonical stores are treated as replicated copies of the same central audit log, not as two independent logs.
Slack and Telegram are notification surfaces only.

## 3. Canonical consistency rule

### 3.1 Equal authority
Notion and Git are both authoritative.
Either may be cited as audit evidence.
A declaration is considered valid when it exists in at least one canonical store with a well-formed record.

### 3.2 Conflict resolution
When Notion and Git contain different records for the same declaration_id:
- the record with the later append timestamp is authoritative,
- the earlier record is retained as prior-version history,
- the discrepancy is registered as an audit incident and reviewed by governance-audit,
- if timestamps are equal (same second or unavailable), manual resolution by Owner is required and the resolution itself is logged.

### 3.3 Independent failure modes
Notion and Git are chosen precisely because their failure modes are independent:
- Notion failure modes: SaaS outage, API rate limit, account lockout, schema migration error, vendor policy change
- Git failure modes: repo access failure, credential rotation gap, push conflict, runner outage

Simultaneous failure of both is considered a major incident and triggers the dual-outage fallback in §8.

## 4. Required declaration schema

Every Owner-absence declaration must contain:

| Field | Required value |
|---|---|
| declaration_id | unique identifier, format `OA-YYYYMMDD-NNN` |
| declared_by | Owner (if pre-planned) or Deputy Owner (if reactive) |
| start_time | ISO 8601 timestamp |
| expected_end_time | ISO 8601 timestamp or the literal string `open-ended` |
| trigger_condition | reference to AX_AVAILABILITY_AND_RBAC §5.5 trigger list |
| response_window_used | `general` / `emergency` / `overnight_non_emergency` |
| scope | `full` or `partial:<description>` |
| ratification_status | `pending` / `ratified` / `reversed` |
| ratified_at | ISO 8601 timestamp, populated on Owner return |
| linked_actions | list of audit log entries tagged with this declaration_id |
| canonical_source | `notion` or `git` (which canonical received the initial write) |
| sync_state | `pending` / `synced` / `conflict` |

### 4.1 Storage format
- Notion: one row per declaration with the fields above as columns.
- Git: one JSONL line per declaration, appended to a single file `audit/owner_absence.jsonl`. The file is append-only. Correction requires a new line with the same declaration_id and an updated record; the later line wins per §3.2.

## 5. Write path rules

### 5.1 Primary write
The declaring human writes to one of the two canonical stores:
- default primary: Notion (when online, during working hours)
- alternative primary: Git (when Notion is unavailable, when off-network, or when declaring from a mobile path that has easier Git access)

### 5.2 Canonical sync
After a primary write, the declaration is synchronized to the other canonical.
Until broadcast automation exists, sync is manual and must be completed within 15 minutes for general and overnight_non_emergency declarations, and within 5 minutes for emergency declarations.

### 5.3 Mirror broadcast
After the declaration is present in at least one canonical, alert mirrors are sent to Slack and Telegram.
Alert mirrors are informational and may be delayed beyond the canonical sync window.

### 5.4 Write authority
Only Owner and Deputy Owner may write Owner-absence declaration records.
Automation may write only as a sync agent between canonicals, not as an originator.

## 6. Broadcast automation requirement

### 6.1 Target state
Required automation at full maturity:
- trigger A: new Notion row → mirror to Git, Slack, Telegram
- trigger B: new Git JSONL line (via push hook or polling) → mirror to Notion, Slack, Telegram
- trigger C: updated Notion row → new JSONL line in Git with updated record, plus Slack/Telegram update notification
- trigger D: amended Git record → update Notion row, plus Slack/Telegram update notification
- conflict detection: if a write arrives at canonical B while a divergent record already exists in canonical B for the same declaration_id, automation logs a sync_state of `conflict` and alerts governance-audit; resolution follows §3.2.

### 6.2 Phased build
Build in two phases to avoid over-engineering before the first real declaration:

Phase A (target: within 30 days of activation)
- one-way sync: Notion → Git, Slack, Telegram
- manual entry in Git is allowed but must be rare
- covers the common case where declarations originate in Notion

Phase B (target: within 60 days of activation)
- two-way sync: Git → Notion also supported
- conflict detection and alerting
- full conformance with §6.1

### 6.3 Runtime platform
Recommended: n8n or GitHub Actions, per AX_OPERATIONS_POLICY §9 runtime platform priority.
GitHub Actions is recommended for the Git → Notion direction (native to Git events).
n8n is recommended for the Notion → Git direction (Notion webhook and Git commit operations via a small worker).

## 7. Interim operating rule (pre-automation)

Until the Phase A automation exists:
- every declaration must be manually entered in both canonicals within the §5.2 sync window
- the human performing the declaration is responsible for consistency
- if the second canonical write is missed, governance-audit treats the first write as the authoritative record and flags the gap as an incident
- alert mirrors (Slack, Telegram) are best-effort during the interim

The interim period must not exceed 30 days from activation date (2026-04-19 → 2026-05-19).
If Phase A is not complete by 2026-05-19, the reason must be documented and an extension approved by Owner.

## 8. Dual-outage fallback

When both Notion and Git are unavailable simultaneously:
- declaration may be posted to Slack or Telegram as a temporary record
- the temporary record must be migrated into both canonicals as soon as either is restored
- the outage itself is registered as an audit incident
- emergency actions requiring Owner-absence authorization may proceed in the dual-outage window only if the declarer commits to backfilling both canonicals within 24 hours of restoration

Dual outage is rare because of the independent failure modes (§3.3).
If dual outage occurs more than once per quarter, the canonical structure must be reviewed.

## 9. Access control on each destination

| Destination | Write access | Read access |
|---|---|---|
| Notion database | Owner, Deputy Owner (manual); automation (sync role) | Owner, Deputy Owner, Approver, governance-audit |
| Git append-only file | Owner, Deputy Owner (manual commit); automation (sync role) | Owner, Deputy Owner, Approver, governance-audit |
| Slack admin channel | broadcast automation + Owner + Deputy Owner (manual alert) | Owner, Deputy Owner, Operator, Approver |
| Telegram | broadcast automation + Owner + Deputy Owner (manual alert) | Owner, Deputy Owner |

Requesters and Viewers have no access to Owner-absence declaration records.

## 10. Schema alignment requirement

Because there are two canonicals, the schemas must remain aligned.

- Any change to the Notion database schema must be reflected in the Git JSONL field set, and vice versa.
- Schema changes are a change_architecture_definition-adjacent action and require four-eyes.
- A schema version field (`schema_version`) should be added to every record so migration history is visible.

## 11. Retention

Owner-absence declaration records are Class B internal business data per AX_DATA_TENANCY_AND_RETENTION_POLICY §4.
Retention: reviewed every 180 days.
Records tied to actions involving Class D data use the stricter Class D retention schedule of the linked data.
Git append-only file is retained indefinitely unless governance-audit approves compaction.

## 12. Audit integration

Every action taken under a declared Owner-absence must include the declaration_id in the central audit log entry.
The declaration_id is the join key between declarations and the actions they authorized.

governance-audit responsibilities added in ADR §11 apply directly to this policy:
- audit of Owner-absence declarations → verify each declaration exists in both canonicals with aligned records
- audit of post-hoc Owner review execution → verify ratification_status becomes `ratified` or `reversed` within 72 hours of Owner return
- audit of canonical consistency → review any `conflict` sync_state and confirm resolution

## 13. Alignment with AX_AVAILABILITY_AND_RBAC §5.5

§5.5 requires a central audit log and forbids a separate continuity log.

This policy interprets "central audit log" as "one logical log, replicated across two canonicals with consistency guarantees."

This is not a separate continuity log because:
- Notion and Git contain the same content by design,
- any divergence is an incident to be resolved, not a design feature,
- Slack and Telegram are explicitly declared non-audit alert surfaces.

If governance-audit determines that the two-canonical structure has drifted into operating as two parallel logs with divergent content, the structure must be collapsed back to a single canonical and this policy revised.

## 14. Review and revision

This policy must be reviewed:
- when Phase A automation goes live (may simplify §5 and §7)
- when Phase B automation goes live (may simplify §6)
- if a canonical is added, removed, or replaced
- if dual outage occurs more than once per quarter
- quarterly minimum

## 15. Instruction to future sessions

Do not treat all four destinations as equivalent.
Notion and Git are canonical. Slack and Telegram are alert mirrors.
The two canonicals are replicated copies of the same log, not two independent logs.
Manual propagation is an interim state, not a target state.
If you observe that Notion and Git are drifting into independent-log behavior, escalate to governance-audit and reconsider the structure.
