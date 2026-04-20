# AX_OPERATIONS_POLICY

Version: 2026-04-18 v5
Status: mandatory operating policy
Supersession:
This document supersedes AX_AGENT_SYSTEM_FINAL (2026-04-18).
v5 supersedes v4 Deputy Owner hybrid model per Owner decision 2026-04-18.

## 1. Purpose

Defines how the AX system is operated in practice: availability, roles, secrets, automation lifecycle, guard enforcement, and measurement.

The action-to-role matrix is not restated here. Canonical matrix lives in AX_AVAILABILITY_AND_RBAC §5.3.

## 2. Availability policy

### 2.1 Single control plane
GoClaw is the intended single control plane. This creates a deliberate single-control dependency.

### 2.2 Minimum service objective
- monthly GoClaw availability SLO: 99.5 percent
- maximum tolerated public-ingress outage per incident: 30 minutes
- maximum tolerated degradation before fallback decision: 10 minutes

### 2.3 Recovery objectives
- RPO for control-plane state backup: 24 hours maximum
- RTO for standard GoClaw recovery: 60 minutes maximum
- RTO for degraded fallback intake path: 15 minutes maximum

### 2.4 Fallback policy
If GoClaw is unavailable: new public work intake is paused or redirected; direct uncontrolled fallback to Hermes is forbidden; a designated legacy bot may be temporarily activated only if isolated by channel and token; recovery status must be visible to operators; no production automation promotion decisions are allowed in degraded mode.

### 2.5 Baseline required availability controls
Baseline: healthcheck endpoint monitoring; service auto-restart; config backup; daily state backup; incident log; rollback procedure. Additional controls in AX_AVAILABILITY_AND_RBAC §3 as stronger profile.

## 3. Roles and permissions

Roles recognized:

Mandatory human roles:
- Owner (operational): 강은구
- Deputy Owner (dormant): 원혜연 — authority held formally, not exercised in daily operation
- Operator: 강은구 primary, 원혜연 available
- Approver: 강은구 operational, 원혜연 formal
- Requester: either human when proposing work

Optional: Viewer.

Business-side role (out of AX governance scope):
- Business Work Partner: 원혜연 — receives work assignments, accepts/rejects/modifies; separate from system governance flow

AI roles:
- Proposer: AI agent that drafts privileged actions (default: Codex)
- Reviewer: independent AI agent used in γ gate cross-check (default: Claude Code)

Authority for each role per AX_AVAILABILITY_AND_RBAC §5.3.

## 4. Action-to-role mapping

Canonical matrix: AX_AVAILABILITY_AND_RBAC §5.3.

Operations-policy-specific clarifications:
- Every privileged action requires a proposer and an approver who are **distinct entities**. AI proposes; 강은구 approves.
- γ gate action classes (R2 secret ops, change_guard_rule, change_secret_backend, retire_legacy_component, change_architecture_definition) additionally require an independent AI reviewer's conformance check before 강은구 approval.
- Active-failure containment demotion is the sole exception to the approval flow — may proceed without approval but must be reviewed afterward.
- Human direct modification of privileged configuration bypassing the proposer pipeline counts as manual override and is an audit incident.

## 5. Secret operations authority

Split into two classes per AX_AVAILABILITY_AND_RBAC §5.2:
- Class R1 — routine rotation (bot/app/API tokens with documented procedure)
- Class R2 — backend or master operation (secret backend change, master encryption path change, age key replacement)

Operations clarifications:
- R1 rotations: AI agent proposes; 강은구 approves; execution by 강은구 or Operator runbook.
- R2 operations: γ gate (AI proposer + independent AI reviewer + 강은구 approval).
- An R1 rotation that incidentally touches the secret backend or master path is reclassified as R2 and must follow the γ gate.

## 6. Secrets policy

### 6.1 Forbidden
- secrets committed to Git
- secrets embedded in tracked JSON or Markdown config
- secrets duplicated across multiple uncontrolled files

### 6.2 Required
- one chosen secret system for canonical storage
- runtime injection at deploy time
- rotation procedure
- access logging where possible

### 6.3 Canonical choice
Default: SOPS + age. Reason: Git-friendly for infrastructure repos; low operational weight compared with Vault; fits self-hosted and VPS-centered workflows; does not force a new SaaS dependency.

Allowed exception: a deliberate switch to Doppler or 1Password CLI is a Class R2 operation requiring γ gate and must update this policy.

Local `.env.local` is allowed only on the server or runtime host and must not be committed.

## 7. Guard policy

### 7.1 Runtime enforcement
System must enforce policy after execution planning and after tool use. Prompt text alone is insufficient.

### 7.2 Guard components
Post-tool-use hook; regex and structural validator; policy validator; violation blocker; failure classifier; recurrence memory.

### 7.3 False positive handling
Every blocked action classified as: correct block; false positive; rule ambiguity; missing context; tool misuse; model drift; borderline case.

### 7.4 Borderline handling
No silent bypass. Requires temporary containment decision; operator review; approver review if needed; rule refinement or explicit exception ruling.

Detailed Guard failmode in AX_GUARD_FAILMODE_AND_RUNTIME_POLICY.

## 8. Automation lifecycle policy

### 8.1 Promotion criteria
Inputs stable; rules explicit; outputs bounded; failure handling known; dry-run passes; proposer drafts; 강은구 approves. Proposer-approver separation is automatic since proposer is AI and approver is human.

### 8.2 Demotion criteria
Demote when: failure rate exceeds threshold for review window; business rules changed materially; human override frequency too high; output ambiguity increased; deterministic recovery logic no longer covers real cases.

### 8.3 Review cadence
After 7 days, 30 days, monthly thereafter if production-critical.

### 8.4 Review ownership
automation-dev prepares evidence; governance-audit reviews policy and recurrence implications; 강은구 makes the promote/demote decision as Approver; Owner arbitrates unresolved disputes.

### 8.5 Review artifacts
Decision outcome; measured failure rate; manual override count; cost note if relevant; keep / modify / demote action; link to incident notes if any.

## 9. Runtime platform policy

Default deterministic runtime priority:
1. GitHub Actions for repo-bound workflows
2. cron or systemd timer for host-bound jobs
3. n8n as default workflow orchestrator
4. Make only by exception when there is a clear connector or maintenance advantage
5. webhook or queue workers for event-driven execution

System should not maintain n8n and Make as equal-first platforms.

## 10. Metrics policy

### 10.1 Required baseline metrics
Average input tokens per request; p50 latency; p95 latency; average handoff count; percentage of repeated work still handled by AI; rule violation detection count; false positive block count; MTTR; monthly manual rework time; Owner-absence declaration count and duration; proposal queue depth during Owner-absence; γ gate reviewer disagreement rate.

### 10.2 Every metric must have
Baseline value; target value; measurement method; review interval. No success claim allowed without baseline and review data.

## 11. Incident policy

Every critical failure must produce: incident summary; affected layer; root-cause classification; containment action; permanent corrective action; whether the failure should become a guard rule or a demotion trigger.

Detailed incident severity tiering in a future incident response document.

## 12. Documentation policy

Any structural change must update: definitions; decision record; operations policy; migration execution plan; availability and RBAC document if the change affects roles, authority, or matrix entries.

Architecture may not drift through chat-only decisions.
