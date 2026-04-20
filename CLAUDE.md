# CLAUDE.md

AX system audit + migration repository. Read this every session.

## Project identity

This repository hosts the AX operating system for:
- veterinary research workspace
- Hakam Solution operations
- Abel (에이블) operations

AX is a multi-manager execution environment, not a chatbot stack. Core principle: **AI writes it. Non-AI runs it.**

## Current state (2026-04-18)

Phase 0 is partially filled. Policy is complete. Governance model is **AI-proposer / Human-approver (Decision 15)**, active from 2026-04-19. Many implementation items are pending.

Full plan: `docs/handoff/AX_HANDOFF_TO_CLAUDE_CODE.md`. Read it before starting any task.

## Role holders (humans)

- Owner: 강은구 (operational — all system management and approval)
- Deputy Owner (dormant): 원혜연 (formal authority, not exercised in daily operation)
- Approver: 강은구 (operational); 원혜연 (formal, dormant)
- Operator: 강은구 (primary); 원혜연 (available)
- Business Work Partner: 원혜연 (work assignment accept/reject/modify — out of AX governance scope)

Authority matrix: `docs/active/AX_AVAILABILITY_AND_RBAC.md` §5.3. Single source of truth.

## Role holders (AI agents)

- Proposer (default): **Codex** — drafts privileged actions as PRs with diff, rationale, policy references
- Reviewer (default, γ gate only): **Claude Code** — independent AI instance reviewing γ gate actions for policy conformance

Other AI agents must be declared in `docs/active/AX_PHASE0_INVENTORY_TEMPLATE.md` §15.5 with a single primary role (proposer / reviewer / neither) before gaining privileged access.

## Core governance model — Decision 15

Every privileged action requires a **proposer** and an **approver** who are distinct entities.

- Proposer = AI agent
- Approver = 강은구
- For γ gate classes (R2 secret ops, change_guard_rule, change_secret_backend, retire_legacy_component, change_architecture_definition): additional independent AI **reviewer** required before 강은구 approves

Proposer-approver separation is structurally guaranteed (AI cannot approve; 강은구 does not auto-propose through pipeline).

## If you are an AI agent reading this

Your role is **proposer** by default unless specifically deployed as a reviewer. You may:
- read source files, run analyses, draft proposals
- execute bash, git, and API calls on behalf of 강은구
- open pull requests for 강은구 to review

You may NOT:
- act as Approver for any privileged action
- execute a γ gate action without a distinct reviewer AI's policy check **and** 강은구's approval
- mark your own proposal as approved
- declare Owner-absence on your own (verification required — see Owner-absence policy)
- treat 강은구's verbal instruction as "self-approval" — the pipeline still applies

When 강은구 gives you an instruction, your job is to **propose the action as a PR**, not to execute it directly. 강은구's instruction is a request to propose, not an approval.

If asked to perform an action whose matrix row shows γ gate, stop and require:
1. a separate AI reviewer's independent policy check
2. 강은구's explicit written approval on the PR

## Critical rules (full list in active docs)

1. **Proposer-approver separation**: proposer and approver are distinct entities. AI cannot approve. Direct human modification bypassing the pipeline is manual override and an audit incident.
2. **γ gate**: for R2 secret, change_guard_rule, change_secret_backend, retire_legacy, change_architecture_definition — proposer AI + independent reviewer AI + 강은구 approver.
3. **Owner-absence queues proposals**: 강은구 unreachable = approval pipeline paused. Dormant Deputy (원혜연) not activated by default. Queue resumes on 강은구's return.
4. **Secrets never in Git**. SOPS+age default. `.env.local` host-only.
5. **Tenant separation mandatory**. Do not mix client data across tenants without documented exception. Class D (healthcare, tax, legal) stricter handling.
6. **Guard layer fail-closed** for: secret-changing, production promotion, destructive, cross-tenant write, policy change, legacy retirement, legal/regulated-data actions.
7. **Do not resurrect**: many-subagent swarm; AI as routine executor of cron-like jobs; config-tracked secrets; equal-central parallel orchestration; static prompt files as sole compliance; **Deputy Owner hybrid model (revoked by Decision 15)**.
8. **Do not collapse two canonicals** (Notion + Git) for Owner-absence log into one; do not treat four destinations as equivalent.
9. **No new policy documents**. New schemas, new frameworks, new roles require Owner decision via ADR, not this cycle.

## Scope freeze

This cycle's scope is WB1 through WB5 in the handoff document. Do not propose new policies, new design documents, or new schemas. Improvements discovered go into `backlog.md` as one-line entries; not picked up this cycle.

## Entry point

Read `docs/handoff/AX_HANDOFF_TO_CLAUDE_CODE.md` and follow the work block it prescribes.

## Reference map

Always current: `docs/active/AX_SUPERSESSION_AND_NAMING_NOTICE.md` lists active documents and versions.

For canonical vocabulary, role authority, or single source of truth: check supersession notice §8 first.
