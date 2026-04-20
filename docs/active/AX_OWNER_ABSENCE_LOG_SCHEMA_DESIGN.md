# AX_OWNER_ABSENCE_LOG_SCHEMA_DESIGN

Version: 2026-04-18 v1
Status: implementation design for AX_OWNER_ABSENCE_LOG_DESTINATION_POLICY v3 §4
Purpose: define the concrete schema for both canonical stores (Notion database and Git append-only JSONL file) so they can be initialized and kept aligned.

This document is the canonical implementation reference. The two canonicals must conform to it identically.

---

## 1. Schema version

`schema_version`: **1.0**

Any change to this schema is an architecture-adjacent action per AX_OWNER_ABSENCE_LOG_DESTINATION_POLICY §10 and requires γ gate approval (AI proposal + independent AI review + 강은구 approval).

---

## 2. Field definitions (canonical)

Every declaration record — in either store — must contain these fields with identical semantics.

| Field | Type | Required | Allowed values / format | Notes |
|---|---|---|---|---|
| declaration_id | string | yes | regex `^OA-\d{8}-\d{3}$` | format `OA-YYYYMMDD-NNN`; NNN is zero-padded sequence for that day |
| schema_version | string | yes | `1.0` (current) | version of this design document that the record conforms to |
| declared_by | enum | yes | `owner` / `deputy_owner` | who initiated the declaration |
| declared_by_name | string | yes | free text | actual human name (e.g. `강은구`); helpful for audit readability |
| start_time | ISO 8601 timestamp | yes | `YYYY-MM-DDTHH:MM:SS+TZ` | absence start |
| expected_end_time | ISO 8601 timestamp or null | conditional | null when `open_ended` is true | absence expected end |
| open_ended | boolean | yes | `true` / `false` | if true, `expected_end_time` must be null |
| trigger_condition | enum | yes | `planned_leave` / `incapacitated` / `unreachable` / `explicit_delegation` | matches AX_AVAILABILITY_AND_RBAC §5.5 trigger list |
| response_window_used | enum | yes | `general` / `emergency` / `overnight_non_emergency` | matches §5.5 window tiers |
| scope | string | yes | `full` or `partial:<description>` | if partial, description is required |
| ratification_status | enum | yes | `pending` / `ratified` / `reversed` | starts at `pending` on creation |
| ratified_at | ISO 8601 timestamp or null | conditional | required when `ratification_status` != `pending` | populated on Owner return |
| linked_actions | array of strings | yes | list of audit log entry IDs | may be empty on creation, appended as actions occur |
| canonical_source | enum | yes | `notion` / `git` | which canonical received the initial write |
| sync_state | enum | yes | `pending` / `synced` / `conflict` | current replication state |
| created_at | ISO 8601 timestamp | yes | auto-populated at creation | immutable once set |
| last_updated_at | ISO 8601 timestamp | yes | auto-populated at every update | mutable |

---

## 3. Validation rules

R1. `declaration_id` uniqueness: no two records may share a `declaration_id` within the same canonical. Cross-canonical duplicates are the **expected** case — both canonicals must contain the same declaration_id for a synced record.

R2. `open_ended` and `expected_end_time` mutual exclusivity:
- if `open_ended` = true → `expected_end_time` must be null
- if `open_ended` = false → `expected_end_time` must be a valid ISO 8601 timestamp

R3. `ratification_status` and `ratified_at` consistency:
- if `ratification_status` = `pending` → `ratified_at` must be null
- if `ratification_status` ∈ {`ratified`, `reversed`} → `ratified_at` must be populated

R4. `scope` partial format: if the value starts with `partial:`, everything after the colon is the required description and must not be empty.

R5. `start_time` ≤ `last_updated_at` always.

R6. `ratified_at` (when populated) must be ≥ `start_time`.

R7. Append-only: once a declaration record is created in either canonical, only the following fields may be updated:
- `expected_end_time` (if changed mid-absence by Owner)
- `ratification_status`
- `ratified_at`
- `linked_actions` (append only, never remove)
- `sync_state`
- `last_updated_at`

All other fields are immutable. Attempts to modify immutable fields must be rejected by validation and logged as an incident.

---

## 4. Notion database schema

### 4.1 Database name
`AX Owner Absence Declarations`

### 4.2 Property definitions

| Property | Notion type | Required | Options / Format |
|---|---|---|---|
| declaration_id | Title | yes | free text, validated against regex |
| schema_version | Rich text | yes | default value `1.0` |
| declared_by | Select | yes | options: `owner`, `deputy_owner` |
| declared_by_name | Rich text | yes | — |
| start_time | Date (with time) | yes | timezone required |
| expected_end_time | Date (with time) | no | timezone required; empty when open_ended |
| open_ended | Checkbox | yes | — |
| trigger_condition | Select | yes | options: `planned_leave`, `incapacitated`, `unreachable`, `explicit_delegation` |
| response_window_used | Select | yes | options: `general`, `emergency`, `overnight_non_emergency` |
| scope | Rich text | yes | — |
| ratification_status | Select | yes | options: `pending`, `ratified`, `reversed`; default `pending` |
| ratified_at | Date (with time) | no | populated on ratification |
| linked_actions | Rich text | yes | comma-separated or JSON array serialized as string; relation type considered for v2 of this schema |
| canonical_source | Select | yes | options: `notion`, `git` |
| sync_state | Select | yes | options: `pending`, `synced`, `conflict` |
| created_at | Created time | yes | auto |
| last_updated_at | Last edited time | yes | auto |

Notion's built-in "Created by" and "Last edited by" properties are also enabled but are not part of the canonical schema (they record which Notion user touched the row, which is orthogonal to `declared_by`).

