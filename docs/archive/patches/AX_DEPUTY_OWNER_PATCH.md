# AX_DEPUTY_OWNER_PATCH

Version: 2026-04-18 v1 active (finalized, activation scheduled 2026-04-19, checklist updated 2026-04-18 with γ confirmation)
Status: approved patch, applied to OPS v4, AVAILABILITY v3, ADR v3, PHASE0 v4
Purpose: resolve N1 (Deputy Owner mandatory status) and N2 (Deputy Owner authority scope) and define Owner-absence semantics.

Owner approval recorded: 2026-04-18.
Deputy Owner assignment confirmed: 2026-04-18 (원혜연 accepted).
Log destination structure confirmed: 2026-04-18 (γ two-canonical).
Activation date: 2026-04-19.

This document is retained as the canonical record of the patch decision.
The patch content is now embedded in the target documents.
This file should be archived under `docs/archive/patches/` after the active set has been verified to reflect all clauses.

---

## 1. Decision summary

Hybrid Deputy Owner authority model (Option C) is adopted.

- Deputy Owner is mandatory in any environment with fewer than three Owner-class humans.
- Deputy Owner permissions split on two axes:
  - axis 1: action risk class (single-actor allowed vs four-eyes required)
  - axis 2: peacetime authority vs Owner-absence-declared additional authority
- Owner-absence is a declared, logged state, not an inferred one.
- Self-approval is forbidden when Owner and Approver are the same person.
- AVAILABILITY_AND_RBAC §5 is the single source of truth for the action-to-role matrix.
- OPERATIONS_POLICY §4 references the matrix instead of restating it.

---

## 2. Authority matrix (canonical)

This matrix is the single source of truth. The authoritative copy lives in AX_AVAILABILITY_AND_RBAC §5.3.

| Action class | Owner | Deputy Owner (peacetime) | Deputy Owner (Owner-absence declared) | Operator | Approver |
|---|---|---|---|---|---|
| request_work | yes | yes | yes | yes | yes |
| view_status | yes | yes | yes | yes | yes |
| inspect_logs | yes | yes | yes | yes | no |
| read_audit_log | yes | yes | yes | yes | yes |
| restart_service | yes | yes | yes | yes | no |
| rollback_service | yes | yes | yes | yes | no |
| rotate_secret_routine (Class R1) | yes | yes | yes | yes | no |
| rotate_secret_backend_or_master (Class R2) | yes, four-eyes required | no | yes, post-hoc Owner review required | no | no |
| promote_automation | yes (no self-approval) | yes (no self-approval) | yes | no | yes (no self-approval) |
| demote_automation | yes (no self-approval) | yes (no self-approval) | yes | no | yes (no self-approval) |
| change_guard_rule | yes, four-eyes required | no | yes, post-hoc Owner review required | no | no |
| change_secret_backend | yes, four-eyes required | no | yes, post-hoc Owner review required | no | no |
| retire_legacy_component | yes, four-eyes required | no | yes, post-hoc Owner review required | no | no |
| change_architecture_definition | yes, four-eyes required | no | no — wait for Owner return and re-decide | no | no |

### 2.1 Secret class definitions (referenced by rotate_secret rows)

- Class R1 — routine secret rotation
  - bot tokens with documented rotation procedure
  - app tokens with documented rotation procedure
  - API keys for third-party services with documented rotation procedure
  - any secret whose rotation does not change the secret architecture
- Class R2 — backend or master secret operation
  - secret backend standard change (e.g. SOPS+age to alternative)
  - master encryption path change
  - age key replacement
  - any operation that affects how secrets themselves are stored, encrypted, or accessed

### 2.2 Notes
- "four-eyes required" = the action requires explicit approval from a second Owner-class actor. Deputy Owner counts as the second actor for Owner-initiated four-eyes actions.
- "post-hoc Owner review required" = action may proceed during declared Owner-absence, but Owner must review and ratify or reverse within 72 hours of return.
- "no self-approval" = the human who proposed the promotion or demotion may not be the human who approves it.

---

## 3. Owner-absence declaration

### 3.1 Definition
Owner-absence is a declared, logged state in which Deputy Owner gains the additional authority shown in the matrix. It is not inferred from response delay alone.

### 3.2 Trigger conditions and response windows
Owner-absence may be declared when one or more apply:

- Owner is on planned leave longer than the agreed response window.
- Owner is medically or otherwise incapacitated.
- Owner has been unreachable beyond the agreed response window.
- Owner has explicitly delegated authority for a defined window.

Agreed response windows:
- general operations: 4 working hours
- emergency operations (active incident, security event, token collision, public-channel outage): 60 minutes
- overnight non-emergency: next working block

A reactive Owner-absence declaration is permitted only after the relevant window has elapsed without Owner response.

### 3.3 Required attributes of declaration
Every Owner-absence declaration must record:
- declaration ID
- declared by (Owner if pre-planned, Deputy Owner if reactive)
- start time
- expected end time (or "open-ended pending review")
- trigger condition
- scope (full or partial)
- canonical_source (which of Notion or Git received the initial write)

### 3.4 Termination
Owner-absence ends when:
- Owner formally returns and acknowledges the audit log of actions taken during absence, or
- a successor Owner is named.

### 3.5 Audit and log destination
All actions taken under Owner-absence must be tagged in the central audit log with the declaration ID.

