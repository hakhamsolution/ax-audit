# AX_AVAILABILITY_AND_RBAC

Version: 2026-04-18 v3
Status: focused operating supplement, single source of truth for the action-to-role matrix
Supersession:
This document is part of the active AX document set and supersedes AX_AGENT_SYSTEM_FINAL (2026-04-18) where topics overlap.
v3 incorporates AX_DEPUTY_OWNER_PATCH (2026-04-18 v1 active).

## 1. Purpose

This document exists because availability and RBAC were identified as unresolved high-risk items.
It narrows those two topics into explicit working policy.

This document is the canonical source for the action-to-role matrix.
Other documents must reference §5.3 instead of restating the matrix.

## 2. Availability topology stance

Working topology:
- single active GoClaw control-plane instance
- documented rollback path
- isolated legacy fallback path
- no active-active multi-brain orchestration

Reason:
The current team size and operating burden do not justify immediate multi-primary orchestration complexity.
Reliability comes first from restartability, observability, backup, and disciplined fallback.

## 3. Minimum required availability controls

Required:
- service healthcheck
- auto-restart
- reverse proxy health monitoring
- config backup
- daily state backup
- weekly recovery drill
- incident log
- rollback procedure
- fallback intake procedure

## 4. Fallback decision rule

If GoClaw is unavailable for 10 minutes or more:
- Operator declares degraded mode
- public ingress is paused or redirected
- only pre-approved fallback channels are used
- no new production promotion actions occur
- legacy bot activation is allowed only if token/channel isolation is confirmed

## 5. RBAC model

### 5.1 Roles

Mandatory roles:
- Owner
- Deputy Owner
- Operator
- Approver
- Requester

Optional role:
- Viewer (read-only)

Deputy Owner is mandatory in any environment with fewer than three Owner-class humans.

Deputy Owner is not a backup Owner only.
Deputy Owner has defined peacetime authority and additional authority that activates only when Owner-absence is formally declared. See §5.5.

### 5.2 Action classes

Action classes:
- request_work
- view_status
- inspect_logs
- read_audit_log
- restart_service
- rollback_service
- rotate_secret_routine (Class R1)
- rotate_secret_backend_or_master (Class R2)
- promote_automation
- demote_automation
- change_guard_rule
- change_secret_backend
- retire_legacy_component
- change_architecture_definition

Secret class definitions:
- Class R1 — routine secret rotation: bot tokens, app tokens, third-party API keys with documented rotation procedure; any secret whose rotation does not change the secret architecture.
- Class R2 — backend or master secret operation: secret backend standard change, master encryption path change, age key replacement, any operation that affects how secrets are stored, encrypted, or accessed.

### 5.3 Canonical action-to-role matrix

| Action class | Owner | Deputy Owner (peacetime) | Deputy Owner (Owner-absence declared) | Operator | Approver |
|---|---|---|---|---|---|
| request_work | yes | yes | yes | yes | yes |
| view_status | yes | yes | yes | yes | yes |
| inspect_logs | yes | yes | yes | yes | no |
| read_audit_log | yes | yes | yes | yes | yes |
| restart_service | yes | yes | yes | yes | no |
| rollback_service | yes | yes | yes | yes | no |
| rotate_secret_routine (R1) | yes | yes | yes | yes | no |
| rotate_secret_backend_or_master (R2) | yes, four-eyes required | no | yes, post-hoc Owner review required | no | no |
| promote_automation | yes (no self-approval) | yes (no self-approval) | yes | no | yes (no self-approval) |
| demote_automation | yes (no self-approval) | yes (no self-approval) | yes | no | yes (no self-approval) |
| change_guard_rule | yes, four-eyes required | no | yes, post-hoc Owner review required | no | no |
| change_secret_backend | yes, four-eyes required | no | yes, post-hoc Owner review required | no | no |
| retire_legacy_component | yes, four-eyes required | no | yes, post-hoc Owner review required | no | no |
| change_architecture_definition | yes, four-eyes required | no | no — wait for Owner return and re-decide | no | no |

Notes:
- "four-eyes required" = the action requires explicit approval from a second Owner-class actor. Deputy Owner counts as the second actor for Owner-initiated four-eyes actions.
- "post-hoc Owner review required" = action may proceed during declared Owner-absence; Owner must review and ratify or reverse within 72 hours of return.
- "no self-approval" = the human who proposed the promotion or demotion may not be the human who approves it.

### 5.4 Self-approval rule

A human may not approve a promotion or demotion they themselves proposed.

This rule applies regardless of role and overrides any otherwise-permitted action grant.

If only one Owner-class actor is available (Owner-absence in effect and no Deputy):
- promotion and demotion actions are paused, or
- the action is queued and executed only after a second actor returns,

except for demotions required to contain an active failure, which proceed and are reviewed afterward.

### 5.5 Owner-absence declaration

Owner-absence is a declared, logged state. It is not inferred from response delay alone.

Trigger conditions:
- Owner is on planned leave longer than the agreed response window.
- Owner is medically or otherwise incapacitated.
- Owner has been unreachable beyond the agreed response window.
- Owner has explicitly delegated authority for a defined window.

Agreed response windows:
- general operations: 4 working hours
- emergency operations (active incident, security event, token collision, public-channel outage): 60 minutes
- overnight non-emergency: next working block

A reactive Owner-absence declaration is permitted only after the relevant window has elapsed without Owner response.

Required attributes of declaration:
- declaration ID
- declared by (Owner if pre-planned, Deputy Owner if reactive)
- start time
- expected end time (or "open-ended pending review")
- trigger condition
- scope (full or partial)
- log destination

Termination:
- Owner formally returns and acknowledges the audit log of actions taken during absence, or
- a successor Owner is named.

Audit:
- All actions taken under Owner-absence must be tagged in the central audit log with the declaration ID.
- There is no separate continuity log.

Post-hoc Owner review:
- Owner must review and ratify or reverse every "post-hoc Owner review required" action within 72 hours of return.

### 5.6 Two-person team minimum assignment

In a two-person environment:
- Owner and Deputy Owner are never the same human.
- Both humans hold Approver and Operator roles so the self-approval and operational continuity rules are enforceable.
- Channel mapping (§6) must reflect that both humans can act in operator and approval channels.

## 6. Channel mapping principle

- casual manager chat channels: Requester only
- operator channels: Operator actions allowed
- approval channels: Approver actions allowed
- owner-only admin path: secret backend, guard-rule model, legacy retirement, architecture definition change
- no secret-changing action in public request channels

Concrete channel/tool mapping must be produced in the Phase 0 inventory.

## 7. Audit rule

All non-requester privileged actions must be attributable to:
- actor
- role
- time
- target
- action
- result
- declaration ID if action was taken under declared Owner-absence

## 8. Review rule

RBAC must be reviewed:
- on every new manager addition,
- on every channel expansion,
- every quarter minimum.

The Deputy Owner mandatory rule must be re-evaluated when team grows to three or more Owner-class humans.
