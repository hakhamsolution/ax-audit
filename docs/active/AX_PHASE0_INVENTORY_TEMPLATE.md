# AX_PHASE0_INVENTORY_TEMPLATE

Version: 2026-04-18 v4
Status: partially filled inventory
Patch record:
- v2 incorporated AX_DEPUTY_OWNER_PATCH (2026-04-18 v1 active)
- v3 filled §15 with confirmed values, added §15.5 (AI agents), added §15.6 (immediate follow-up actions)
- v4 finalized §15.4 with γ (two-canonical) structure confirmed

## 1. Purpose

This document is the required inventory template for Phase 0.
No migration, consolidation, promotion, or retirement decision is valid until this inventory exists in filled form.

## 2. Rule

Phase 0 is not planning.
Phase 0 is evidence collection.

If this inventory is incomplete, all downstream architecture work is provisional only.

## 3. Required outputs

The filled inventory must contain all of the following:

1. current agent inventory — pending
2. current channel ownership map — pending
3. current tool map — pending
4. current hook map — pending
5. current wrapper and script inventory — pending
6. secrets exposure list — pending
7. missing asset list — pending
8. skill-by-skill classification table — pending
9. current session-truth locations — pending
10. current fallback paths — pending
11. current approval paths — pending
12. current human operators and privileges — **filled in §15**
13. Owner-absence declaration log destination — **filled in §15.4, γ two-canonical confirmed**
14. self-approval-risk register — **filled in §15.3**

## 4. Current agent inventory

| Field | Required value |
|---|---|
| agent_id | unique current identifier |
| display_name | current human-readable name |
| current_layer | L1 / L2 / L3 / other |
| current_runtime | GoClaw / OpenClaw / Claude Code / bot / other |
| current_owner | human owner if known |
| primary_function | one-sentence real function |
| actual_inputs | what it receives |
| actual_outputs | what it produces |
| current_channels | Slack / Telegram / Discord / Web / CLI / none |
| tool_access | current tool set |
| secrets_dependency | yes / no + which |
| failure_history | known recurring failure pattern |
| target_state | keep / merge / specialist / retire / unknown |

## 5. Channel ownership map

| Channel | Current owner | Current token/bot | Purpose | Collision risk | Proposed future owner |
|---|---|---|---|---|---|
| Slack channel / ID |  |  |  | low / medium / high |  |
| Telegram chat / topic |  |  |  | low / medium / high |  |
| Discord channel |  |  |  | low / medium / high |  |
| Web / CLI path |  |  |  | low / medium / high |  |

## 6. Tool map

| Tool / integration | Current user | Purpose | Runtime | Secret dependency | Tenant sensitivity | Proposed future location |
|---|---|---|---|---|---|---|
| GitHub |  |  |  |  |  | GoClaw / runtime / legacy |
| Notion |  |  |  |  |  |  |
| Google Drive |  |  |  |  |  |  |
| Google Sheets |  |  |  |  |  |  |
| Slack |  |  |  |  |  |  |
| Telegram |  |  |  |  |  |  |
| n8n |  |  |  |  |  |  |
| Make |  |  |  |  |  |  |

## 7. Hook map

| Hook name | Current trigger point | Purpose | Fail-open or fail-closed today | Proposed future disposition |
|---|---|---|---|---|

## 8. Wrapper and script inventory

| File / script | Current path | Invoker | Function | Required secret | Criticality | Keep / rewrite / retire |
|---|---|---|---|---|---|---|

## 9. Secrets exposure list

| Secret class | Current storage location | Currently exposed in Git/history/chat | Rotation required | R1 or R2 | Target storage model |
|---|---|---|---|---|---|
| API key |  | yes / no | yes / no | R1 / R2 | SOPS+age / other |
| bot token |  | yes / no | yes / no | R1 / R2 |  |
| app token |  | yes / no | yes / no | R1 / R2 |  |
| gateway token |  | yes / no | yes / no | R1 / R2 |  |
| age key itself |  | yes / no | yes / no | R2 |  |

R1 = routine secret rotation. R2 = backend or master secret operation (includes age key).
Definitions: AX_AVAILABILITY_AND_RBAC §5.2.

## 10. Missing asset list

| Asset | Why needed | Where expected | Blocking severity | Recovery plan |
|---|---|---|---|---|
| wrapper |  |  | high / medium / low |  |
| identity file |  |  | high / medium / low |  |
| config |  |  | high / medium / low |  |

## 11. Skill-by-skill classification table

