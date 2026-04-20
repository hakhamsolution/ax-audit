# AX_PHASE0_MIGRATION_ARTIFACTS

Version: 2026-04-20 v5
Status: Phase 0 execution artifact; mk2 runtime evidence, live credential-layout proof, GitHub remote bootstrap, and GitHub platform-gate evidence incorporated

## 1. Purpose

This file collects the migration artifacts that AX_MIGRATION_EXECUTION §5 requires to exist during Phase 0.
It is an execution companion, not a new policy source.

## 2. Old-to-new mapping table

### 2.1 Structural mapping

| Old structure | New structure | Current evidence | Execution status |
|---|---|---|---|
| OpenClaw L1 | GoClaw control plane | OpenClaw is still the live L1 in recovered evidence | blocked until Phase 1 |
| Claude Code many-subagent L2 | consolidated core agents + Hermes specialists | current inventory shows 38 Claude workers and 10 Codex OAuth majors | mapped in inventory; execution blocked until Phase 2 |
| repeated AI execution | deterministic automation runtime | n8n, cron, systemd, heartbeat jobs already exist in part | extraction plan prepared; production promotion blocked |
| legacy bots as ad hoc routing | isolated temporary legacy processes pending retirement | Telegram archive/ingress path still exists | isolation documented; retirement not yet approved |

### 2.2 Responsibility mapping

| Current responsibility | Target owner |
|---|---|
| General routing / managerial intake | `hq-router` |
| Research / literature / analysis | `research-core` |
| Repeated automation / scripts / workflow generation | `automation-dev` |
| Deployment / infra / logs / service state | `ops-platform` |
| Business copy / content / campaign operations | `business-content` |
| Email / message / admin handling | `comms-admin` |
| Knowledge curation / memory / archive | `archive-memory` |
| Policy / audit / rule integrity / review | `governance-audit` |
| Heavy veterinary reasoning | `vet-research-specialist` |
| Complex code generation | `codegen-specialist` |
| Difficult incident reproduction and diagnosis | `incident-specialist` |

## 3. Channel ownership table

This condensed table mirrors the live ingress/admin surfaces from `AX_PHASE0_INVENTORY_TEMPLATE` §5.

| Surface | Current owner | Current credential holder | Target owner |
|---|---|---|---|
| Telegram manager groups (`ABEL`, `은혜`) | `main` / `jarvis` | shared Telegram bot token | `hq-router` only |
| Slack `#000-대표-똘똘이` (`C0ASNEFES4C`) | `main`, approval workflow, heartbeat escalation | shared Slack app/bot token | `hq-router` + human approvers |
| Slack `#003-간부회의` (`C0ASGQQFP8W`) | `main` + 13 team leads | shared Slack app/bot token | consolidated core-team leads |
| Slack `#999-컨퍼런스` (`C0ASM1RBWBX`) | `main` + 13 team leads | shared Slack app/bot token | consolidated core-team leads |
| Slack department channels (13 recovered IDs in inventory §5) | department team leads | shared Slack app/bot token | canonical department owners after runtime export |
| Gateway UI | OpenClaw `main` | gateway token | `hq-router` only |
| trusted CLI wrappers | approved team leads | host-local runner auth | approved team leads only |

## 4. Token ownership table

This resolves the inventory gap that previously named the token ownership manifest as missing.

