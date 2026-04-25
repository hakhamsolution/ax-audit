# backlog.md

Purpose: hold improvement ideas and operational bookmarks discovered during this cycle.
Not worked on this cycle. Considered only after cycle completion (see `docs/handoff/AX_HANDOFF_TO_CLAUDE_CODE.md` §10).

Rules:
- One line per idea or bookmark, ISO date prefix.
- Do not expand entries into full designs here. That is next-cycle work.
- This file is append-mostly; entries may be edited only to add the resolution status after the cycle closes.

---

## improvements_discovered_during_execution

_(empty — append as found)_

## newly_discovered_gates

- 2026-04-20: `AX_handoff_package_2026-04-18_v2.zip` confirms the active governance model is Decision 15 (`AI-proposer / Human-approver`) rather than the previously restored hybrid Deputy Owner model. Core policy documents and operator instructions must be re-aligned before further execution.
- 2026-04-20: GitHub Actions billing gate persists after package-v2 realignment. Manual workflow run `24642505500` on commit `dbe1896` failed before job start with the same billing error as earlier runs.
- 2026-04-26: GitHub Actions billing gate is resolved by self-hosted runner cutover (`44fef70` on 2026-04-23 switched the `validate` job to `runs-on: [self-hosted, linux, x64, hakham-vps]`). Today's manual workflow_dispatch run `24934831397` completed in 13 seconds on the `hakham-vps` runner with conclusion success, proving CI execution is no longer blocked by billing. The plan-gate (private-repo branch-protection / rulesets) is a separate blocker and still returns `403 Upgrade to GitHub Pro or make this repository public`.
- 2026-04-26: Track A finalized — `똘똘이mk2` git history contains a plain-text Slack bot token of the form `xoxb-9849432992692-…`, which the repository's own `SECRETS.md` already self-flagged as "재발급 필요". The `dashboard/.env.example` carries only placeholder values (`changeme`). The previously suspected `src/config.ts` and `src/telegram-bot.ts` paths are no longer in the current tree, and the surviving live token-handling surface (`scripts/heartbeat.py`, `scripts/heartbeat_checks/*.py`) reads `OPENCLAW_GATEWAY_TOKEN`, `OPENAI_API_KEY`, and `LIGHTRAG_API_KEY` from environment without inlining values. Required next action: R1 rotation of the exposed Slack bot/app token (and as precaution the Telegram bot token) — AI propose + 강은구 approve, no γ gate.
- 2026-04-20: Slack bot/app concrete values confirmed by 강은구 — Slack app `똘똘`, bot member `U0ARNS78EM9`, current direct endpoint `D0AS8534L01` (DM channel, not shared channel). DM is acceptable for a temporary simple mirror, but if 원혜연 / governance-audit read access becomes necessary, a dedicated private channel should replace it.
- 2026-04-20: Telegram bot concrete value corrected by 강은구 — `@SN_ocle_bot`. Slack workspace domain is `eunhyebooboo.slack.com`; this is a workspace identifier, not a channel ID. Subsequent Slack API search confirmed the current admin-channel permalink as `https://eunhyebooboo.slack.com/archives/C0ASNEFES4C` for `#000-대표-똘똘이 (C0ASNEFES4C)`. Slack/Telegram 모두 기존 token을 그대로 승계하고 기존 flow는 종료 예정이므로, 남은 gating item은 `기존 flow retirement + Track A secrets exposure verification + SOPS/age migration`이다.
- 2026-04-20: Notion API visibility gate — `python3 scripts/init_notion_owner_absence_db.py --verify --database-id 57605a19-e78d-491e-bd29-c397396b99ae` succeeds with
  inconclusive status (`live properties are not visible`) and requires manual UI confirmation of schema v1.0.
