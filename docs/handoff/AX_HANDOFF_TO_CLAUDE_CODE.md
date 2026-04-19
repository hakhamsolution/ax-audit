# AX_HANDOFF_TO_CLAUDE_CODE

Version: 2026-04-18 v1
Status: execution handoff to Claude Code
Audience: Claude Code agent taking over execution for Work Blocks 1 through 5

This document is not a new policy. It is an execution launcher that consolidates the end-to-end plan, KPIs, and human-in-the-loop gates for the remaining AX Phase 0 cycle.

## 0. Handoff state at 2026-04-20

### 0.1 최초 실행 계획 요약 (핵심만)

- WB1-B: `ax-audit` 레포 내 `audit/owner_absence.jsonl` 초기 구조 생성
- WB1-C: Notion DB `AX 소유자 부재 신고` 생성 또는 수동 생성 후 스키마 v1.0 검증
- WB1-C Gate: Notion API로 스키마 확인(`--verify`)은 API 가시성 이슈 시 Notion UI 수동 검증으로 전환
- WB1 완료 조건: Track A/B/C 3개 트랙 완료 + K3/K4 흡수 완료

### 0.2 2026-04-20 기준 진행 상태

- `backlog.md` 상태
  - `operational_bookmarks.notion_database_id`는 `421644f9-3db4-4f18-b50e-b6e35c019f25`로 최신화됨.
  - `newly_discovered_gates`에 Notion API 가시성 제한 및 수동 검증 필요 메시지가 누적됨.
- 실행 산출물
  - `Makefile`에 `notion-dry`, `notion-verify`, `notion-create` 추가됨.
  - `scripts/init_notion_owner_absence_db.py`는 `--verify`에서 `live properties are not visible via this integration context.` 수신 시 수동 판독 가이드를 출력하도록 설계됨.
- 직전 수행 결과 요약
  - `make notion-create`를 통해 Notion DB 생성은 성공 (`AX 소유자 부재 신고`, id `421644f9-3db4-4f18-b50e-b6e35c019f25`).
  - 동일 DB 대상 `make notion-verify`는 API로는 속성 목록 노출이 제한되어 `inconclusive`/수동판독 필요로 종료됨.
- 다음 인수인계 액션(우선순위)
  - 1) Notion UI에서 DB 전체 속성 펼침 확인: `declaration_id`~`last_updated_at` v1.0 열 모두 존재 여부
  - 2) 필요 시 수동으로 6개 추천 뷰 생성(스키마 문서 §4.3)
  - 3) 액세스 권한 확인(원혜연 Full, Approver Read)
  - 4) 확인 결과를 `backlog.md`에 `cycle_log` 및 `newly_discovered_gates`로 마지막 확정

---

## 1. Mission

Close Phase 0 and stand up the two Owner-absence canonicals so the hybrid authority model activated on 2026-04-19 is backed by real infrastructure, not just policy text.

Scope ends at KPI satisfaction in §3. Phase 1 (control plane establishment) is a separate cycle and is **out of scope**.

## 2. Hard scope rules

1. Do not author new policy documents.
2. Do not extend schemas. A schema change is a four-eyes action; do not initiate one.
3. Do not re-open closed decisions (Deputy Owner model, rotate_secret R1/R2 split, γ two-canonical structure, Owner-absence response windows). These are recorded in the active document set; reference them rather than revising them.
4. Improvements discovered during execution go to `backlog.md` as a single line and are not worked on in this cycle.
5. If a Work Block exposes a genuine blocker that cannot be resolved without policy revision, stop and surface it to a human. Do not invent a policy patch.

## 3. KPIs — this cycle ends when all four are true

