# AX_ARCHITECTURE_DECISIONS

Version: 2026-04-18 v3
Status: active architecture decision record
Supersession:
This document supersedes AX_AGENT_SYSTEM_FINAL (2026-04-18).
The earlier document is retained as historical context only and must not be used as the active design source.
v3 incorporates AX_DEPUTY_OWNER_PATCH (2026-04-18 v1 active) as Decision 14 and extends §11 boundary notes.

## 1. Purpose

This document records the decisions that are already made, the reasons they were made, and the conditions under which they may be revisited.
Its purpose is to stop abandoned plans from silently reappearing in new sessions.

## 2. Decision summary

Final direction:
- GoClaw as central control plane
- a small set of core agents instead of a large swarm
- Hermes as specialist execution plane
- deterministic automation for repeated work
- runtime guard enforcement instead of static prompt-only discipline
- hybrid Deputy Owner authority model with self-approval rule and Owner-absence declaration

## 3. Decisions already made

Decision 1.
Do not return to an OpenClaw-centered future architecture.

Reason:
The target problem is not a single-user personal assistant.
It is a multi-manager operating environment with routing, governance, and shared operational context.

Decision 2.
Do not preserve the previous many-agent Claude Code structure as the target state.

Reason:
The previous structure showed rule bypass tendencies, fragmented responsibility, increased handoff overhead, and higher token duplication.

Decision 3.
Do not let AI remain the executor of repeated deterministic work.

Reason:
Repeated AI execution increases cost, reduces reproducibility, slows response, and makes failures harder to trace.

Decision 4.
Do not rely on static rule files alone to solve rule bypass.

Reason:
This already failed.
Rules that are not enforced at runtime become advisory text.

Decision 5.
Do not run multiple equivalent central brains in parallel.

Reason:
Parallel equal-central systems create session conflicts, routing ambiguity, duplicated memory, and unclear responsibility.

## 4. Decisions under active target state

Decision 6.
Use GoClaw as control plane.

Decision 7.
Use Hermes only for specialist execution.

Decision 8.
Reduce the operational agent model to a small set of core agents.

Decision 9.
Treat deterministic automation as a first-class layer.

## 5. Why large agent swarms were rejected

Observed or expected failure modes:
- rule bypass through partial context interpretation,
- duplicate system instructions,
- unclear ownership,
- token inflation from repeated handoff context,
- slower response from multi-hop routing,
- poor incident attribution,
- drift between identity files, wrappers, and shared includes.

## 6. Why "49 -> about 8" is directional, not magical

The number 8 is not sacred.
It is a working ceiling chosen to enforce consolidation.

The real rule is:
- one core agent per stable responsibility boundary,
- no duplicate responsibility zones,
- no agent created only for naming convenience,
- no specialist made public unless necessary.

If later analysis proves that 7 or 9 is better, that is acceptable.
What is not acceptable is drifting back into dozens of semi-overlapping agents.

## 7. Revisit conditions

A decision may be revisited only if one of these conditions is met:
- GoClaw cannot satisfy the required control-plane role after practical validation,
- Hermes introduces unacceptable cost or latency under measured workload,
- deterministic automation creates more operational risk than AI-assisted handling for a specific work class,
- a new platform materially changes the architecture tradeoff,
- measured results contradict current assumptions for two consecutive review cycles.

Any revisit must create a new ADR entry.
Abandoned plans must not be reintroduced informally in chat.

## 8. Absolute "do not resurrect" list

Do not resurrect:
- dozens of thin Claude Code subagents as the default operating model,
- AI as the routine executor of cron-like jobs,
- config-tracked secrets,
- equal-central parallel orchestration systems,
- static prompt files as the only compliance mechanism.

## 9. Current core-agent target

Working target set:
- hq-router
- research-core
- automation-dev
- ops-platform
- business-content
- comms-admin
- archive-memory
- governance-audit

Possible contraction to 7 is allowed only after a review window proves that archive-memory can be merged without measurable loss.
Until that review exists, the working target remains 8.

## 10. Current specialist target

- vet-research-specialist
- codegen-specialist
- incident-specialist

## 11. Responsibility boundary notes

ops-platform:
- preventive monitoring,
- platform health,
- deployment,
- service state,
- ordinary operational logs,
- backup and restore operations,
- ensures Guard runtime is up,
- monitors Guard health,
- restores Guard service.

incident-specialist:
- incident reproduction,
- hard failure diagnosis,
- deep failure-path analysis,
- fix hypothesis generation for exceptional failures,
- diagnoses deep Guard failure behavior,
- reproduces critical rule-bypass paths.

governance-audit:
- policy integrity,
- rule violation tracking,
- auditability,
- recurrence tracking,
- promotion of recurring failures into permanent rules,
- audit of Owner-absence declarations,
- audit of self-approval rule compliance,
- audit of post-hoc Owner review execution,
- review of false positives and exception patterns.

archive-memory:
- knowledge curation across approved tenant scopes,
- memory and archive operations,
- enforcement of tenant boundaries per AX_DATA_TENANCY_AND_RETENTION_POLICY §11,
- support for retention review and deletion triggers.

## 12. Transition stance

Legacy systems may remain during migration.
They are tolerated for continuity, not endorsed as the end state.

## 13. Root-cause hypothesis requirement for rule bypass

Guard enforcement is necessary but not sufficient.
Any persistent rule-bypass pattern must be classified under one or more hypotheses:
- context-window loss,
- prompt-priority conflict,
- ambiguous or contradictory rule design,
- completion pressure overriding compliance,
- tool-surface mismatch,
- model drift.

Repeated violations without hypothesis tracking are considered incomplete incident handling.

## 14. Decision 14 — hybrid Deputy Owner authority model

Adopt hybrid Deputy Owner authority model.

Reason:
A two-person operation cannot tolerate Owner SPOF, but cannot tolerate Owner-equivalent Deputy authority either, because separation of duties collapses.
The hybrid model preserves separation in peacetime and continuity during declared Owner-absence.

Components:
- Deputy Owner is mandatory in any environment with fewer than three Owner-class humans.
- Authority is split on two axes: action risk class (single-actor allowed vs four-eyes required) and peacetime vs Owner-absence-declared.
- Owner-absence is a declared, logged state with tiered response windows (general 4 working hours, emergency 60 minutes, overnight non-emergency next working block).
- Self-approval is forbidden for promote_automation and demote_automation.
- change_architecture_definition is four-eyes required, not recommended.
- rotate_secret is split into Class R1 (routine) and Class R2 (backend or master).
- All actions taken under Owner-absence are tagged with the declaration ID in the central audit log.
- Post-hoc Owner review of "post-hoc Owner review required" actions must occur within 72 hours of Owner return.

Source of truth:
The canonical action-to-role matrix lives in AX_AVAILABILITY_AND_RBAC §5.3.
This document does not restate the matrix.

Revisit conditions:
- team grows to three or more Owner-class humans (re-evaluate Deputy Owner mandatory status),
- measured Owner-absence frequency or duration exceeds the working assumption for two consecutive review cycles,
- audit shows that the post-hoc Owner review path is not being executed,
- audit shows repeated self-approval violations,
- response window tiers prove unworkable under measured incident frequency.

Patch record:
Adopted from AX_DEPUTY_OWNER_PATCH (2026-04-18 v1 active).
