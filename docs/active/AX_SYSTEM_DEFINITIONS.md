AX SYSTEM DEFINITIONS
Version: 2026-04-18 v2
Status: active authoritative definitions
Supersession:
This document supersedes AX_AGENT_SYSTEM_FINAL (2026-04-18).
The earlier document is retained as historical context only and must not be used as the active design source.

1. Purpose

This document defines the canonical terms for the AX system so that a new session, operator, or LLM can reason from the same vocabulary without hidden memory.

2. System objective

The AX system is not a generic chatbot stack.
It is an operating system for execution across:
- veterinary research,
- Hakam Solution operations,
- Abel operations.

Its purpose is:
- to accept requests from multiple managers,
- to preserve shared operational context,
- to route work to the correct execution layer,
- to move repeated work out of AI and into deterministic automation,
- to reduce rule bypass, token waste, handoff overhead, and recovery time.

Core principle:
AI writes it. Non-AI runs it.

3. Definitions

3.1 GoClaw
GoClaw is the central control plane and gateway.
It is responsible for:
- public channel ingress,
- session source of truth,
- routing,
- approval flow,
- audit traces,
- policy enforcement entrypoint,
- tool and integration hub.

GoClaw is not where all work should be executed.
GoClaw decides, routes, tracks, and governs.

3.2 Hermes
Hermes is the specialist execution plane.
It is used for:
- long-context research,
- memory-heavy analysis,
- complex code generation,
- difficult exception analysis,
- recovery support for hard failures.

Hermes is not the public ingress.
Hermes should not own public channels in the target architecture.

3.3 Core agent
A core agent is a stable responsibility boundary under GoClaw.
A core agent exists only when:
- the work class is recurring,
- the responsibility is clearly distinct,
- the decision boundary is stable,
- merging it would reduce clarity or increase failure risk.

A core agent must not exist only because a named persona is convenient.

3.4 Specialist
A specialist is a narrow execution role used for heavy or exceptional work.
Specialists are invoked.
They are not expanded into a public-facing swarm.

3.5 Legacy bot
A legacy bot is an already-running independent process that may remain in service during migration.
Legacy bots are not the architectural future state.
They are retained only while replacement risk is higher than retention cost.

3.6 Automation Runtime Plane
This is the deterministic execution layer for repeated work.
Examples:
- cron,
- systemd timer,
- GitHub Actions,
- n8n,
- Make only by exception,
- webhook workers,
- queue workers,
- cloud jobs.

This layer executes repeatable work without requiring an LLM at runtime.

3.7 Guard Layer
The Guard Layer is the runtime enforcement and diagnostic layer that prevents rule bypass.
It contains:
- post-tool-use validation,
- regex and structural policy checks,
- violation blocking,
- failure classification,
- forced context injection where needed,
- memory of recurrent failure patterns.

3.8 Promotion
Promotion means moving a task from AI-assisted execution into deterministic runtime execution.

3.9 Demotion
Demotion means moving a task back from deterministic runtime execution into AI-assisted handling because the task is no longer stable enough for deterministic execution.

3.10 Session source of truth
The canonical record of task state, routing context, and decision history.
Target state: GoClaw owns this.

3.11 Availability fallback
A defined degraded-mode or alternate execution path used when the control plane is unavailable.

3.12 RBAC
Role-based access control.
The minimal required model for multi-manager operation.

4. Layers

L0: Automation Runtime Plane
Runs repeated work.

L1: GoClaw control plane
Owns ingress, routing, traceability, approval, and governance.

L2: Core agents
Own recurring responsibility zones.

L2-S: Hermes specialists
Handle heavy and exceptional work.

L3: Legacy bots
Temporary parallel processes retained only when needed.

5. What the system is not

It is not:
- a swarm of dozens of lightly differentiated agents,
- a structure where AI directly performs every repeated task,
- a design where every channel talks to a different brain,
- a system that relies on static rule files alone for compliance,
- a stack where secrets live in config tracked by Git.

6. Canonical target state

GoClaw
-> core agents
-> Hermes specialists
-> Automation Runtime Plane
-> optional isolated legacy bots

7. Non-negotiable constraints

- Public ingress must be centralized.
- Session truth must be singular.
- Repeated work must leave AI whenever feasible.
- Rule compliance must be enforced at runtime, not requested politely.
- Core agent count must stay low.
- Secrets must never live in tracked configuration files.

8. Canonical names

Active core-agent target names:
- hq-router
- research-core
- automation-dev
- ops-platform
- business-content
- comms-admin
- archive-memory
- governance-audit

Active specialist target names:
- vet-research-specialist
- codegen-specialist
- incident-specialist

Reason:
The system objective explicitly includes veterinary research as a first-class domain.
Therefore the research specialist remains veterinary-specific by default.