| KPI | Current | Target | Measurement |
|---|---|---|---|
| K1 PHASE0 §16 exit criteria done | 5 of 14 | 14 of 14 | direct checklist verification |
| K2 DEPUTY_OWNER_PATCH §8 activation checklist done | 9 of 16 | 16 of 16 | direct checklist verification |
| K3 Phase A automation (Notion → Git, Slack, Telegram) working | not built | built + verified with a real test declaration | `OA-20260419-000` test declaration triggers all three mirrors within the sync window |
| K4 Dual-canonical write path verified end-to-end | not verified | verified | a declaration written in either canonical appears in the other within sync window |

Until all four read "done", this cycle is open. When all four read "done", stop. Do not continue improving.

## 4. Active role holders and Claude Code's position

Humans:
- Owner: 강은구
- Deputy Owner: 원혜연
- Approver: 강은구, 원혜연
- Operator: 강은구, 원혜연

Claude Code:
- is an AI agent with effective Operator-level privilege
- may execute bash, git, and API calls on behalf of a human
- is NOT a human and cannot close any four-eyes or self-approval gate
- is subject to inventory entry in `AX_PHASE0_INVENTORY_TEMPLATE.md` §15.5

Permission rule for Claude Code in this cycle:
- if a task's authority matrix row says single-actor allowed → Claude Code may execute on human's direction
- if the row says four-eyes required → Claude Code prepares the change as a PR/proposal and waits for two humans to approve in writing
- if the row says no-self-approval → Claude Code checks the proposer and blocks if proposer equals approver

Reference for the matrix: `docs/active/AX_AVAILABILITY_AND_RBAC.md` §5.3.

## 5. Active document map

Read on every session:
- `CLAUDE.md` (project root, auto-loaded)
- `docs/active/AX_SUPERSESSION_AND_NAMING_NOTICE.md` (version truth table)
- `docs/active/AX_AVAILABILITY_AND_RBAC.md` (authority matrix, Owner-absence semantics, self-approval rule)
- `docs/active/AX_PHASE0_INVENTORY_TEMPLATE.md` (§16 exit criteria, §15.6 follow-up items)

Consult when the task domain matches:
- secrets, automation lifecycle, metrics, runtime platform → `docs/active/AX_OPERATIONS_POLICY.md`
- tenant separation, data classes, retention → `docs/active/AX_DATA_TENANCY_AND_RETENTION_POLICY.md`
- guard fail-open/fail-closed, borderline handling → `docs/active/AX_GUARD_FAILMODE_AND_RUNTIME_POLICY.md` *(recovered on 2026-04-20 from `똘똘이mk2` evidence and cross-checked against live host guard markers; full wrapper export is still pending)*
- Owner-absence log structure, broadcast automation, dual-outage fallback → `docs/active/AX_OWNER_ABSENCE_LOG_DESTINATION_POLICY.md`
- Owner-absence field schema, validation rules → `docs/active/AX_OWNER_ABSENCE_LOG_SCHEMA_DESIGN.md`
- architectural do-not-resurrect list, core-agent target, ADR 14 → `docs/active/AX_ARCHITECTURE_DECISIONS.md`
- definitions of GoClaw, Hermes, core agent, specialist, layers → `docs/active/AX_SYSTEM_DEFINITIONS.md`
- migration phase plan → `docs/active/AX_MIGRATION_EXECUTION.md`

Patch record (for audit, not for runtime decisions):
- `docs/archive/patches/AX_DEPUTY_OWNER_PATCH.md`

## 6. Repository layout assumption

This handoff assumes the following layout in an `ax-audit` (or equivalent) Git repository:

```
<repo-root>/
├── CLAUDE.md
├── backlog.md
├── docs/
│   ├── active/
│   │   ├── AX_SYSTEM_DEFINITIONS.md            (v2, legacy .txt pending conversion — see WB1 note)
│   │   ├── AX_ARCHITECTURE_DECISIONS.md        (v3)
│   │   ├── AX_OPERATIONS_POLICY.md             (v4)
│   │   ├── AX_MIGRATION_EXECUTION.md           (v2, legacy .txt pending conversion — see WB1 note)
│   │   ├── AX_AVAILABILITY_AND_RBAC.md         (v3)
│   │   ├── AX_PHASE0_INVENTORY_TEMPLATE.md     (v8)
│   │   ├── AX_GUARD_FAILMODE_AND_RUNTIME_POLICY.md (v1)
│   │   ├── AX_DATA_TENANCY_AND_RETENTION_POLICY.md (v1)
│   │   ├── AX_OWNER_ABSENCE_LOG_DESTINATION_POLICY.md (v2)
│   │   ├── AX_OWNER_ABSENCE_LOG_SCHEMA_DESIGN.md (v1)
│   │   └── AX_SUPERSESSION_AND_NAMING_NOTICE.md (v8)
│   ├── handoff/
│   │   └── AX_HANDOFF_TO_CLAUDE_CODE.md
│   └── archive/
│       ├── AX_AGENT_SYSTEM_FINAL_2026-04-18.md
│       └── patches/
│           └── AX_DEPUTY_OWNER_PATCH.md
├── audit/
│   ├── owner_absence.jsonl                     (created in WB1)
│   ├── owner_absence.schema.json               (created in WB1)
│   └── README.md                               (created in WB1)
└── scripts/
    ├── init_owner_absence_log.sh
    └── init_notion_owner_absence_db.py
```

Note: `AX_SYSTEM_DEFINITIONS.md` and `AX_MIGRATION_EXECUTION.md` currently exist only as .txt files (v2). If these are placed in `docs/active/` as .md, the content is unchanged — only the extension converts.

## 7. Work blocks

### WB1 — Activation readiness

**Deadline**: today (2026-04-18) or tomorrow before activation timestamp.

**Purpose**: make the Owner-absence declaration mechanism real before the hybrid authority model goes live; surface any currently-exposed secrets.

**Track A — Secrets exposure scan**
- Human input needed: list of AX-adjacent repositories to scan.
- Actions Claude Code may take:
  - run `git log --all -p` filtered by regex for secret-like strings in each named repo
  - inspect `.env*` files (but do not print their contents to chat; report presence and suspicious patterns only)
  - propose a secrets inventory table to be filled into `AX_PHASE0_INVENTORY_TEMPLATE.md` §9
- Human action required:
  - confirm whether exposed secrets (if any) are live
  - decide R1/R2 classification per secret
  - authorize rotation (R1: Operator; R2: four-eyes)
- Success: §9 populated with every detected secret, R1/R2 classified, rotation status recorded.

**Track B — Git canonical initialization**
- Human input needed: target repository (create `ax-audit` or use an existing repo).
- Actions Claude Code may take:
  - create the repo directory structure per §6
  - run `scripts/init_owner_absence_log.sh` from the repo root
  - stage and commit on a feature branch
  - open a PR with 강은구 as proposer
- Human action required:
  - 원혜연 reviews and approves the PR (first live self-approval-rule exercise)
  - 강은구 does NOT approve their own PR
- Success: `audit/owner_absence.jsonl`, `audit/owner_absence.schema.json`, `audit/README.md` merged to main via PR reviewed by the non-proposer.

**Track C — Notion canonical initialization**
- Human input needed: Notion parent page, Notion integration token, access list.
- Actions Claude Code may take:
  - run `scripts/init_notion_owner_absence_db.py --dry-run` to show payload
  - run the script for real once the human provides token via env var
  - verify schema parity with `--verify --database-id <id>`
- Alternatively, the human may create the Notion database manually; Claude Code then runs `--verify` to confirm parity.
- Human action required:
  - provide `NOTION_TOKEN` (never commit, never log)
  - provide parent page ID
  - after DB creation, manually configure the six recommended views from `AX_OWNER_ABSENCE_LOG_SCHEMA_DESIGN.md` §4.3
  - grant access to 원혜연 (Full) and any Approvers (Read)
- Success: Notion DB exists with all schema properties aligned; views exist; access is granted; DB ID recorded in `backlog.md` under `operational_bookmarks`.

