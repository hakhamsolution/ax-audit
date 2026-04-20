# AX_GUARD_FAILMODE_AND_RUNTIME_POLICY

Version: 2026-04-20 v1
Status: recovered from `똘똘이mk2` runtime evidence; sanitized live-host re-export verified on 2026-04-20
Patch record:
- v1 reconstructed from recovered guard-pack files, install scripts, and 2026-04-15 runtime audit notes

## 1. Purpose

This document defines the guard fail-open and fail-closed behavior referenced by:
- `AX_OPERATIONS_POLICY` §7
- `AX_SUPERSESSION_AND_NAMING_NOTICE` §8

This is not a new design source.
It is a recovery of the currently evidenced guard model from the `똘똘이mk2` runtime pack.

## 2. Evidence basis

- `똘똘이mk2/docs/cc-rules-pack/local/claude/CLAUDE.md`
- `똘똘이mk2/docs/cc-rules-pack/local/claude/hooks/post_tool_use/long_task_guard.py`
- `똘똘이mk2/docs/cc-rules-pack/local/claude/rules/block/003_no_sync_long_task.json`
- `똘똘이mk2/docs/cc-rules-pack/local/claude/rules/block/004_no_bg_without_log.json`
- `똘똘이mk2/docs/cc-rules-pack/local/claude/rules/warn/201_cache_ttl_boundary.json`
- `똘똘이mk2/docs/cc-rules-pack/local/claude/rules/warn/202_openclaw_no_bg.json`
- `똘똘이mk2/docs/cc-rules-pack/openclaw/AGENTS.md`
- `똘똘이mk2/docs/cc-rules-pack/openclaw/rules-engine/rules/block/001_no_sync_long_task.json`
- `똘똘이mk2/docs/cc-rules-pack/openclaw/rules-engine/rules/block/002_no_bg_without_log.json`
- `똘똘이mk2/docs/cc-rules-pack/openclaw/rules-engine/rules/warn/101_session_start_check.json`
- `똘똘이mk2/docs/cc-rules-pack/setup_claude_md.sh`
- `똘똘이mk2/scripts/server/install-claude-guard.sh`
- `똘똘이mk2/memory/2026-04-15.md`

## 3. Guard components

### 3.1 Local Claude worker plane

| Component | Current path in recovered repo | Role |
|---|---|---|
| local identity file | `docs/cc-rules-pack/local/claude/CLAUDE.md` | prompt text is not authoritative; rules/hooks/skills are authoritative |
| post-tool-use hook | `docs/cc-rules-pack/local/claude/hooks/post_tool_use/long_task_guard.py` | executes block/warn rules, scans `/tmp/cc_jobs`, sends `cmux` notifications, writes lore |
| block rules | `docs/cc-rules-pack/local/claude/rules/block/` | hard-stop high-risk execution patterns |
| warn rules | `docs/cc-rules-pack/local/claude/rules/warn/` | allow execution but attach warning and containment guidance |
| long-task skill | `docs/cc-rules-pack/local/claude/skills/long-task/SKILL.md` | required background-job pattern |
| session-recovery skill | `docs/cc-rules-pack/local/claude/skills/session-recovery/SKILL.md` | session start / reconnect recovery flow |
| cmux-integration skill | `docs/cc-rules-pack/local/claude/skills/cmux-integration/SKILL.md` | operator notification ergonomics |

### 3.2 OpenClaw plane

| Component | Current path in recovered repo | Role |
|---|---|---|
| runtime behavior guide | `docs/cc-rules-pack/openclaw/AGENTS.md` | session-start scan, long-task execution standard, reconnect rules |
| block rules | `docs/cc-rules-pack/openclaw/rules-engine/rules/block/` | hard-stop long synchronous waits and untracked background jobs |
| warn rules | `docs/cc-rules-pack/openclaw/rules-engine/rules/warn/` | warn when session restart/reconnect hygiene is skipped |
| installer | `docs/cc-rules-pack/setup_claude_md.sh` | deploys local `~/.claude` guard pack and OpenClaw rule files |
| runner hardening installer | `scripts/server/install-claude-guard.sh` | guards `run-claude` and `run-claude.raw` against direct invocation |

## 4. Runtime truth and deployment rules

### 4.1 Runtime truth