The central audit log is implemented as a two-canonical (Notion + Git) replicated structure with two alert mirrors (Slack + Telegram). Full policy: AX_OWNER_ABSENCE_LOG_DESTINATION_POLICY v2.

---

## 4. Self-approval rule

A human may not approve a promotion or demotion they themselves proposed.

This rule applies regardless of role and overrides any otherwise-permitted action grant.

If only one Owner-class actor is available (Owner-absence in effect and no Deputy):
- promotion and demotion actions are paused, or
- the action is queued and executed only after a second actor returns,

except for demotions required to contain an active failure, which proceed and are reviewed afterward.

---

## 5. Two-person team assignment (actual)

Confirmed 2026-04-18:
- Owner: 강은구
- Deputy Owner: 원혜연
- Approver: 강은구 and 원혜연 (both)
- Operator: 강은구 and 원혜연 (both)

Owner and Deputy Owner are two distinct humans.
Both humans hold Approver so the self-approval rule is enforceable.
Both humans hold Operator so restart and rollback are not blocked by absence.

---

## 6. Resolved open questions

| Q | Decision |
|---|---|
| Q1 Deputy Owner mandatory? | Mandatory. |
| Q2 Owner response window? | General 4 working hours / emergency 60 minutes / overnight non-emergency next working block. |
| Q3 Owner-absence log location? | γ two-canonical: Notion + Git as canonical, Slack + Telegram as alert mirrors. Detail in AX_OWNER_ABSENCE_LOG_DESTINATION_POLICY v2. |
| Q4 architecture change four-eyes? | Required, not just recommended. |
| Q5 post-hoc Owner review window? | 72 hours after Owner return. |

---

## 7. Adjustments applied during finalization

1. change_architecture_definition raised from "four-eyes recommended" to "four-eyes required."
2. rotate_secret split into two classes (R1 routine, R2 backend/master/age key) with different authority levels.
3. Owner response window split into three tiers (general / emergency / overnight non-emergency) instead of a single window.
4. Log destination confirmed as γ two-canonical structure after Option α / β / γ comparison (2026-04-18).

---

## 8. Activation checklist (status as of 2026-04-18, updated with γ confirmation)

| Step | Status |
|---|---|
| Owner approves matrix in §2 | done |
| Owner and Deputy Owner formally named | done — 강은구 Owner, 원혜연 Deputy Owner |
| AX_OPERATIONS_POLICY updated to v4 | done |
| AX_AVAILABILITY_AND_RBAC updated to v3 | done |
| AX_ARCHITECTURE_DECISIONS updated to v3 | done |
| AX_PHASE0_INVENTORY_TEMPLATE updated to v4 | done (§15 filled, §15.4 γ confirmed) |
| AX_SUPERSESSION_AND_NAMING_NOTICE updated to v5 | done |
| Owner-absence declaration log destination policy created | done — AX_OWNER_ABSENCE_LOG_DESTINATION_POLICY v2 |
| Owner-absence declaration log destination structural choice confirmed | **done — γ two-canonical (Notion + Git) + two alert mirrors (Slack + Telegram)** |
| Notion database initialization per OWNER_ABSENCE_LOG_DESTINATION_POLICY §4 | **pending** |
| Git append-only file initialization at `audit/owner_absence.jsonl` | **pending** |
| Phase A broadcast automation (Notion → Git, Slack, Telegram) | **pending** (30-day deadline 2026-05-19) |
| Phase B broadcast automation (two-way with conflict detection) | **pending** (60-day deadline 2026-06-18) |
| Effective access reduction for 원혜연 to Deputy Owner peacetime scope | **pending** (PHASE0 §15.6 item 1) |
| Effective access enforcement for four-eyes actions on 강은구 | **pending** (PHASE0 §15.6 item 2) |
| §15.5 AI agents table populated | **pending** |
| governance-audit informed of three new audit responsibilities + canonical consistency audit | pending |
| Codex packet updated to reflect Deputy Owner hybrid model, self-approval rule, and log destination structure | pending separate task (blocked until PHASE0 channel / secret inventory) |

---

## 9. Activation rule

The hybrid authority model is policy-complete as of 2026-04-18 v4 of the document set.
It becomes operationally active on 2026-04-19 when:
- self-approval becomes forbidden for promote_automation and demote_automation
- four-eyes requirements apply to R2, change_guard_rule, change_secret_backend, retire_legacy_component, change_architecture_definition
- Owner-absence declarations become the only path to elevated Deputy authority
- Owner-absence declarations must be entered in both canonicals per γ structure

Items listed as "pending" in §8 do not block activation of the policy logic.
They do define follow-up work that must be completed to bring the real system into conformance with the now-active policy.

During the interim period before broadcast automation exists (up to 2026-05-19 for Phase A, up to 2026-06-18 for Phase B):
- dual-canonical manual entry is required within the sync windows defined in AX_OWNER_ABSENCE_LOG_DESTINATION_POLICY §5.2
- Slack and Telegram alerts are best-effort

---

## 10. Note to future sessions

Do not treat Deputy Owner as a passive backup.
Do not let Deputy Owner authority quietly expand into Owner-equivalence in peacetime.
Do not skip the Owner-absence declaration when convenient.
Do not collapse rotate_secret R1 and R2 back into a single action class.
Do not collapse the two canonicals into one, and do not treat the four destinations as equivalent.
The hybrid model only works if all five rules are enforced.