**WB1 completion gate** — all three:
- Track A: §9 populated and any exposed secret has a rotation plan
- Track B: PR merged, first self-approval-rule exercise succeeded
- Track C: Notion DB created and schema-verified
- End-to-end smoke test: declaration `OA-20260419-000` written to both canonicals, verified visible in Slack/Telegram alerts (manual in interim, automated in WB5), ratified immediately as a test record

### WB2 — Access realignment

**Deadline**: 2026-04-21.

**Purpose**: close PHASE0 §15.6 items 1 and 2. Technical access must match the policy authority matrix.

**Steps**:
1. Identify every repository, secret store, and data path where either 강은구 or 원혜연 currently has direct write access that the peacetime authority matrix does not grant.
2. For each gap, propose a specific access change (e.g. "change 원혜연's role on the `<repo>` from Admin to Write, add branch protection requiring PR approval"). Present the list for human review.
3. After human approval, execute the access reductions. Record before/after in `backlog.md` under `access_realignment_log`.
4. Verify that four-eyes-required actions (R2, change_guard_rule, change_secret_backend, retire_legacy_component, change_architecture_definition) can no longer be executed by a single actor on the infrastructure.

**Human input needed**:
- confirmation of current access listing (Claude Code inventories, human verifies)
- approval of proposed reductions
- execution of access changes may require Owner/Deputy Owner action depending on the platform

**Success**: §15.6 items 1 and 2 marked done in `AX_PHASE0_INVENTORY_TEMPLATE.md`. Spot check: 강은구 attempts a change_guard_rule locally and the PR cannot be merged without 원혜연's review.

### WB3 — Current-state inventory

**Deadline**: 2026-04-25.

**Purpose**: fill `AX_PHASE0_INVENTORY_TEMPLATE.md` §4, §5, §6, §7, §8, §10, §12, §13, §14, §15.5.

**Strategy**: a single inventory pass per section. Use the known facts from `AX_MIGRATION_EXECUTION.md` §2 as the starting point (21 agents, 57 skills, 38 bindings, 4 hooks from legacy handoff).

**Sections in priority order**:
1. §5 channel ownership map — Slack channels, Telegram chats, Discord (if any), CLI paths; flag token collision risks
2. §12 session-truth locations — where task state actually lives today
3. §4 agent inventory — one row per currently-running agent; target_state per row
4. §6 tool map — GitHub, Notion, Google Drive, Google Sheets, Slack, Telegram, n8n, Make
5. §7 hook map — 4 hooks from legacy handoff
6. §8 wrapper and script inventory — any wrapper/identity files
7. §10 missing asset list — populated from §4–§8 gaps
8. §13 fallback paths — current fallback for each failure case
9. §14 approval paths — current approver for each privileged action
10. §15.5 AI agents — Codex, Claude Code instances, n8n runners, anything with effective privilege

**Human input needed**:
- confirmations for items Claude Code cannot verify remotely (actual bot tokens in use, current operator passwords, etc. — never echoed to chat)
- decisions on target_state per agent (keep / merge / specialist / retire)

**Success**: §16 exit criteria entries for §4–§15 all read "done".

### WB4 — Skill classification

**Deadline**: 2026-05-02.

**Purpose**: classify each of the 57 skills (per legacy handoff) into target locations (GoClaw tool / MCP adapter / runtime job / deprecated).

**Strategy**: table-driven. One row per skill. Difficulty, dependencies, priority assigned during classification.

**Human input needed**:
- decisions on ambiguous skills (keep or deprecate)
- priority overrides where Claude Code's suggestion conflicts with operational knowledge

**Success**: `AX_PHASE0_INVENTORY_TEMPLATE.md` §11 fully populated. K1 KPI reaches 14 of 14.

### WB5 — Phase A automation

**Deadline**: 2026-05-19 per `AX_OWNER_ABSENCE_LOG_DESTINATION_POLICY.md` §6.2.

**Purpose**: replace manual dual-canonical entry with automated broadcast Notion → Git, Slack, Telegram.