| Token / credential class | Current runtime dependency | Current effective custodian | Intended owner role | Isolation / collision risk | Rotation class | Current blocker |
|---|---|---|---|---|---|---|
| gateway token | OpenClaw ingress / Gateway UI | Owner + Deputy Owner shared | Owner-managed with Approver oversight | medium | R1 | live runtime path is known, but console-level custody proof/export is not captured |
| Slack bot/app tokens | Slack ingress, reports, alerts | Owner + Deputy Owner shared | Owner-managed with Operator use | high | R1 | live runtime confirms one shared Slack bot token + one shared Slack app token; app-admin custody proof and isolated AX token set are still missing |
| Telegram bot token | Telegram ingress and alert mirror | Owner + Deputy Owner shared | Owner-managed with Operator use | high | R1 | live runtime confirms one shared Telegram bot token across both manager groups; bot-admin custody proof and isolated AX bot binding are still missing |
| Notion integration token | Notion canonical + ops DBs | Owner + Deputy Owner shared | Owner-managed with limited operator use | medium | R1 | exact integration ownership record not exported |
| Google OAuth / app credentials | Drive/Docs/Sheets/Slides actions | Owner + Deputy Owner shared | Owner-managed with limited operator use | medium | R1 | live connection inventory missing |
| GitHub app / PAT / deploy credentials | repo write, CI, workflow ops | Owner + Deputy Owner shared | Owner-managed with Approver oversight | medium | R1 | canonical remote is initialized, but branch-protection is plan-gated for this private repo and Actions execution is billing-gated until account settlement |
| Codex OAuth runner auth (`~/.codex/auth.json`) | trusted Codex OAuth majors | approved team leads on trusted host | Operator-held runner auth, no broad secret-store role | low | R1 | trusted-runner host inventory not exported |
| future SOPS age key | secret backend replacement | not yet deployed | γ gate custody model (AI proposal + independent AI review + 강은구 approval) | medium | R2 | backend not yet migrated |

## 5. Secret rotation checklist

- [x] Major secret classes identified and classified into R1/R2.
- [x] Historical exposure risk recorded in inventory/backlog.
- [x] Target storage model set to `SOPS + age` for migrated secrets.
- [x] Sanitized live runtime credential-layout export captured from production runtime.
- [ ] Slack token collision isolated by dedicated AX app/token set.
- [ ] Telegram token collision isolated by dedicated AX bot/chat binding.
- [ ] Notion / Google / GitHub integration owners documented from live console.
- [ ] R1 rotation executed and logged.
- [ ] R2 backend custody and procedure executed under γ gate.

## 6. Rollback checklist

Use this checklist before any control-plane or automation promotion:

1. Export the current runtime configuration and channel/token bindings.
2. Confirm the current canonical stores (`Notion`, `audit/owner_absence.jsonl`) are readable.
3. Capture a pre-change metrics snapshot from `AX_PHASE0_BASELINE_METRICS.md`.
4. Record the approver and proposer separately.
5. Keep the old ingress/token path live until the replacement passes validation.
6. If validation fails, demote the new path, restore the previous routing/token binding, and log the incident.
7. Verify both canonical stores still agree after rollback.

## 7. Retirement checklist

No legacy component may be retired unless every item below is satisfied:

- [ ] stable replacement exists and is documented
- [ ] rollback path has been tested
- [ ] channel collision risk is zero or explicitly accepted by approver
- [ ] secrets tied to the retired component are rotated or destroyed
- [ ] audit trail records what was retired, when, and by whose approval

Current retirement candidates:

| Candidate | Replacement requirement | Current status |
|---|---|---|
| legacy Telegram ingress overlap | isolated `hq-router` ingress | blocked |
| ad hoc Make automations | n8n / deterministic runtime | blocked |
| unvetted wrapper paths | inventoried trusted wrappers only | partially ready |
| persona-proliferated thin agents | consolidated core-agent set | blocked until Phase 2 |

## 8. Remaining blockers

- `AX_GUARD_FAILMODE_AND_RUNTIME_POLICY.md` has been recovered from mk2 evidence and key guard install markers were verified on the live host.
- The exact historical 57-skill manifest is still missing, but later `90 -> 65` mapping evidence exists and current-state classification no longer depends on the historical count.
- Slack/Telegram live runtime now proves shared platform-level credentials, but console-level custody proof and isolated AX credential sets are still missing.
- Branch-protection and reviewer-enforcement proof are still missing; branch-protection APIs return `403 Upgrade to GitHub Pro or make this repository public` for this private repo on 2026-04-20, so the remaining blocker is now a hosting-plan gate rather than repo bootstrap.

## 9. Sanitized runtime snapshot (2026-04-20)