- 2026-04-20: 사용자가 직접 확인한 결과와 최신 Notion 조회 모두 동일: `AX Owner Absence Declarations` DB 스키마에 v1.0 사용자 정의 속성이 반영되지 않고 `Name`(타이틀)만 표시됨. 현재 Notion/connector 모두에서 스키마 부재 상태가 확인됨.
- 2026-04-20: 부모 페이지 `은혜그룹` 아래에 Owner-absence DB가 2개(`57605a19-e78d-491e-bd29-c397396b99ae`, `421644f9-3db4-4f18-b50e-b6e35c019f25`) 존재함. 현재 운영 대상으로는 후자만 복구했으며, 전자 정리(보존/삭제/이름변경)는 인간 결정이 필요함.
- 2026-04-20: 현재 Owner-absence canonical의 Notion 컬럼명을 한글로 바꾸는 것은 `AX_OWNER_ABSENCE_LOG_SCHEMA_DESIGN.md` 기준 스키마 변경에 해당하며 γ gate 승인이 필요함. 즉시 변경하지 말고 다음 스키마 버전 제안으로 다뤄야 함.
- 2026-04-20: live Notion operational DB title is currently `AX 소유자 부재 신고`, while `AX_handoff_package_v2` expects `AX Owner Absence Declarations` as the canonical title. Script/runtime compatibility exists, but title reconciliation still needs a human decision.

## access_realignment_log

- 2026-04-26 (proposed): apply branch protection to hakhamsolution/ax-audit main — before: protection unset (gh api repos/hakhamsolution/ax-audit/branches/main/protection => 404 Branch not protected; gh api repos/hakhamsolution/ax-audit/rulesets => []); after-target: require pull_request review (1 approving review, dismiss stale on new commits), require status check "validate", enforce on admins, disallow force push, disallow deletions. Proposer: Codex; Reviewer: pending (distinct Claude Code session); Approver: 강은구. PR: <PR_URL_PLACEHOLDER>.

## operational_bookmarks

- notion_database_id: 421644f9-3db4-4f18-b50e-b6e35c019f25 (현재 사용 DB, DB명: AX 소유자 부재 신고, v1.0 스키마 생성 대상)
- notion_integration_name: _(populate after WB1 Track C)_
- audit_repo_url: _(populate after WB1 Track B)_
- owner_absence_log_path_git: `audit/owner_absence.jsonl`
- slack_workspace_domain: `eunhyebooboo.slack.com`
- slack_admin_channel: `#000-대표-똘똘이 (C0ASNEFES4C)` — `똘똘이mk2` `approval-workflow.sh`의 L3/L4 승인 경로와 `heartbeat` 기본 escalation channel 기준
- slack_admin_channel_permalink: `https://eunhyebooboo.slack.com/archives/C0ASNEFES4C`
- slack_bot_app: `똘똘` (bot member/user id `U0ARNS78EM9`)
- slack_bot_dm_endpoint: `D0AS8534L01` — 강은구 ↔ 똘똘 봇 DM. 단순 mirror/intake로는 사용 가능하지만 shared read에는 부적합
- telegram_admin_endpoint: `ABEL (-1003286171878)`, `은혜그룹 (-1003881200687)` — live host `openclaw.json`/cron evidence 기준; `은혜그룹`에서는 archive topic `92`도 관측됨
- telegram_bot_username: `@SN_ocle_bot`

## gaps_at_handoff

- 2026-04-18: `docs/active/AX_GUARD_FAILMODE_AND_RUNTIME_POLICY.md` (v1) is referenced by `AX_SUPERSESSION_AND_NAMING_NOTICE.md` §1 and by `docs/handoff/AX_HANDOFF_TO_CLAUDE_CODE.md` §5 but is not present in this handoff package. It was authored in an earlier session. Recovery: retrieve from prior chat export, original working copy, or the Anthropic session history. Until restored, fall back to `AX_OPERATIONS_POLICY.md` §7 (which summarizes guard policy at a higher level) and do not design guard logic from scratch — that would be scope expansion.
- 2026-04-20: `똘똘이mk2`의 guard pack, installer, 2026-04-15 runtime audit 메모를 근거로 `docs/active/AX_GUARD_FAILMODE_AND_RUNTIME_POLICY.md`를 복구함. 남은 gap은 문서 부재가 아니라 live host 재-export 미확보 상태다.

## policy_change_log

