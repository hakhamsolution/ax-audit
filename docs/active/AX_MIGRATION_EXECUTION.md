AX MIGRATION EXECUTION
Version: 2026-04-18 v2
Status: target-state migration execution guide
Supersession:
This document supersedes AX_AGENT_SYSTEM_FINAL (2026-04-18).
The earlier document is retained as historical context only and must not be used as the active design source.

1. Purpose

This document explains how to move from the current known structure into the target AX structure without reintroducing abandoned plans.

2. Current known state from legacy docs

Known facts from the legacy handoff and migration documents:
- the old L1 migration scope was OpenClaw gateway to GoClaw gateway,
- current inventory included 21 agents, 57 skills, 38 bindings, and 4 hooks,
- L2 Claude Code assets and L3 Telegram bot were treated as runtime-independent and retained during that migration plan,
- secrets exposure had already occurred in old tracked config/history,
- Telegram token collisions between systems were already identified as a real risk,
- the GoClaw config schema was noted as potentially unstable versus copied OpenClaw structure,
- some L2 wrappers and identity assets were not fully collected.

These facts mean the target migration is not a greenfield rebuild.
It is a controlled restructuring of a live system.

3. Migration stance

Do not perform a big-bang rewrite.
Do not try to preserve the old many-agent logic as-is.
Do not destroy legacy assets before replacement stability is proven.

Migration should happen in four tracks:
- control-plane replacement,
- agent consolidation,
- deterministic automation extraction,
- legacy retirement.

4. Phase plan

Phase 0. Freeze and inventory
Required outputs:
- current agent inventory,
- current channel ownership map,
- current tool map,
- current hooks map,
- current wrappers and scripts inventory,
- secrets exposure list,
- missing assets list,
- skill-by-skill classification table.

The skill-by-skill classification table must include:
- current skill name,
- target location: GoClaw tool / MCP adapter / deterministic runtime job / deprecated,
- migration difficulty: low / medium / high,
- dependencies,
- migration priority.

Phase 1. Safe control plane establishment
- establish GoClaw as the target L1 control plane,
- centralize ingress design,
- define session truth ownership,
- keep legacy components isolated by token and channel,
- validate healthchecks, restart, fallback, and rollback.

Phase 2. Core agent consolidation
- classify old agents by responsibility boundary,
- fold overlapping roles into the target core set,
- move heavy specialist work into Hermes,
- document every old-to-new mapping,
- do not preserve persona proliferation.

Phase 3. Automation extraction
- identify repeated tasks currently done by AI,
- generate deterministic scripts or workflows,
- move them into GitHub Actions, cron, systemd, or n8n,
- implement promotion and demotion reviews,
- define review cadence, review owner, review artifact, and failure thresholds.

Phase 4. Guard activation
- enable runtime guard components,
- classify failure causes,
- block violations,
- tune false positives,
- convert repeated failures into permanent policy.

Phase 5. Legacy retirement
- retire only what has a stable replacement,
- remove dead bindings and wrappers,
- keep an audit trail of what was removed and why.

5. Required migration artifacts

Must exist:
- current-state inventory file
- old-to-new mapping table
- channel ownership table
- token ownership table
- secret rotation checklist
- baseline metrics file
- rollback checklist
- retirement checklist
- supersession notice for deprecated design docs

6. Mandatory old-to-new mapping table

6.1 Structural mapping

Old: OpenClaw L1
New: GoClaw control plane

Old: Claude Code many-subagent L2
New: consolidated core agents plus Hermes specialists

Old: repeated AI execution
New: deterministic automation runtime

Old: legacy bots as ad hoc routing
New: isolated temporary legacy processes pending retirement

6.2 Working responsibility mapping

General routing / managerial intake -> hq-router
Research / literature / analysis -> research-core
Repeated automation / scripts / workflow generation -> automation-dev
Deployment / infra / logs / service state -> ops-platform
Business copy / content / campaign operations -> business-content
Email / message / admin handling -> comms-admin
Knowledge curation / memory / archive -> archive-memory
Policy / audit / rule integrity / review -> governance-audit

Heavy veterinary reasoning -> vet-research-specialist
Complex code generation -> codegen-specialist
Difficult incident reproduction and diagnosis -> incident-specialist

7. Explicitly forbidden during migration

Forbidden:
- recreating dozens of thin agents because names feel useful,
- copying old config secrets into tracked target config,
- letting Hermes become public ingress,
- letting multiple systems answer the same channel with the same role,
- promoting automation without review artifacts,
- assuming old wrappers are safe without inventory and validation,
- calling the migration complete before metrics baseline and stabilization reviews exist.

8. Completion gates

Migration is not complete until all are true:
- GoClaw is the active control plane,
- a consolidated core-agent set is active,
- Hermes specialists are wired only for specialist work,
- deterministic runtime owns the majority of repeated tasks,
- secret storage is remediated,
- metrics baseline and first review cycle exist,
- at least one legacy component retirement decision has been formally made,
- rollback path is still documented and tested.

9. Final instruction to future sessions

If you are a new session or a different LLM:
- do not revive the abandoned large-agent architecture,
- do not propose AI-first repeated execution,
- do not propose secret-bearing tracked configs,
- do not assume “final” means unchangeable,
- but do require explicit evidence before revisiting any rejected plan.

The intended direction is stable.
Revisions are allowed only through documented evidence, not through drift.