| Skill name | Current owner | Real usage | Target location | Difficulty | Dependencies | Priority | Notes |
|---|---|---|---|---|---|---|---|
| skill_x |  |  | GoClaw tool / MCP adapter / runtime job / deprecated | low / medium / high |  | P1 / P2 / P3 |  |

## 12. Session-truth locations

| System | Stores session truth? | Scope | Backup method | Recovery risk |
|---|---|---|---|---|
| GoClaw | yes / no |  |  |  |
| Claude Code | yes / no |  |  |  |
| legacy bot | yes / no |  |  |  |

## 13. Current fallback paths

| Failure case | Current fallback exists? | Trigger | Human owner | Safe? | Proposed future fallback |
|---|---|---|---|---|---|

## 14. Current approval paths

| Action | Current approver | Current method | Logged? | Self-approval possible today? | Proposed future approver |
|---|---|---|---|---|---|
| promote automation |  |  | yes / no | yes / no |  |
| demote automation |  |  | yes / no | yes / no |  |
| rotate secrets R1 |  |  | yes / no | n/a |  |
| rotate secrets R2 |  |  | yes / no | n/a |  |
| restart services |  |  | yes / no | n/a |  |
| change guard rule |  |  | yes / no | n/a |  |
| change architecture definition |  |  | yes / no | n/a |  |

## 15. Current humans and privileges — FILLED

Confirmation source: Owner decision recorded 2026-04-18.
Activation target date: 2026-04-19.

### 15.1 Canonical humans table

| Human | Current effective privileges | Formal role today | Owner / Deputy Owner / Approver / Operator eligibility | Self-approval risk note | Risk note | Proposed future role |
|---|---|---|---|---|---|---|
| 강은구 (Human X) | full — production secret store access, GoClaw host deploy/restart, Guard rule repository access, Class C·D tenant data access, automation promote/demote authority | 대표 | Owner: yes · Deputy Owner: no (cannot hold both) · Approver: yes · Operator: yes | current state: self-approval has been occurring by default because no second approver existed · from activation date: forbidden for promote_automation and demote_automation | Owner SPOF is structurally resolved by Deputy Owner assignment but actual access scope must be re-aligned per §15.6 | Owner + Approver + Operator |
| 원혜연 (Human Y) | full — production secret store access, GoClaw host deploy/restart, Guard rule repository access, Class C·D tenant data access, automation promote/demote authority | 대표 | Owner: no · Deputy Owner: yes (accepted) · Approver: yes · Operator: yes | current state: self-approval has been occurring by default · from activation date: forbidden for promote_automation and demote_automation | **current access scope is broader than the hybrid model's Deputy Owner peacetime authority; scope reduction required in Phase 1 per §15.6** | Deputy Owner + Approver + Operator |

### 15.2 Role assignment summary

- Owner: 강은구
- Deputy Owner: 원혜연
- Approver: 강은구 and 원혜연 (both, required by self-approval rule)
- Operator: 강은구 and 원혜연 (both, required for operational continuity)
- Requester: either human when proposing work they are not the approver for

Owner and Deputy Owner are two distinct humans.
Both humans hold Approver.
Both humans hold Operator.
All exit criteria in §16 related to role assignment are satisfied.

### 15.3 Self-approval risk register

| Action class | Pre-activation state (through 2026-04-18) | Post-activation state (from 2026-04-19) |
|---|---|---|
| promote_automation proposed by 강은구 | 강은구 self-approved (no alternative) | 원혜연 approves; 강은구 self-approval forbidden |
| promote_automation proposed by 원혜연 | 원혜연 self-approved (no alternative) | 강은구 approves; 원혜연 self-approval forbidden |
| demote_automation proposed by 강은구 | 강은구 self-approved | 원혜연 approves, except demotion required to contain active failure |
| demote_automation proposed by 원혜연 | 원혜연 self-approved | 강은구 approves, except demotion required to contain active failure |

Interim rule for the 2026-04-18 to 2026-04-19 gap:
- non-critical promotions paused
- demotions allowed only to contain active failure
(adopted as proposed, per Owner decision D4)

### 15.4 Owner-absence declaration log destination — CONFIRMED

Owner decision 2026-04-18: structure γ (two-canonical + two alert mirrors).

| Destination | Role |
|---|---|
| Notion database | canonical — structured |
| Git append-only file | canonical — immutable |
| Slack admin channel | alert mirror (not audit evidence) |
| Telegram | alert mirror (not audit evidence) |

Canonical consistency rule: conflict resolution by later append timestamp; discrepancies are audit incidents reviewed by governance-audit.

Full policy including schema, write path, broadcast automation phases, and dual-outage fallback: AX_OWNER_ABSENCE_LOG_DESTINATION_POLICY v2.