### 4.3 Recommended views

- **All declarations**: default table view, sorted by start_time descending
- **Active absences**: filter `ratification_status = pending`, sorted by start_time descending
- **Pending ratification**: filter `ratification_status = pending AND open_ended = false AND expected_end_time < now()` (absences that should have ended)
- **Conflicts**: filter `sync_state = conflict`
- **By quarter**: board view grouped by quarter of start_time
- **Audit export**: filter last 90 days, sort by start_time ascending (for governance-audit quarterly review)

### 4.4 Access control
Per AX_OWNER_ABSENCE_LOG_DESTINATION_POLICY §9. Implement in Notion by:
- granting write access to 강은구 and authorized sync automation only
- granting read access to 강은구, 원혜연, and governance-audit
- not sharing with Requester or Viewer role accounts

---

## 5. Git append-only file schema

### 5.1 Paths
- data file: `audit/owner_absence.jsonl`
- schema reference file: `audit/owner_absence.schema.json`
- human-readable readme: `audit/README.md`

### 5.2 File format
JSONL: one JSON object per line, UTF-8, no trailing comma, newline-delimited.

### 5.3 Example record (schema v1.0)

```json
{"declaration_id":"OA-20260419-001","schema_version":"1.0","declared_by":"owner","declared_by_name":"강은구","start_time":"2026-04-19T09:00:00+09:00","expected_end_time":"2026-04-19T18:00:00+09:00","open_ended":false,"trigger_condition":"planned_leave","response_window_used":"general","scope":"full","ratification_status":"pending","ratified_at":null,"linked_actions":[],"canonical_source":"notion","sync_state":"pending","created_at":"2026-04-19T08:55:12+09:00","last_updated_at":"2026-04-19T08:55:12+09:00"}
```

### 5.4 Append-only enforcement

Three layers of enforcement, defense in depth:

**Layer 1 — repository protection**
- the `audit/` directory is on a protected branch
- direct pushes to main are disallowed; all changes go through PR
- PR requires approval by the human approver after AI proposal review (proposer-approver separation applied at Git level)

**Layer 2 — pre-commit hook**
- validates that the diff for `audit/owner_absence.jsonl` is append-only (no existing lines modified or removed)
- validates that every new line is a valid JSON object conforming to `audit/owner_absence.schema.json`
- rejects commits that violate either rule

**Layer 3 — CI validation**
- runs the same schema validation on every PR
- fails the build if the JSONL file has been non-append-modified
- this catches anyone who bypasses the pre-commit hook locally

### 5.5 Correction mechanism
Per R7, only a subset of fields may be updated. In an append-only file this means: to update a declaration, append a **new line** with the same `declaration_id` and the updated fields.

Reader rule: when multiple lines exist with the same `declaration_id`, the record with the latest `last_updated_at` is the authoritative version for that declaration. All prior lines are retained for audit history.

---

## 6. Cross-canonical alignment

### 6.1 Field parity
Every field in §2 must exist in both canonicals with identical semantics and allowed values.

### 6.2 Type mapping notes
- Notion `Checkbox` ↔ JSONL `boolean`
- Notion `Select` ↔ JSONL `string` (enum value)
- Notion `Date (with time)` ↔ JSONL `string` (ISO 8601)
- Notion `Rich text` ↔ JSONL `string`
- Notion `Created time` / `Last edited time` ↔ JSONL `created_at` / `last_updated_at` (must be written explicitly on the JSONL side since Git has no auto-populated timestamps)

### 6.3 Initial write direction
The `canonical_source` field records where the declaration was first written. The other canonical then receives a sync copy. Both copies carry the same `canonical_source` value (i.e. the field identifies the original write location, not "this store").

### 6.4 Conflict detection
If a declaration exists in both canonicals with different values for any immutable field (§3 R7), that is a `sync_state = conflict`. Resolution per AX_OWNER_ABSENCE_LOG_DESTINATION_POLICY §3.2.

---

## 7. Schema migration rule

When schema_version increments (e.g. 1.0 → 1.1 or 2.0):

1. The change is proposed as a γ gate action (AI proposal + independent AI review + 강은구 approval).
2. This design document is updated first and becomes v2 (or equivalent).
3. Both canonicals are migrated in the same change window.
4. All existing records retain their original `schema_version` value. New records use the new version.
5. Readers must handle multiple `schema_version` values gracefully.
6. A migration note is appended to `audit/README.md`.

---

## 8. Initialization artifacts

The following artifacts must be created to initialize the system:

- Notion database with the properties defined in §4 → created via the init script `init_notion_owner_absence_db.py` or manually in the Notion UI
- Git files at `audit/owner_absence.jsonl`, `audit/owner_absence.schema.json`, `audit/README.md` → created via the init script `init_owner_absence_log.sh`
- Pre-commit hook and CI validation → deferred to a follow-up task (these are append-only enforcement layers, not prerequisites for the first declaration)

The first declaration must not be made until the Notion database exists and the Git files exist. The first declaration should itself be logged as a test declaration (declaration_id `OA-20260419-000`) to verify end-to-end consistency, then marked ratified and archived as a test record.

---

## 9. Instruction to future sessions

This document defines the schema. It does not define the broadcast automation (see policy §6) or the append-only enforcement mechanics beyond the three-layer sketch in §5.4.

If you are asked to add a field, do not silently edit this document. Propose a schema version bump, obtain γ gate approval, and migrate both canonicals together.

If you are asked to use a different store as canonical (e.g. replacing Notion or Git), re-open AX_OWNER_ABSENCE_LOG_DESTINATION_POLICY first and only update this schema document after that policy is revised.
