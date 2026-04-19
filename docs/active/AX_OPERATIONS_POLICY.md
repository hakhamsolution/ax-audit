# AX_OPERATIONS_POLICY

Version: 2026-04-18 v4
Status: mandatory operating policy
Supersession:
This document supersedes AX_AGENT_SYSTEM_FINAL (2026-04-18).
The earlier document is retained as historical context only and must not be used as the active design source.
v4 incorporates AX_DEPUTY_OWNER_PATCH (2026-04-18 v1 active).

## 1. Purpose

This document defines how the AX system is operated in practice.
It covers availability, roles, secrets, automation lifecycle, guard enforcement, and measurement.

The action-to-role matrix is not restated in this document.
The canonical matrix lives in AX_AVAILABILITY_AND_RBAC §5.3.
This document references the matrix and defines operations-policy-specific clarifications only.

## 2. Availability policy

### 2.1 Single control plane acknowledgment
GoClaw is the intended single control plane.
This creates a deliberate single-control dependency.

### 2.2 Minimum service objective
Until a stricter target is approved, the working availability target is:
- monthly GoClaw availability SLO: 99.5 percent
- maximum tolerated public-ingress outage per incident: 30 minutes
- maximum tolerated degradation before fallback decision: 10 minutes

### 2.3 Recovery objectives
Working targets:
- RPO for control-plane state backup: 24 hours maximum
- RTO for standard GoClaw recovery: 60 minutes maximum
- RTO for degraded fallback intake path: 15 minutes maximum

### 2.4 Fallback policy
If GoClaw is unavailable:
- new public work intake is paused or redirected,
- direct uncontrolled fallback to Hermes is forbidden,
- a designated legacy bot may be temporarily activated only if it is isolated by channel and token,
- recovery status must be visible to operators,
- no production automation promotion decisions are allowed in degraded mode.

### 2.5 Baseline required availability controls
Required baseline controls:
- healthcheck endpoint monitoring
- service auto-restart
- config backup
- daily state backup
- incident log
- rollback procedure

Additional required controls are defined in AX_AVAILABILITY_AND_RBAC §3 and should be treated as the stronger profile where both documents apply.

## 3. Roles and permissions

Five mandatory roles plus one optional read-only role are recognized.

Mandatory:
- Owner
- Deputy Owner
- Operator
- Approver
- Requester

Optional:
- Viewer

Deputy Owner is mandatory in any environment with fewer than three Owner-class humans.

Authority for each role is defined by the canonical action matrix in AX_AVAILABILITY_AND_RBAC §5.3.

## 4. Action-to-role mapping

The canonical action-to-role mapping is defined in AX_AVAILABILITY_AND_RBAC §5.3.
This document does not restate the matrix.

Operations-policy-specific clarifications:
- actions tagged "four-eyes required" in the matrix may not be performed by a single actor in peacetime, even if that actor is Owner.
- actions tagged "post-hoc Owner review required" in the matrix may proceed during declared Owner-absence and must be reviewed and ratified or reversed by Owner within 72 hours of return.
- self-approval is forbidden for promote_automation and demote_automation regardless of role. See AX_AVAILABILITY_AND_RBAC §5.4.
- Owner-absence is a declared, logged state. See AX_AVAILABILITY_AND_RBAC §5.5.

## 5. Secret operations authority

Secret operations are split into two classes:

- Class R1 — routine secret rotation
- Class R2 — backend or master secret operation

Definitions and authority are in AX_AVAILABILITY_AND_RBAC §5.2 and §5.3.

Operations clarifications:
- R1 rotations may be executed by Owner, Deputy Owner, or Operator if and only if a documented rotation procedure exists for that secret and the action is logged.
- R2 operations are four-eyes required in peacetime and post-hoc Owner review required during declared Owner-absence.
- An R1 rotation that incidentally requires changing the secret backend or master path is reclassified as R2 and must follow R2 authority.

## 6. Secrets policy

### 6.1 Forbidden
Forbidden:
- secrets committed to Git,
- secrets embedded in tracked JSON or Markdown config,
- secrets duplicated across multiple uncontrolled files.