Remote verification was performed directly on Contabo host `5.182.17.93` as `root`.
Only non-sensitive metadata is recorded below.

### 9.1 Runtime truth files

| Path | Observed state |
|---|---|
| `/root/.openclaw/openclaw.json` | present; `size=29717`; `mtime=2026-04-16 21:07:22 +0200` |
| `/root/.openclaw/config/main.toml` | present but older than `openclaw.json`; `mtime=2026-04-11 18:25:03 +0200` |
| `/root/.openclaw/config/routing.toml` | present but older than `openclaw.json`; `mtime=2026-04-11 18:24:50 +0200` |
| `/root/.openclaw/config/logging.toml` | present; `mtime=2026-04-15 14:49:37 +0200` |
| `/root/.openclaw/logs/route_logs/2026-04-15.jsonl` | present; `size=2489`; `mtime=2026-04-15 19:33:54 +0200` |

Interpretation:
- `openclaw.json` is confirmed present on the live host and is newer than the key TOML files.
- This matches the recovered 2026-04-15 audit note that `openclaw.json` is the runtime truth and the TOML files may be stale.

### 9.2 Live channel and binding evidence

| Surface | Live evidence |
|---|---|
| Telegram `ABEL` | group id `-1003286171878`; confirmed in live cron/job messages as `Telegram 그룹 'ABEL'` |
| Telegram `은혜그룹` | group id `-1003881200687`; confirmed in live cron/job messages as `Telegram 그룹 '은혜그룹'` |
| Telegram topic evidence | `은혜그룹` config includes topic `92` as an archive topic; cron session keys also reference topic `1` for archive runs |
| Telegram route binding | live `openclaw.json` binding routes Telegram channel traffic to `main` |
| Slack key bindings | live `openclaw.json` bindings align with recovered key Slack channel IDs such as `C0ASNEFES4C`, `C0ASGQQFP8W`, `C0ASM1RBWBX` |

### 9.3 Guard install evidence

| Path | Live marker check |
|---|---|
| `/usr/local/bin/run-claude` | contains `OPENCLAW_CLAUDE_PUBLIC_GUARD=1` |
| `/usr/local/bin/run-claude.raw` | contains `OPENCLAW_CLAUDE_AUDITED_GUARD=1` |

### 9.4 Route-log schema evidence

The live route-log file exists and sample entries were observed with:
- camelCase keys: `originChannel`, `returnTo`, `owner`, `reportFormat`, `hops`
- snake_case variants also coexist in some entries

This confirms the recovered audit note that actual route logs are richer than the stale `logging.toml` description.

### 9.5 Credential-layout evidence

| Surface | Sanitized finding |
|---|---|
| Slack runtime credentials | exactly one `botToken` occurrence and one `appToken` occurrence were observed under `root.channels.slack`; no per-channel Slack token split was observed |
| Telegram runtime credentials | exactly one `botToken` occurrence was observed under `root.channels.telegram`; no per-group Telegram token split was observed |

Interpretation:
- current live runtime is using shared platform-level Slack and Telegram credentials rather than isolated AX-only channel-specific credentials
- this resolves the evidence gap about the live binding shape, but it does not satisfy the intended isolation target

## 10. GitHub platform-gate evidence (2026-04-20)

| Surface | Observed result |
|---|---|
| GitHub Actions manual run | `owner-absence-validate` workflow runs `24640809639` and `24642505500` were both created, but the jobs did not start and GitHub reported: `The job was not started because recent account payments have failed or your spending limit needs to be increased.` |
| Branch-protection API | `gh api repos/hakhamsolution/ax-audit/branches/main/protection` returned `403 Upgrade to GitHub Pro or make this repository public to enable this feature.` |
| Rulesets API | `gh api repos/hakhamsolution/ax-audit/rulesets` returned the same `403 Upgrade to GitHub Pro or make this repository public to enable this feature.` |

Interpretation:
- GitHub Actions runtime is currently blocked by billing/account payment state, not by the workflow YAML shape
- repository-level branch protection for this private repo is currently blocked by the active GitHub plan
