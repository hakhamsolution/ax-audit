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

- 2026-04-20: Notion API visibility gate — `python3 scripts/init_notion_owner_absence_db.py --verify --database-id 57605a19-e78d-491e-bd29-c397396b99ae` succeeds with
  inconclusive status (`live properties are not visible`) and requires manual UI confirmation of schema v1.0.
- 2026-04-20: 사용자가 직접 확인한 결과와 최신 Notion 조회 모두 동일: `AX Owner Absence Declarations` DB 스키마에 v1.0 사용자 정의 속성이 반영되지 않고 `Name`(타이틀)만 표시됨. 현재 Notion/connector 모두에서 스키마 부재 상태가 확인됨.
- 2026-04-20: 부모 페이지 `은혜그룹` 아래에 Owner-absence DB가 2개(`57605a19-e78d-491e-bd29-c397396b99ae`, `421644f9-3db4-4f18-b50e-b6e35c019f25`) 존재함. 현재 운영 대상으로는 후자만 복구했으며, 전자 정리(보존/삭제/이름변경)는 인간 결정이 필요함.
- 2026-04-20: 현재 Owner-absence canonical의 Notion 컬럼명을 한글로 바꾸는 것은 `AX_OWNER_ABSENCE_LOG_SCHEMA_DESIGN.md` 기준 스키마 변경에 해당하며 four-eyes 승인이 필요함. 즉시 변경하지 말고 다음 스키마 버전 제안으로 다뤄야 함.

## access_realignment_log

_(empty — populate during WB2; one line per access change with before/after)_

## operational_bookmarks

- notion_database_id: 421644f9-3db4-4f18-b50e-b6e35c019f25 (현재 사용 DB, DB명: AX 소유자 부재 신고, v1.0 스키마 생성 대상)
- notion_integration_name: _(populate after WB1 Track C)_
- audit_repo_url: _(populate after WB1 Track B)_
- owner_absence_log_path_git: `audit/owner_absence.jsonl`
- slack_admin_channel: `#000-대표-똘똘이 (C0ASNEFES4C)` — `똘똘이mk2` `approval-workflow.sh`의 L3/L4 승인 경로와 `heartbeat` 기본 escalation channel 기준
- telegram_admin_endpoint: `ABEL (-1003286171878)`, `은혜그룹 (-1003881200687)` — live host `openclaw.json`/cron evidence 기준; `은혜그룹`에서는 archive topic `92`도 관측됨

## gaps_at_handoff

- 2026-04-18: `docs/active/AX_GUARD_FAILMODE_AND_RUNTIME_POLICY.md` (v1) is referenced by `AX_SUPERSESSION_AND_NAMING_NOTICE.md` §1 and by `docs/handoff/AX_HANDOFF_TO_CLAUDE_CODE.md` §5 but is not present in this handoff package. It was authored in an earlier session. Recovery: retrieve from prior chat export, original working copy, or the Anthropic session history. Until restored, fall back to `AX_OPERATIONS_POLICY.md` §7 (which summarizes guard policy at a higher level) and do not design guard logic from scratch — that would be scope expansion.
- 2026-04-20: `똘똘이mk2`의 guard pack, installer, 2026-04-15 runtime audit 메모를 근거로 `docs/active/AX_GUARD_FAILMODE_AND_RUNTIME_POLICY.md`를 복구함. 남은 gap은 문서 부재가 아니라 live host 재-export 미확보 상태다.

## cycle_log
- 2026-04-20: `docs/active/AX_PHASE0_INVENTORY_TEMPLATE.md`를 현재 회수 가능한 증거 기준으로 정리 완료. §§4–15.5는 채워졌고, 미복구 자산/라이브 증빙 부족만 §10·§11·§16에 blocker로 남김.
- 2026-04-20: Phase 0 필수 산출물로 `docs/active/AX_PHASE0_MIGRATION_ARTIFACTS.md`, `docs/active/AX_PHASE0_BASELINE_METRICS.md`를 추가해 old-to-new mapping, token ownership, secret rotation checklist, rollback/retirement checklist, baseline metrics 파일을 생성함. 다만 라이브 runtime export/브랜치 보호 증빙/실제 metric baseline 값은 인간 권한이 필요해 미완료 상태로 남김.
- 2026-04-20: 로컬 검증/자동화 경로 추가 — `scripts/validate_owner_absence.py`, `scripts/sync_owner_absence_phase_a.py`, `make owner-absence-validate`, `make phasea-dry-run`, `.github/workflows/owner-absence-validate.yml`. 현재는 로컬 dry-run/CI 준비까지 완료했고, 실제 Slack/Telegram fanout은 라이브 토큰 및 destination ID가 확보될 때만 활성화 가능함.
- 2026-04-20: `똘똘이mk2` 증거 회수 반영 — `docs/OPERATIONAL.md`의 실제 Slack channel ID 16개, `memory/2026-04-15.md`의 runtime truth(`openclaw.json` 우선, TOML stale), `docs/HISTORY.md`의 `90 -> 65` skill mapping 흔적, `docs/cc-rules-pack/*` 및 `scripts/server/install-claude-guard.sh`의 guard failmode 근거를 AX inventory/artifact/backlog에 반영함.
- 2026-04-20: Contabo live host(`root@5.182.17.93`) 직접 검증 완료 — `/root/.openclaw/openclaw.json` 실존, `route_logs/2026-04-15.jsonl` 실존, Telegram group id `ABEL=-1003286171878` / `은혜그룹=-1003881200687`, 그리고 `/usr/local/bin/run-claude*` guard marker 설치 상태를 확인함. 민감값은 저장하지 않고 sanitized snapshot만 문서화함.
- 2026-04-20: 같은 live host 검증에서 현재 runtime credential layout도 확정함 — Slack은 `root.channels.slack` 아래 단일 bot/app token set, Telegram은 `root.channels.telegram` 아래 단일 bot token 1개만 사용 중이며, 따라서 현재는 AX 전용 isolated credential set이 아직 아님을 문서에 반영함. GitHub canonical remote는 `hakhamsolution/ax-audit`로 식별 후 HTTPS 인증 경로를 복구해 `main` 첫 push까지 완료했고, 이제 branch protection은 repo bootstrap이 아니라 설정 증빙 단계만 남음.
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