### 6.2 Required
Required:
- one chosen secret system for canonical storage,
- runtime injection at deploy time,
- rotation procedure,
- access logging where possible.

### 6.3 Canonical choice
Default recommended choice for this environment:
SOPS + age

Reason:
- Git-friendly for infrastructure repos,
- low operational weight compared with Vault,
- fits self-hosted and VPS-centered workflows,
- does not force a new SaaS dependency.

Allowed exception:
A deliberate switch to Doppler or 1Password CLI is a Class R2 operation.
It may be made only by four-eyes Owner-plus-Deputy-Owner decision and must update this policy.

Local `.env.local` is allowed only on the server or runtime host and must not be committed.

## 7. Guard policy

### 7.1 Runtime enforcement is mandatory
The system must enforce policy after execution planning and after tool use.
Prompt text alone is insufficient.

### 7.2 Guard components
Required:
- post-tool-use hook
- regex and structural validator
- policy validator
- violation blocker
- failure classifier
- recurrence memory

### 7.3 False positive handling
Every blocked action must be classified as:
- correct block,
- false positive,
- rule ambiguity,
- missing context,
- tool misuse,
- model drift,
- borderline case.

### 7.4 Borderline handling
Borderline cases must not silently bypass policy.
They require:
- temporary containment decision,
- operator review,
- approver review if needed,
- rule refinement or explicit exception ruling.

Detailed Guard failmode policy is defined in AX_GUARD_FAILMODE_AND_RUNTIME_POLICY.

## 8. Automation lifecycle policy

### 8.1 Promotion criteria
A task may be promoted when:
- inputs are stable,
- rules are explicit,
- expected outputs are bounded,
- failure handling is known,
- dry-run passes,
- an approver authorizes activation,
- the approver is not the proposer (self-approval rule).

### 8.2 Demotion criteria
A task must be demoted when one or more apply:
- failure rate exceeds threshold for the review window,
- business rules changed materially,
- human override frequency becomes too high,
- output ambiguity increased,
- deterministic recovery logic no longer covers real cases.

### 8.3 Review cadence
Every promoted automation must be reviewed:
- after 7 days,
- after 30 days,
- monthly thereafter if still active and production-critical.

### 8.4 Review ownership
- automation-dev prepares evidence,
- governance-audit reviews policy and recurrence implications,
- Approver makes the promote/demote decision, subject to the self-approval rule defined in AX_AVAILABILITY_AND_RBAC §5.4,
- Owner arbitrates unresolved disputes.

### 8.5 Review artifacts
Every review must produce:
- decision outcome,
- measured failure rate,
- manual override count,
- cost note if relevant,
- keep / modify / demote action,
- link to incident notes if any.

## 9. Runtime platform policy

Default deterministic runtime priority:
1. GitHub Actions for repo-bound workflows
2. cron or systemd timer for host-bound jobs
3. n8n as default workflow orchestrator
4. Make only by exception when there is a clear connector or maintenance advantage
5. webhook or queue workers for event-driven execution

The system should not maintain n8n and Make as equal-first platforms.

## 10. Metrics policy

Architecture success must be measured.

### 10.1 Required baseline metrics
- average input tokens per request
- p50 latency
- p95 latency
- average handoff count
- percentage of repeated work still handled by AI
- rule violation detection count
- false positive block count
- MTTR
- monthly manual rework time
- Owner-absence declaration count and duration
- post-hoc Owner review backlog count

### 10.2 Every metric must have
- baseline value
- target value
- measurement method
- review interval

No success claim is allowed without baseline and review data.

## 11. Incident policy

Every critical failure must produce:
- incident summary,
- affected layer,
- root-cause classification,
- containment action,
- permanent corrective action,
- whether the failure should become a guard rule or a demotion trigger.

Detailed incident severity tiering should be defined in a future incident response document.

## 12. Documentation policy

Any structural change must update:
- definitions,
- decision record,
- operations policy,
- migration execution plan,
- availability and RBAC document if the change affects roles, authority, or matrix entries.

Architecture may not drift through chat-only decisions.