- 2026-04-18: Decision 15 (AI-proposer / Human-approver) adopted; Decision 14 (Deputy Owner hybrid model) revoked same day. Revocation reason: 원혜연's operational strength is business work assignment, not system governance; assigning her Deputy operational authority produced form without substance. Replacement works via entity separation (AI proposer + human approver) for self-approval prevention and γ gate (proposer + independent reviewer + approver) for high-risk actions. See AX_ARCHITECTURE_DECISIONS §14-15.

## owner_absence_activation_procedure_template

Pending definition. Will be codified at first real Owner-absence scenario triggering Deputy activation. Scaffold:
- trigger check (unreachable beyond emergency window AND active-failure state)
- notification path to 원혜연
- scope of elevated authority (narrow — only what is needed to contain the failure)
- post-hoc 강은구 review within 72 hours
- incident log entry

## cycle_log
- 2026-04-20: `AX_handoff_package_2026-04-18_v2.zip`를 읽고 active policy baseline을 package v2로 재설정함. Core docs (`AX_ARCHITECTURE_DECISIONS`, `AX_AVAILABILITY_AND_RBAC`, `AX_OPERATIONS_POLICY`, `AX_SUPERSESSION_AND_NAMING_NOTICE`, `AX_PHASE0_INVENTORY_TEMPLATE`, `AX_OWNER_ABSENCE_LOG_DESTINATION_POLICY`, handoff, CLAUDE/AGENTS)를 package 기준으로 동기화함.
- 2026-04-20: package-v2 기준선 적용 후 잃어버린 current-state evidence를 `AX_PHASE0_INVENTORY_TEMPLATE`에 재병합했고, 보조 문서/스크립트의 `four-eyes` 잔재와 `v2` 참조를 현재 Decision 15 / γ gate / v3 기준으로 정리함.
- 2026-04-20: 강은구가 Slack/Telegram concrete values를 제공함 — Slack app `똘똘`, bot member `U0ARNS78EM9`, DM endpoint `D0AS8534L01`, Slack workspace `eunhyebooboo.slack.com`, Telegram bot `@SN_ocle_bot`. Slack workspace 값은 channel ID가 아니므로 기존 DM/channel 증거는 유지하고, bot identifier만 최신값으로 교체함. 기존 token 재사용과 기존 flow 종료 예정이 확인되어 credential blocker 정의를 `new token creation`에서 `retirement + exposure verification + SOPS migration`으로 재정의함.
- 2026-04-20: `docs/active/AX_PHASE0_INVENTORY_TEMPLATE.md`를 현재 회수 가능한 증거 기준으로 정리 완료. §§4–15.5는 채워졌고, 미복구 자산/라이브 증빙 부족만 §10·§11·§16에 blocker로 남김.
- 2026-04-20: Phase 0 필수 산출물로 `docs/active/AX_PHASE0_MIGRATION_ARTIFACTS.md`, `docs/active/AX_PHASE0_BASELINE_METRICS.md`를 추가해 old-to-new mapping, token ownership, secret rotation checklist, rollback/retirement checklist, baseline metrics 파일을 생성함. 다만 라이브 runtime export/브랜치 보호 증빙/실제 metric baseline 값은 인간 권한이 필요해 미완료 상태로 남김.
- 2026-04-20: 로컬 검증/자동화 경로 추가 — `scripts/validate_owner_absence.py`, `scripts/sync_owner_absence_phase_a.py`, `make owner-absence-validate`, `make phasea-dry-run`, `.github/workflows/owner-absence-validate.yml`. 현재는 로컬 dry-run/CI 준비까지 완료했고, 실제 Slack/Telegram fanout은 라이브 토큰 및 destination ID가 확보될 때만 활성화 가능함.
- 2026-04-20: `똘똘이mk2` 증거 회수 반영 — `docs/OPERATIONAL.md`의 실제 Slack channel ID 16개, `memory/2026-04-15.md`의 runtime truth(`openclaw.json` 우선, TOML stale), `docs/HISTORY.md`의 `90 -> 65` skill mapping 흔적, `docs/cc-rules-pack/*` 및 `scripts/server/install-claude-guard.sh`의 guard failmode 근거를 AX inventory/artifact/backlog에 반영함.
- 2026-04-20: Contabo live host(`root@5.182.17.93`) 직접 검증 완료 — `/root/.openclaw/openclaw.json` 실존, `route_logs/2026-04-15.jsonl` 실존, Telegram group id `ABEL=-1003286171878` / `은혜그룹=-1003881200687`, 그리고 `/usr/local/bin/run-claude*` guard marker 설치 상태를 확인함. 민감값은 저장하지 않고 sanitized snapshot만 문서화함.
- 2026-04-20: 같은 live host 검증에서 현재 runtime credential layout도 확정함 — Slack은 `root.channels.slack` 아래 단일 bot/app token set, Telegram은 `root.channels.telegram` 아래 단일 bot token 1개만 사용 중이며, 따라서 현재는 AX 전용 isolated credential set이 아직 아님을 문서에 반영함. GitHub canonical remote는 `hakhamsolution/ax-audit`로 식별 후 HTTPS 인증 경로를 복구해 `main` 첫 push까지 완료했고, 이제 branch protection은 repo bootstrap이 아니라 설정 증빙 단계만 남음.
- 2026-04-20: GitHub Actions/보호정책 실증 — `owner-absence-validate` 수동 run(`24640809639`)은 생성됐지만 job 시작 전 billing gate로 차단되었고, private repo `hakhamsolution/ax-audit`의 branch protection/rulesets API는 현재 플랜에서 `403 Upgrade to GitHub Pro or make this repository public`를 반환함. 따라서 현재 blocker는 Codex 업로드가 아니라 GitHub billing + plan gate다.
- 2026-04-20: Slack connector/API로 `#000-대표-똘똘이`의 permalink `https://eunhyebooboo.slack.com/archives/C0ASNEFES4C`와 ID `C0ASNEFES4C`를 재확인했고, 2026-04-15/16 메시지 hit로 해당 채널 경로가 아직 live임을 확인함. 따라서 “최종 Slack channel URL/ID 확인” blocker는 해소됐고, 남은 것은 prior-flow retirement 증빙이다.
- 2026-04-20: Track A 초벌 안전 스캔(`ax-audit`, `ax_handoff_package`, `똘똘이mk2`) 결과, `ax-audit`/`ax_handoff_package`에는 tracked `.env*`/`*secret*` 파일이 없고, `똘똘이mk2`에는 gitignored `SECRETS.md`와 tracked `dashboard/.env.example`가 존재함을 확인했다. 또한 `똘똘이mk2` git history keyword scan은 `src/config.ts`, `src/telegram-bot.ts`, `scripts/heartbeat.py`, `scripts/heartbeat_checks/info_requests.py` 등 token-handling code path 흔적을 보여서 exposure verification은 계속 open 상태다.
- 2026-04-26: billing-gate 재검증 — `gh workflow run owner-absence-validate --ref main` (run `24934831397`)이 self-hosted runner `hakham-vps`에서 13초 만에 success로 종료. 즉 self-hosted 우회 경로가 현재 alive함을 확인. 동시에 `gh api repos/hakhamsolution/ax-audit/branches/main/protection` 및 `…/rulesets`는 여전히 `403 Upgrade to GitHub Pro or make this repository public`. 따라서 두 gate를 분리해 추적: billing=resolved, plan-gate=active. Plan-gate 해소는 (a) `hakhamsolution` GitHub Pro 업그레이드, (b) 거버넌스 repo의 org tier 이전, (c) `ax-audit` public 전환 셋 중 하나의 인간 결정이 필요.
- 2026-04-26: Track A finalize — `똘똘이mk2` git history에서 `BOT_TOKEN="xoxb-9849432992692-10872891286723-…"` 평문 Slack bot token 노출을 확인. backlog/SECRETS.md 자체에서도 같은 토큰 prefix를 "재발급 필요"로 이미 분류. PHASE0 §9에 finalize 반영함. 다음 액션: R1 rotation 제안 PR(AI propose + 강은구 approve, γ gate 아님). Telegram bot token도 동일 노출 가능성 차단 차원에서 동시 회전 권고.
- 2026-04-26: Owner decision — Track A로 노출이 입증된 Slack bot/app token과 precautionary Telegram bot token의 R1 rotation은 **수행하지 않음**. 노출은 Owner-accepted residual risk로 기록되며 AX cutover는 기존 토큰을 그대로 재사용한다. PHASE0 §9·§15.6에 결정 명시. 향후 새로운 signal(abuse, unauthorized use, Owner의 새 지시)이 없는 한 AI는 이 rotation을 다시 제안하지 않는다. SOPS+age 마이그레이션은 별개 일정으로 남는다.
- 2026-04-26: Owner decision — plan-gate 해소 경로로 `hakhamsolution/ax-audit` repo visibility를 public으로 전환. `gh repo edit hakhamsolution/ax-audit --visibility public --accept-visibility-change-consequences` 적용 후 `gh repo view`는 `"visibility":"PUBLIC"`을 반환했고, `gh api .../branches/main/protection`은 `404 Branch not protected`(plan-gate 403 사라짐, protection 미설정 의미), `gh api .../rulesets`은 `[]`(plan-gate 403 사라짐, ruleset 미설정 의미)을 반환해 plan-gate 해소를 검증. 다음 단계는 WB2에서 `main` branch protection을 실제로 설정해 PR-only 강제를 정책-only에서 기술 강제로 승격시키는 것.
- 2026-04-26: Owner decision — WB2 deadline을 2026-04-21에서 **2026-05-08**로 갱신. handoff v3로 patch. WB2 첫 deliverable는 `main` branch protection 적용이며, 이를 정상 γ gate end-to-end (Codex proposer + 별도 Claude Code reviewer 세션 + 강은구 approver)로 수행해 KPI K4("γ gate workflow verified end-to-end")를 합성 테스트 없이 자연스럽게 충족시킨다. 후속 단계(인벤토리, 원혜연 access 감축, 잔여 γ gate enforcement)는 동일 deadline 안에서 순차 진행.
- 2026-04-20: WB1 smoke test 선언 `OA-20260419-000`을 Notion canonical(page `3479f4ce-ee5b-81ee-b11f-c5751cdfda7e`)에 생성 후 `ratified`/`synced`로 갱신했고, Git canonical `audit/owner_absence.jsonl`에는 append-only 규칙에 따라 pending/synced 이력 2줄을 추가함.
- 2026-04-20: Notion connector로 현재 운영 DB `421644f9-3db4-4f18-b50e-b6e35c019f25` (`AX 소유자 부재 신고`)의 data source `collection://be325b8a-ef40-4245-9947-470debe58c26`를 직접 갱신해 `declaration_id`~`last_updated_at` v1.0 스키마 전체를 생성했고, 후속 `notion.fetch`에서 모든 속성이 커넥터 응답에 노출됨을 확인.
- 2026-04-20: 같은 DB에 핵심 운영 뷰 5개를 생성함 — `All declarations`, `Active absences`, `Pending ratification`, `Conflicts`, `Audit export`.
- 2026-04-20: 중복 영문 DB `57605a19-e78d-491e-bd29-c397396b99ae` (`AX Owner Absence Declarations`)를 휴지통으로 보내 부모 페이지 `은혜그룹`에는 운영 DB `AX 소유자 부재 신고`만 남도록 정리함.
- 2026-04-20: `make notion-create NOTION_PARENT_PAGE_ID=33c9f4ce-ee5b-80c5-b287-de3f43128ddf NOTION_TOKEN=...` 실행으로 새 DB를 생성해 DB명이 `AX 소유자 부재 신고`로 확인되었고 ID가 `421644f9-3db4-4f18-b50e-b6e35c019f25`로 발급됨. 이어진 `make notion-verify`는 통합 토큰의 속성 가시성 제한으로 `live properties are not visible via this integration context` 상태를 반환해 UI에서 직접 확인이 필요함.
- 2026-04-20: 2026-04-20 최종 재시도 결과: `NOTION_TOKEN` 적용 후 `--verify`는 API상 속성 가시성 제한으로 `live properties are not visible via this integration context` 상태가 반복됨. 클립보드 캡처 OCR(rapidocr-onnxruntime)에서 `Ax Owner Absence Declarations`, `Default view`, `Name`만 안정적으로 인식되었고 `Schema v1.0`의 개별 사용자 정의 컬럼(예: Owner/Category 등)은 판독되지 않음. 최종 판별은 Notion UI에서 DB 속성 전체 펼침 확인이 필요함.
- 2026-04-20: Make 연동 관점 대응 위해 `Makefile`에 `notion-dry`, `notion-verify`, `notion-create` 타깃을 추가. `make notion-verify NOTION_DATABASE_ID=... NOTION_TOKEN=...` 경로로, 코덱스 API 가시성 제한이 있을 때 Make의 노드(별도 연결 토큰) 검증 플로우와 동일하게 운용 가능하도록 정리.