**Architecture** (per the policy §6.1):
- Notion webhook triggers on new or updated row in the `AX Owner Absence Declarations` database
- an n8n workflow (or GitHub Action, depending on which is more reliable for the webhook path) receives the webhook
- the workflow validates the record against `owner_absence.schema.json`
- on valid record: appends JSONL line to `audit/owner_absence.jsonl`, posts to Slack admin channel, posts to Telegram
- on schema failure: alerts operator, does not sync

**Steps**:
1. Design the n8n workflow (or GitHub Action) on paper first; show to human for review.
2. Build in a sandbox. Use test declaration IDs `OA-SANDBOX-NNN` that are purged before production.
3. Dry run with a fabricated test record.
4. Promote to production via the authority matrix's `promote_automation` row — Approver is the non-proposer (self-approval rule).
5. First real production test: declaration `OA-20260519-001` (or whenever the first real declaration occurs) must propagate to all three mirrors within the sync window.

**Human input needed**:
- Notion integration permissions for webhook subscription
- Slack bot/webhook setup
- Telegram bot token (treat as secret)
- promote_automation approval (self-approval forbidden)

**Success**: K3 KPI reaches "built + verified". Manual dual-canonical entry is no longer the operating procedure.

## 8. Human-in-the-loop gates — consolidated

| Gate | Who decides | When | How it is logged |
|---|---|---|---|
| WB1-B PR approval | 원혜연 (proposer: 강은구) | before merge | PR review record |
| WB1-C Notion integration token provisioning | 강은구 or 원혜연 | before script run | not logged in repo (secret handling) |
| WB2 access reduction approval | 강은구 | before each change | `backlog.md` under `access_realignment_log` |
| WB3 agent target_state decisions | 강은구 and 원혜연 (joint review) | per session | inline in §4 table |
| WB4 skill classification edge cases | 강은구 | per item | inline in §11 table |
| WB5 promote_automation for Phase A | 원혜연 or 강은구 (whichever did not propose) | before production | declaration log with declaration_id |

Any other gate discovered during execution: stop, surface, and record in `backlog.md` under `newly_discovered_gates`. Do not invent authority.

## 9. Reporting format

At the end of every Work Block, post (to the Slack admin channel or directly to the humans) a short report:

```
WB<n> status: <done | blocked | partial>
KPIs moved: <K1 5→6, K2 9→11, ...>
Human input pending: <list or "none">
Blockers: <list or "none">
Next: WB<n+1> or "cycle complete"
```

Do not continue to the next Work Block automatically if there are unresolved human-input items or blockers.

## 10. Cycle completion

When all four KPIs (§3) are "done":
1. Run one final consistency check: `AX_PHASE0_INVENTORY_TEMPLATE.md` §16 exit criteria all "done"; `AX_DEPUTY_OWNER_PATCH.md` §8 activation checklist all "done"; K3 and K4 verified by a real declaration flow.
2. Append a cycle-closed note to `backlog.md` with timestamp and KPI snapshot.
3. Post cycle-complete report.
4. Do not start Phase 1 (control plane establishment) in the same conversation. Phase 1 is a new cycle requiring new scope definition, fresh human approval, and potentially a new handoff document.

## 11. What to do when in doubt

In priority order:

1. Check the active document set (§5 of this file).
2. Check this handoff for an explicit rule.
3. If still ambiguous, stop and ask a human. Do not fill the gap by inferring a new policy.
4. If the human gives an answer that contradicts the active document set, flag the contradiction explicitly and wait for confirmation before acting.

## 12. Anti-patterns to avoid

- proposing to add a new `.md` file "to clarify things"
- merging policy documents because you notice overlap
- updating a document version number without a corresponding policy change
- treating a single human's instruction as four-eyes approval
- silently deferring a pending KPI item by marking it done-with-asterisk
- starting Phase 1 work because WB5 feels close to done
- revisiting a closed decision (see §2.3) without human initiation