Automation status:
- Phase A (Notion → Git, Slack, Telegram one-way sync): target within 30 days of activation (deadline 2026-05-19)
- Phase B (two-way sync with conflict detection): target within 60 days of activation (deadline 2026-06-18)
- Interim: manual dual-canonical entry required within the sync window defined in the policy §5.2

### 15.5 AI agents and effective privileges

This subsection was added in v3 to close a gap identified while filling §15: §15 as originally scoped covered only humans, but AI agents such as Codex, Claude Code instances, and future automation agents may hold effective privileges that resemble Operator-level or Owner-level capability.

| Agent | Runtime | Effective tool access | Secret read access | Write access scope | Self-approval path possible? | Proposed future restriction |
|---|---|---|---|---|---|---|
| Codex |  |  |  |  | yes / no |  |
| Claude Code instance A |  |  |  |  | yes / no |  |
| Claude Code instance B |  |  |  |  | yes / no |  |
| n8n workflow runners |  |  |  |  | yes / no |  |
| other automation agents |  |  |  |  | yes / no |  |

Fill rule:
- every AI agent that can read any secret, write to any repository, or trigger any privileged action must appear in this table
- "self-approval path possible?" asks whether the agent could both propose and execute a privileged action without a human second-pair-of-eyes; if yes, either the agent must be restricted or a human approval gate must be inserted

This table is not yet filled.
It must be filled during Phase 0 before any AI agent is granted production-capable privilege in the new AX architecture.

### 15.6 Immediate follow-up actions from filled §15

The following actions are required as a direct consequence of filling §15.
They are tracked here because they are gap-closing work, not new design.

1. Reduce 원혜연 effective access to match Deputy Owner peacetime scope:
   - Guard rule repository: change direct-edit access to read + PR-approve access
   - production secret store: keep read access and R1 rotation capability; remove or gate R2 operation capability (backend change, age key replacement) so it requires four-eyes
   - Class C·D tenant data: verify tenancy separation per AX_DATA_TENANCY_AND_RETENTION_POLICY is enforced at storage path and credential level
2. Reduce 강은구 peacetime access for four-eyes-required actions:
   - change_guard_rule, change_secret_backend, retire_legacy_component, change_architecture_definition may not be executed by Owner alone; enforce technically where possible (e.g. PR approval requirement, two-person rule on infrastructure repository)
3. Activate self-approval forbidden rule on 2026-04-19:
   - promote_automation and demote_automation require the non-proposer as approver
   - pause non-critical promotions during the 2026-04-18 to 2026-04-19 gap
4. Establish Owner-absence declaration log per γ structure:
   - initialize Notion database with schema from AX_OWNER_ABSENCE_LOG_DESTINATION_POLICY §4
   - initialize Git append-only file at `audit/owner_absence.jsonl`
   - build Phase A automation (Notion → Git, Slack, Telegram) within 30 days
   - build Phase B automation (two-way with conflict detection) within 60 days
   - during interim, dual-canonical manual entry within sync window
5. Populate §15.5 AI agents table for every AI agent currently holding any privileged access.
6. Schedule quarterly RBAC review per AX_AVAILABILITY_AND_RBAC §8.

## 16. Exit criteria for Phase 0

Phase 0 is complete only when:
- every currently active channel has an owner — pending
- every current secret has a known storage location and an R1/R2 classification — pending
- every current critical script is inventoried — pending
- every current agent has a target-state disposition — pending
- every current skill has a target-location classification — pending
- every known missing asset has a blocking severity — pending
- token collision risks are explicitly listed — pending
- approval paths and privilege paths are written down — **partial (§15 done, §14 pending)**
- Owner and Deputy Owner are explicitly assigned to two different humans — **done (§15.2)**
- both humans are formally assigned the Approver role — **done (§15.2)**
- both humans are formally assigned the Operator role — **done (§15.2)**
- the Owner-absence declaration mechanism is documented and has a log destination in the central audit log — **done (§15.4, γ confirmed; broadcast automation pending per §15.6 item 4)**
- the self-approval-risk register is populated for every action class where the same human currently could be proposer and approver — **done (§15.3)**
- AI agents with privileged access are inventoried — pending (§15.5 template added)

## 17. Instruction to future sessions

Do not skip this document.
If someone asks for migration planning without a completed Phase 0 inventory, the correct response is to say the migration is still evidence-incomplete.

As of 2026-04-18 v4, §15 (humans) is filled, §15.3 (self-approval risk) is filled, and §15.4 (Owner-absence log destination) is confirmed as γ.
All other sections (§4–§14, §15.5) remain pending and must be populated before Phase 0 is considered complete.
