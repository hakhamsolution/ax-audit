# AX_ARCHITECTURE_DECISIONS

Version: 2026-04-18 v4
Status: active architecture decision record
Supersession:
This document supersedes AX_AGENT_SYSTEM_FINAL (2026-04-18).
v4 adds Decision 15 (AI-proposer / Human-approver model) and revokes Decision 14 (Deputy Owner hybrid model).

## 1. Purpose

Records decisions already made, reasons, and revisit conditions. Stops abandoned plans from silently reappearing.

## 2. Decision summary

Final direction:
- GoClaw as central control plane
- small set of core agents instead of a large swarm
- Hermes as specialist execution plane
- deterministic automation for repeated work
- runtime guard enforcement instead of static prompt-only discipline
- **AI-proposer / Human-approver model with γ gate for high-risk action classes** (Decision 15)

## 3. Decisions already made (1–5)

**Decision 1**: Do not return to an OpenClaw-centered future architecture. The target problem is multi-manager operating environment, not single-user personal assistant.

**Decision 2**: Do not preserve the previous many-agent Claude Code structure. Showed rule bypass, fragmented responsibility, handoff overhead, token duplication.

**Decision 3**: Do not let AI remain the executor of repeated deterministic work. Increases cost, reduces reproducibility, slows response, harder to trace failures.

**Decision 4**: Do not rely on static rule files alone to solve rule bypass. Already failed — rules not enforced at runtime become advisory text.

**Decision 5**: Do not run multiple equivalent central brains in parallel. Creates session conflicts, routing ambiguity, duplicated memory, unclear responsibility.

## 4. Decisions under active target state (6–9)

**Decision 6**: Use GoClaw as control plane.
**Decision 7**: Use Hermes only for specialist execution.
**Decision 8**: Reduce operational agent model to a small set of core agents.
**Decision 9**: Treat deterministic automation as a first-class layer.

## 5. Why large agent swarms were rejected

Observed/expected failure modes: rule bypass through partial context interpretation; duplicate system instructions; unclear ownership; token inflation from repeated handoff context; slower response from multi-hop routing; poor incident attribution; drift between identity files, wrappers, and shared includes.

## 6. Why "49 -> about 8" is directional, not magical

8 is a working ceiling to enforce consolidation. Real rule: one core agent per stable responsibility boundary; no duplicate responsibility zones; no agent created only for naming convenience; no specialist made public unless necessary. 7 or 9 is acceptable if proven better; drifting back into dozens of semi-overlapping agents is not.

## 7. Revisit conditions

A decision may be revisited only if: GoClaw cannot satisfy required control-plane role after practical validation; Hermes introduces unacceptable cost or latency under measured workload; deterministic automation creates more operational risk than AI-assisted handling for a specific work class; a new platform materially changes the tradeoff; measured results contradict current assumptions for two consecutive review cycles.

Any revisit must create a new ADR entry. Abandoned plans must not be reintroduced informally.

## 8. Absolute "do not resurrect" list

Do not resurrect: dozens of thin Claude Code subagents as default operating model; AI as routine executor of cron-like jobs; config-tracked secrets; equal-central parallel orchestration systems; static prompt files as sole compliance mechanism.

## 9. Current core-agent target

Working target set: hq-router; research-core; automation-dev; ops-platform; business-content; comms-admin; archive-memory; governance-audit.

Possible contraction to 7 allowed only after a review window proves archive-memory can be merged without measurable loss.

## 10. Current specialist target

vet-research-specialist; codegen-specialist; incident-specialist.

## 11. Responsibility boundary notes

**ops-platform**: preventive monitoring; platform health; deployment; service state; ordinary operational logs; backup and restore operations; ensures Guard runtime is up; monitors Guard health; restores Guard service.

**incident-specialist**: incident reproduction; hard failure diagnosis; deep failure-path analysis; fix hypothesis generation for exceptional failures; diagnoses deep Guard failure behavior; reproduces critical rule-bypass paths.

**governance-audit**: policy integrity; rule violation tracking; auditability; recurrence tracking; promotion of recurring failures into permanent rules; audit of Owner-absence declarations; **audit of proposer-approver separation compliance** (Decision 15); **audit of γ gate reviewer disagreement patterns**; audit of manual-override incidents; review of false positives and exception patterns.