- As of the recovered 2026-04-15 audit, the live OpenClaw runtime truth was `/root/.openclaw/openclaw.json`.
- `/root/.openclaw/config/*.toml` existed but were partially stale and could not be treated as sole truth.
- `main.toml` and `routing.toml` were explicitly recorded as stale in the recovered audit notes.
- `logging.toml` also lagged reality; recovered notes say real route logs already carried `originChannel`, `returnTo`, `owner`, `reportFormat`, and `hops`.

### 4.2 Deployment surface

- Local Claude guard pack is intended for `~/.claude/`.
- OpenClaw rules are intended for `/root/openclaw/rules-engine/rules/`.
- Long-task state is standardized under `/tmp/cc_jobs/`.
- Direct use of `run-claude` and `run-claude.raw` is intended to be blocked unless the audited wrapper path is used.

### 4.3 Current confidence limit

This document is recovered from repository evidence and was cross-checked against a sanitized live-host export on 2026-04-20.
Any future session that gains host access should still prefer a fresh sanitized export of:
- `/root/.openclaw/openclaw.json`
- one representative route-log sample
- the effective runner guard install state

## 5. Fail-open / fail-closed action classes

### 5.1 Fail-closed

The following cases are evidenced as block-on-violation:

| Rule / guard | Current trigger | Enforced action | Notes |
|---|---|---|---|
| local Claude block `003_no_sync_long_task` | `sleep` long enough to imply 5+ minute synchronous wait | block | instructs conversion to `nohup + /tmp/cc_jobs/` pattern |
| local Claude block `004_no_bg_without_log` | `nohup ... &` without `/tmp/cc_jobs` log redirection and markers | block | requires log, PID file, and `.done` marker |
| OpenClaw block `001_no_sync_long_task` | 5+ minute synchronous wait in single Bash turn | block | same safety class as local Claude |
| OpenClaw block `002_no_bg_without_log` | background execution without log and `.done` marker | block | restart-safe execution requires observable markers |
| public runner hardening | direct `run-claude` invocation | exit non-zero and refuse execution | only the audited wrapper path is allowed |
| audited runner hardening | direct `run-claude.raw` invocation without wrapper context | exit non-zero and refuse execution | requires wrapper lineage plus request metadata |

### 5.2 Fail-open with warning

The following cases are evidenced as allow-with-warning or best-effort observability:

| Rule / behavior | Current trigger | Enforced action | Notes |
|---|---|---|---|
| local Claude warn `201_cache_ttl_boundary` | `sleep` at roughly 2m30s+ where cache/session risk is rising | allow + warning | tells operator to switch to background pattern before crossing the boundary |
| local Claude warn `202_openclaw_no_bg` | remote OpenClaw SSH command without `nohup` or `screen` | allow + warning | warns that the remote process may die with the SSH session |
| OpenClaw warn `101_session_start_check` | session start or reconnect without `/tmp/cc_jobs` scan | allow + warning | restart hygiene failure is warned, not immediately blocked |
| `cmux` notify path | notification send failure | allow + stderr only | observability aid; not an execution gate |
| lore write path | lore write failure | allow + stderr only | recurrence memory is best-effort in the recovered hook |

### 5.3 Borderline handling

Borderline cases must follow `AX_OPERATIONS_POLICY` §7.3-§7.4:
- do not silently bypass a warning or block with prompt text alone
- classify the event as correct block, false positive, rule ambiguity, missing context, tool misuse, model drift, or borderline case
- apply a temporary containment decision first
- require operator review
- require approver review when the action crosses a privileged boundary
- refine the rule or record an explicit exception

## 6. Operational standard implied by the recovered guard pack

- Session start or reconnect must begin with a `/tmp/cc_jobs` scan.
- Any task likely to exceed the safe synchronous boundary must move to background execution.
- Background execution must create:
  - a log file under `/tmp/cc_jobs`
  - a PID file
  - a `.done` marker
- Remote OpenClaw long tasks must not depend on an attached SSH session.
- Direct shell use of the raw/public Claude runners is not an approved execution path.

## 7. Current unresolved items

- A sanitized export of the live `/root/.openclaw/openclaw.json` is still missing from `ax-audit`.
- The current session verified the guard install markers on the host, but should not assume they remain unchanged indefinitely.
- The recovered notes indicate document/runtime drift remained present on 2026-04-15; future sessions must assume drift is still possible until re-exported.
