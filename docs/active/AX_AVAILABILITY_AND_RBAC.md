# AX_AVAILABILITY_AND_RBAC

Version: 2026-04-18 v4
Status: focused operating supplement, single source of truth for the action-to-role matrix
Supersession:
This document is part of the active AX document set and supersedes AX_AGENT_SYSTEM_FINAL (2026-04-18) where topics overlap.
v4 supersedes v3 Deputy Owner hybrid model per Owner decision 2026-04-18.
v3 (and the patch AX_DEPUTY_OWNER_PATCH) remain as audit record in `docs/archive/patches/`.

## 1. Purpose

This document defines RBAC and availability for the AX system.
It is the canonical source for the action-to-role matrix.
Other documents must reference §5.3 instead of restating the matrix.

## 2. Availability topology stance

Working topology: single active GoClaw control-plane instance; documented rollback path; isolated legacy fallback path; no active-active multi-brain orchestration. Reliability comes first from restartability, observability, backup, and disciplined fallback.

## 3. Minimum required availability controls

Required: service healthcheck; auto-restart; reverse proxy health monitoring; config backup; daily state backup; weekly recovery drill; incident log; rollback procedure; fallback intake procedure.

## 4. Fallback decision rule

If GoClaw is unavailable for 10 minutes or more: Operator declares degraded mode; public ingress is paused or redirected; only pre-approved fallback channels are used; no new production promotion actions occur; legacy bot activation is allowed only if token/channel isolation is confirmed.

## 5. RBAC model — AI-proposer / Human-approver

### 5.1 Core design principle

Every privileged action requires a **proposer** and an **approver** who are distinct entities. In the target working model:

- **Proposer** = AI agent (Codex, Claude Code, or other automation agent)
- **Approver** = 강은구 (Owner, human)

The proposer drafts the action with full context, policy references, and expected impact. The approver reviews and permits execution. AI and human contribute **different kinds of judgment** (rule application vs. situational judgment), and together satisfy the separation-of-duties intent that self-approval rules were designed to enforce.

This replaces the Deputy Owner hybrid model (v3). The self-approval forbidden rule is replaced with the broader **proposer-approver separation rule** (§5.4).

### 5.2 Roles

Mandatory (by position, even if some are dormant in daily operation):
- Owner
- Deputy Owner (dormant — authority held but not exercised in normal operation)
- Operator
- Approver
- Requester

Optional role: Viewer (read-only).

Roles held by AI agents (not humans):
- Proposer — default role for AI agents authorized to suggest privileged actions
- Reviewer — independent AI role used in γ cross-check (§5.3) for high-risk action classes

### 5.3 Canonical action-to-role matrix

| Action class | Proposer | Reviewer (independent AI) | Approver (human) | Notes |
|---|---|---|---|---|
| request_work | human or AI | — | 강은구 or automation policy | routine intake |
| view_status | — | — | any role with read access | no approval needed |
| inspect_logs | — | — | Owner, Operator | read action |
| read_audit_log | — | — | Owner, Approver, Operator | read action |
| restart_service | AI agent or Operator | — | 강은구 | emergency restart by Operator allowed under documented runbook |
| rollback_service | AI agent or Operator | — | 강은구 | emergency rollback by Operator allowed under documented runbook |
| rotate_secret_routine (R1) | AI agent | — | 강은구 | documented procedure required |
| rotate_secret_backend_or_master (R2) | AI agent | **yes — γ gate** | 강은구 | proposer + independent reviewer + Owner approval |
| promote_automation | AI agent | — | 강은구 | proposer-approver separation automatic |
| demote_automation | AI agent | — | 강은구 | exception: active-failure containment demotion may proceed without approval and be reviewed afterward |
| change_guard_rule | AI agent | **yes — γ gate** | 강은구 | |
| change_secret_backend | AI agent | **yes — γ gate** | 강은구 | |
| retire_legacy_component | AI agent | **yes — γ gate** | 강은구 | |
| change_architecture_definition | AI agent | **yes — γ gate** | 강은구 | |

#### 5.3.1 γ gate meaning

For action classes marked γ gate in the Reviewer column:

1. A proposer AI agent drafts the change as a Pull Request with diff, rationale, and references to the active policy documents.
2. An **independent AI instance** (distinct session, distinct context, preferably different model family) reviews the PR specifically for policy conformance, do-not-resurrect list violations, scope freeze violations, schema alignment, and tenant separation impact. The reviewer posts a review comment marking the PR as pass / borderline / fail with policy citations.
3. 강은구 reviews the PR and the AI reviewer's comment, then approves or rejects.

The reviewer cannot be the proposer. The reviewer cannot be 강은구. AI agents declared to one role remain in that role for a given action to prevent collusion-by-convenience.

#### 5.3.2 Agent role assignments (working default)

- Proposer: Codex (primary executor in current session)
- Reviewer: Claude Code (independent session)

Other AI agents (n8n workflows, future automation) are added to AX_PHASE0_INVENTORY_TEMPLATE §15.5 with role declaration before granting any privileged access.

### 5.4 Proposer-approver separation rule

No action of class `promote_automation`, `demote_automation`, or any γ gate class may be both proposed and approved by the same entity.

Structurally enforced by the AI-proposer / Human-approver model: AI cannot approve, and human cannot propose privileged actions automatically without going through the proposer pipeline.

If a human directly modifies a privileged configuration bypassing the AI proposer pipeline, this counts as a **manual override** and must be logged as an audit incident by governance-audit with explicit rationale.

### 5.5 Owner-absence

Since 강은구 is the sole approver in the working model, Owner-absence means the approval pipeline is paused.

- All pending AI proposals enter a queue during Owner-absence.
- No new γ gate action may be completed.
- No R2 secret operation may be completed.
- No promote_automation or demote_automation (except active-failure containment demotion) may be completed.

Agreed response windows:
- general operations: 4 working hours
- emergency operations (active incident, security event, token collision, public-channel outage): 60 minutes
- overnight non-emergency: next working block

#### 5.5.1 Deputy Owner dormant authority

원혜연 holds Deputy Owner role formally. The authority exists on paper but is not exercised in daily operation. It is reserved for exceptional situations:

- extreme emergency where 강은구 is unreachable beyond the emergency window AND the system is in an active-failure state that cannot be contained without an approver
- documented delegation by 강은구 in advance for a defined window

Activation procedure is **pending definition** and must be decided at the first real Owner-absence scenario, then codified. Until then, Owner-absence default behavior is "queue pending proposals, no elevated activation."

This dormant state is intentional: 원혜연's primary role is business work assignment (see PHASE0 §15.1), not system governance.

#### 5.5.2 Required attributes of Owner-absence declaration

declaration ID; declared by (Owner if pre-planned; AI agent that detected unreachability with independent verification if reactive); start time; expected end time or "open-ended pending review"; trigger condition; scope; log destination (see AX_OWNER_ABSENCE_LOG_DESTINATION_POLICY).

#### 5.5.3 Post-hoc review

When 강은구 returns, every queued proposal is processed in order. Queue content is preserved in the audit log.

### 5.6 Role assignment (actual)

Confirmed 2026-04-18:
- Owner: 강은구
- Deputy Owner (dormant): 원혜연
- Approver: 강은구 (operational); 원혜연 (formal, not exercised)
- Operator: 강은구 (primary); 원혜연 (available, not primary)
- Business Work Partner: 원혜연 (work assignment accept/reject/modify flow; out of AX governance scope)

AI roles (working default, expandable per §15.5):
- Proposer: Codex
- Reviewer: Claude Code

## 6. Channel mapping principle

Casual manager chat channels: Requester only. Operator channels: Operator actions allowed. Approval channels: 강은구 exclusive for Approver actions; 원혜연 has read access for situational awareness. Owner-only admin path: secret backend, guard-rule model, legacy retirement, architecture definition change. No secret-changing action in public request channels.

Concrete channel/tool mapping must be produced in the Phase 0 inventory.

## 7. Audit rule

All non-requester privileged actions must be attributable to:
- proposer (AI agent identifier)
- reviewer if applicable (AI agent identifier)
- approver (human)
- time (proposed, reviewed, approved, executed timestamps)
- target
- action class
- result
- declaration ID if action taken under declared Owner-absence

## 8. Review rule

RBAC must be reviewed:
- on every new manager addition
- on every channel expansion
- on every new AI agent introduction (PHASE0 §15.5)
- every quarter minimum

The proposer-approver separation rule and γ gate assignments must be re-evaluated annually or when a team member is added.