**archive-memory**: knowledge curation across approved tenant scopes; memory and archive operations; enforcement of tenant boundaries per AX_DATA_TENANCY_AND_RETENTION_POLICY §11; support for retention review and deletion triggers.

## 12. Transition stance

Legacy systems may remain during migration. Tolerated for continuity, not endorsed as end state.

## 13. Root-cause hypothesis requirement for rule bypass

Guard enforcement necessary but not sufficient. Any persistent rule-bypass pattern must be classified: context-window loss; prompt-priority conflict; ambiguous or contradictory rule design; completion pressure overriding compliance; tool-surface mismatch; model drift. Repeated violations without hypothesis tracking are incomplete incident handling.

## 14. Decision 14 — Hybrid Deputy Owner authority model (REVOKED)

**Status: revoked 2026-04-18, superseded by Decision 15.**

Reason for revocation: the hybrid model assumed two Owner-class humans exercising system governance authority. In practice, 원혜연's operational strength is business work assignment, not system governance. Assigning her Deputy Owner operational authority produced form without substance (policy-active approvers who would not exercise real judgment), which is worse than no second approver.

Revocation implications:
- self-approval forbidden rule (tied to two-human structure) is replaced
- four-eyes required rule (tied to two-human structure) is replaced with γ gate (Decision 15)
- Deputy Owner role is retained formally but dormant (see AX_AVAILABILITY_AND_RBAC §5.5.1)

Original patch record: `docs/archive/patches/AX_DEPUTY_OWNER_PATCH.md` preserved for audit trail.

## 15. Decision 15 — AI-proposer / Human-approver model

Adopt AI-proposer / Human-approver separation as the working governance model.

**Components**:
- Proposer = AI agent (default: Codex)
- Approver = 강은구 (Owner, human)
- Reviewer (γ gate only) = independent AI agent (default: Claude Code)
- γ gate applies to: R2 secret operations, change_guard_rule, change_secret_backend, retire_legacy_component, change_architecture_definition
- Proposer-approver separation is structurally guaranteed (AI cannot approve; human does not auto-propose through the pipeline)
- Human direct modification bypassing the pipeline is a manual override and an audit incident
- Owner-absence queues pending proposals; no elevated Deputy activation by default

**Reason**:
- Self-approval is structurally prevented by entity separation (AI ≠ human), not by policy alone
- Two judgment layers contribute different information (AI: rule-based, Human: context-based)
- γ gate adds a second AI instance for high-risk actions, guarding against single-agent drift
- Aligns with core AX principle "AI writes it. Non-AI runs it."
- Avoids the over-engineering of the hybrid Deputy Owner model that produced form without substance

**Revisit conditions**:
- team grows to two or more humans who will genuinely exercise system governance authority (reintroduce Decision 14 variant)
- AI reviewer disagreement rate exceeds a threshold suggesting the two agents are not truly independent (collusion-by-convenience) — in which case reviewer must be re-diversified (different model family, different context, or replaced with deterministic checker)
- audit reveals that 강은구 is rubber-stamping AI proposals without substantive review (defeats the purpose) — in which case cool-off requirement is added
- measured approval queue depth during Owner-absence regularly blocks business continuity (reintroduce Deputy activation procedure)

**Patch record**: this decision is recorded in this document; no separate patch file is created.

## 16. Transition obligations from Decision 14 revocation to Decision 15 adoption

1. AX_AVAILABILITY_AND_RBAC v3 updated to v4 (matrix replaced with proposer/reviewer/approver columns).
2. AX_OPERATIONS_POLICY v4 updated to v5 (role definitions and operations clarifications updated).
3. AX_PHASE0_INVENTORY_TEMPLATE v4 updated to v5 (§15 role holders updated; §15.3 self-approval register replaced with proposer-approver register; §15.5 AI agents schema adds role declaration).
4. AX_OWNER_ABSENCE_LOG_DESTINATION_POLICY v2 updated to v3 (declaration schema adds proposer/reviewer fields; §7 clarifies queue behavior).
5. AX_SUPERSESSION_AND_NAMING_NOTICE v5 updated to v6 (version table).
6. AX_DEPUTY_OWNER_PATCH archived to `docs/archive/patches/` with status note.
7. CLAUDE.md updated (role holders, critical rules, Claude Code's own role).
8. AX_HANDOFF_TO_CLAUDE_CODE.md updated (Codex as proposer, Claude Code as reviewer).