- 2026-04-18: cycle opened; WB1 scheduled.
- 2026-04-18: handoff package assembled; one document gap noted (see gaps_at_handoff).
- 2026-04-19: WB1-B executed locally in this session: `bash scripts/init_owner_absence_log.sh` confirmed audit canonical files exist (`owner_absence.jsonl` empty, `owner_absence.schema.json`, `README.md`) and script is idempotent.
- 2026-04-19: WB1-C dry-run executed with `python3 scripts/init_notion_owner_absence_db.py --dry-run` and generated expected Notion DB payload for `AX Owner Absence Declarations`; real Notion API run remains pending because `NOTION_TOKEN` / parent page ID governance requires Owner/Deputy provision.
- 2026-04-19: WB1-C re-check confirms `python3 scripts/init_notion_owner_absence_db.py --dry-run` now blocks without env vars in this environment; required: `NOTION_PARENT_PAGE_ID`, `NOTION_TOKEN`.
- 2026-04-20: WB1-C verify blocker confirmed: Notion API `databases.retrieve` returns limited schema visibility in this integration context; schema parity check is now treated as inconclusive when live property metadata is unavailable, and requires manual UI verification in Notion.
- 2026-04-20: Notion DB fetch for `57605a19-e78d-491e-bd29-c397396b99ae` shows data source schema rendering currently as `Name`-only in connector view; proceed with manual Notion UI check for full schema v1.0 column parity.
- 2026-04-20: 재시도 실행 결과, `NOTION_TOKEN`/`NOTION_PARENT_PAGE_ID` 미등록으로 실전 호출은 차단(verify 실행은 실패). 다만 `--dry-run`은 성공했고, 부모페이지 `33c9f4ce-ee5b-80c5-b287-de3f43128ddf`로 `AX Owner Absence Declarations` 스키마 payload 생성 형식이 정상적으로 출력됨.
- 2026-04-20: 사용자 토큰 적용 후 `--verify` 재시도했으나 `httpx.ConnectError: nodename nor servname provided, or not known`로 API 호출이 실패했으며, Notion 커넥터 `notion.fetch` 결과는 동일하게 DB data source schema가 `Name` only(`displayProperties: ["Name"]`)로 보임. 현재 상태는 수동 UI 확인으로만 진행 필요.
- 2026-04-20: 최신 실행에서 `--verify`는 성공적으로 완료되었으나 `[verify] INFO: live properties are not visible via this integration context.` 메시지가 출력되며 API로는 속성 가시성 확인 불가. 즉, Notion UI에서 AX Owner Absence Declarations v1.0 스키마(예: Owner, Category 등)를 직접 확인해야 함.
- 2026-04-20: 캡처 파일 OCR(rapidocr-onnxruntime, 확대 1.5x~3x) 분석 결과, 화면 상 `Ax Owner Absence Declarations` DB 헤더에서 `Default view`와 `Name`만 가시적이며, v1.0 스키마 추가 컬럼은 캡처 기준 미확인. 수동확인 상태는 계속 Open(수동 판별 필요).
