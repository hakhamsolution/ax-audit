# AX_PHASE0_INVENTORY_TEMPLATE

Version: 2026-04-26 v15
Status: populated with current-state evidence and re-aligned to package-v2 Decision 15 baseline; billing gate resolved by self-hosted runner cutover (workflow run `24934831397` 13s success on 2026-04-25); plan-gate resolved 2026-04-26 by Owner decision to flip `hakhamsolution/ax-audit` from private to public (branch-protection / rulesets APIs now accessible); Track A is finalized with confirmed plain-text Slack bot-token exposure in `똘똘이mk2` git history, and Owner has explicitly decided NOT to rotate the exposed Slack/Telegram bot tokens at this time — the exposure is therefore a recorded acceptance of risk by the Owner. Remaining blockers documented in §10 and §16
Patch record:
- v2 incorporated AX_DEPUTY_OWNER_PATCH (2026-04-18 v1 active)
- v3 filled §15 with confirmed values, added §15.5 (AI agents), added §15.6 (immediate follow-up actions)
- v4 finalized §15.4 with γ (two-canonical) structure confirmed
- v5 incorporated `똘똘이mk2` runtime evidence: recovered guard policy document, filled concrete Slack channel IDs, and tightened runtime-truth notes
- v6 incorporated direct Contabo host verification: `openclaw.json`/route-log presence, Telegram group IDs, and runner-guard install markers
- v7 incorporated live credential-layout evidence: one shared Slack app+bot credential set and one shared Telegram bot token are confirmed in runtime; branch-protection blocker is narrowed to an identified but uninitialized GitHub remote
- v8 reflects successful GitHub HTTPS bootstrap: canonical remote `hakhamsolution/ax-audit` is initialized and `main` is published; branch-protection remains a settings-proof blocker only
- v9 incorporates GitHub platform-gate evidence: Actions run failure is caused by account billing, and branch-protection APIs for this private repo currently return plan-gated 403
- v10 re-aligns the inventory to `AX_handoff_package_2026-04-18_v2.zip`: Decision 15 terminology restored, proposer-approver model replaces hybrid/self-approval wording, and previously recovered runtime evidence is preserved
- v11 incorporates representative-provided Slack/Telegram concrete values: Slack app `똘똘`, bot member `U0ARNS78EM9`, DM endpoint `D0AS8534L01`, Telegram bot `@똘똘이`, and the decision to reuse existing tokens while retiring the prior flow
- v12 corrects those concrete values by distinguishing Slack workspace `eunhyebooboo.slack.com` from channel-level evidence and by updating the Telegram bot identifier to `@SN_ocle_bot`
- v13 confirms the current Slack admin-channel permalink `https://eunhyebooboo.slack.com/archives/C0ASNEFES4C`, records that the legacy Slack path is still active, and logs a preliminary Track A repo scan
- v14 records billing-gate resolution via `hakham-vps` self-hosted runner cutover (workflow run `24934831397` success in 13s), distinguishes the still-active plan-gate (branch-protection / rulesets API 403) from the now-resolved billing gate, and finalizes Track A with a confirmed plain-text Slack bot-token exposure in `똘똘이mk2` git history
- v15 records two Owner decisions made on 2026-04-26: (a) `hakhamsolution/ax-audit` was flipped from private to public to remove the plan-gate; branch-protection now returns `404 Branch not protected` and rulesets returns `[]`, both indicating API access is restored, and (b) the exposed Slack/Telegram bot tokens identified by Track A will NOT be rotated at this time; the exposure is recorded as an Owner-accepted residual risk and the AX cutover will continue to reuse the existing tokens

## 1. Purpose

This document is the required inventory template for Phase 0.
No migration, consolidation, promotion, or retirement decision is valid until this inventory exists in filled form.

## 2. Rule

Phase 0 is not planning.
Phase 0 is evidence collection.

If this inventory is incomplete, all downstream architecture work is provisional only.

## 3. Required outputs

The filled inventory must contain all of the following:

1. current agent inventory — **filled in §4**
2. current channel ownership map — **filled in §5**
3. current tool map — **filled in §6**
4. current hook map — **filled in §7**
5. current wrapper and script inventory — **filled in §8**
6. secrets exposure list — **filled in §9**
7. missing asset list — **filled in §10**
8. skill-by-skill classification table — **filled in §11** (current recoverable surface classified; historical 57-skill manifest remains an archival gap only)
9. current session-truth locations — **filled in §12**
10. current fallback paths — **filled in §13**
11. current approval paths — **filled in §14**
12. current human operators and privileges — **filled in §15**
13. Owner-absence declaration log destination — **filled in §15.4, γ two-canonical confirmed**
14. proposer-approver separation register — **filled in §15.3**

## 4. Current agent inventory

Evidence basis:
- `똘똘이mk2/docs/OPERATIONAL.md` (2026-04-15)
- `똘똘이mk2/dashboard/data/agents.json` snapshot (60 active agents across 4 planes)

Human owner is system-level only in the current evidence set. No per-agent human owner manifest was found, so the table records the current effective system holders instead.

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

| agent_id | display_name | current_layer | current_runtime | current_owner | primary_function | actual_inputs | actual_outputs | current_channels | tool_access | secrets_dependency | failure_history | target_state |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| main | 똘똘이 | L1 | OpenClaw | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 전체 세션 관리, 레인 선택, 위임 판단 | Telegram / Slack / Gateway ingress, jarvis brief, team-lead reports | routing decision, final response, escalation notice | Telegram / Slack (#t-management) / Gateway UI | OpenAI Direct + gateway/router + routing logs | yes: gateway token, model creds, channel/bot creds | direct-reply drift if work is not re-routed | merge -> hq-router |
| jarvis | 자비스 | L1 | OpenClaw | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 요청 수신, 분류, 브리핑 생성, 라우팅 | public requests from Telegram / Slack / Gateway UI | briefing packet and route selection | Telegram / Slack ingress, #003-간부회의 | OpenAI Direct + gateway/router + routing logs | yes: gateway token, model creds, channel/bot creds | ingress misclassification under channel drift | merge -> hq-router |
| tobak | 바로미 | L1 | OpenClaw | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 사실 확인, 데이터/수치 검증 | candidate output, risk signal, verification request | audit note, verification result, risk flag | #003-간부회의 / internal control-plane lane | OpenAI Direct + gateway/router + routing logs | yes: gateway token, model creds, channel/bot creds | documented failure pattern not uniquely evidenced | merge -> governance-audit |
| kokkkok | 콕콕 | L1 | OpenClaw | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 전략 인사이트: 시장/경쟁사/트렌드 분석 | candidate output, risk signal, verification request | audit note, verification result, risk flag | #003-간부회의 / internal control-plane lane | OpenAI Direct + gateway/router + routing logs | yes: gateway token, model creds, channel/bot creds | documented failure pattern not uniquely evidenced | merge -> research-core |
| matchum | 맞춤 | L1 | OpenClaw | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 브랜드 톤앤매너 검수, 보이스 일관성 | candidate output, risk signal, verification request | audit note, verification result, risk flag | #003-간부회의 / internal control-plane lane | OpenAI Direct + gateway/router + routing logs | yes: gateway token, model creds, channel/bot creds | documented failure pattern not uniquely evidenced | merge -> business-content |
| dadeum | 다듬 | L1 | OpenClaw | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 맞춤법/문법, 가독성, 최종 품질 보증 | candidate output, risk signal, verification request | audit note, verification result, risk flag | #003-간부회의 / internal control-plane lane | OpenAI Direct + gateway/router + routing logs | yes: gateway token, model creds, channel/bot creds | documented failure pattern not uniquely evidenced | merge -> business-content |
| gganggan | 도장 | L1 | OpenClaw | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | QA & Risk Control, 품질 검증 | candidate output, risk signal, verification request | approval/reject verdict with review notes | #003-간부회의 / internal control-plane lane | OpenAI Direct + gateway/router + routing logs | yes: gateway token, model creds, channel/bot creds | documented failure pattern not uniquely evidenced | merge -> governance-audit |
| pi_audit | PI-감사리드 | L1 | OpenClaw | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 연구 감사 총괄 | research briefs, artifacts, documents, audit context | audit note, verification result, risk flag | #003-간부회의 / internal control-plane lane | OpenAI Direct + gateway/router + routing logs | yes: gateway token, model creds, channel/bot creds | documented failure pattern not uniquely evidenced | merge -> governance-audit |
| baromi_r | 바로미-R | L1 | OpenClaw | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 방법론 적정성 감사 | research briefs, artifacts, documents, audit context | audit note, verification result, risk flag | #003-간부회의 / internal control-plane lane | OpenAI Direct + gateway/router + routing logs | yes: gateway token, model creds, channel/bot creds | documented failure pattern not uniquely evidenced | merge -> governance-audit |
| matchum_r | 맞춤-R | L1 | OpenClaw | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 데이터-결론 정합성 감사 | research briefs, artifacts, documents, audit context | audit note, verification result, risk flag | #003-간부회의 / internal control-plane lane | OpenAI Direct + gateway/router + routing logs | yes: gateway token, model creds, channel/bot creds | documented failure pattern not uniquely evidenced | merge -> governance-audit |
| dojang_r | 도장-R | L1 | OpenClaw | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 연구 결과 채택 승인 | research briefs, artifacts, documents, audit context | approval/reject verdict with review notes | #003-간부회의 / internal control-plane lane | OpenAI Direct + gateway/router + routing logs | yes: gateway token, model creds, channel/bot creds | documented failure pattern not uniquely evidenced | merge -> governance-audit |
| ddoldol | 똘똘 | L2 | Codex OAuth | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 내부 실행 총괄 (Codex OAuth 우선) | internal ops request, reminders, inbox/admin context | ops summary, reminder, admin action note | Slack internal-only (#001-비서실-똘똘 / office lane) | GPT-5.4 trusted runner + repo shell + agent-specific tools | yes: ~/.codex/auth.json, repo/env creds, channel app creds | runner metadata omission / fallback handoff drift | merge -> hq-router |
| bopil | 보필 | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 대표 일정/문서 관리 | internal ops request, reminders, inbox/admin context | ops summary, reminder, admin action note | #003-간부회의 + Slack 부서채널 | Opus 4.6 worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | merge -> comms-admin |
| mosim | 모심 | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 똘똘이 위임 작업 보조 | internal ops request, reminders, inbox/admin context | ops summary, reminder, admin action note | Slack internal-only (#001-비서실-똘똘 / office lane) | Opus 4.6 worker + agent-specific includes | no direct secret use documented | legacy Slack channel references and doc/runtime mismatch | merge -> comms-admin |
| allim | 알림 | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 이메일 발송, 후속조치 | internal ops request, reminders, inbox/admin context | ops summary, reminder, admin action note | #003-간부회의 + Slack 부서채널 | Opus 4.6 worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | merge -> comms-admin |
| allim_r | 알림-R | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 정기 보고 리마인드, 마감 추적 | internal ops request, reminders, inbox/admin context | ops summary, reminder, admin action note | Slack internal-only (#001-비서실-똘똘 / office lane) | Opus 4.6 worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | merge -> comms-admin |
| salpim | 살핌 | L2 | Codex OAuth | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 전사 상태 체크 | internal ops request, reminders, inbox/admin context | ops summary, reminder, admin action note | #003-간부회의 + Slack 부서채널 | GPT-5.4 trusted runner + repo shell + agent-specific tools | yes: ~/.codex/auth.json, repo/env creds, channel app creds | runner metadata omission / fallback handoff drift | merge -> ops-platform |
| gamsa | 감사 | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 운영 프로세스 감사 | internal ops request, reminders, inbox/admin context | ops summary, reminder, admin action note | #003-간부회의 + Slack 부서채널 | Opus 4.6 worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | merge -> governance-audit |
| chok | 촉 | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 시장/트렌드 분석 | strategy question, web/data sources, market scope | research memo, findings, recommendation | #003-간부회의 + Slack 부서채널 | Opus 4.6 worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | merge -> research-core |
| satssat | 샅샅 | L2 | Codex OAuth | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 심층 조사, 데이터 수집 | strategy question, web/data sources, market scope | research memo, findings, recommendation | #003-간부회의 + Slack 부서채널 | GPT-5.4 trusted runner + repo shell + agent-specific tools | yes: ~/.codex/auth.json, repo/env creds, channel app creds | runner metadata omission / fallback handoff drift | merge -> research-core |
| geomi | 거미 | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 웹 데이터 수집 | strategy question, web/data sources, market scope | research memo, findings, recommendation | #003-간부회의 + Slack 부서채널 | Opus 4.6 worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | merge -> research-core |
| ieum | 이음 | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 고객 관계 관리 | strategy question, web/data sources, market scope | research memo, findings, recommendation | #003-간부회의 + Slack 부서채널 | Opus 4.6 worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | merge -> comms-admin |
| gijun | 기준 | L2 | Codex OAuth | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | SOP, 정책 문서 | strategy question, web/data sources, market scope | research memo, findings, recommendation | #003-간부회의 + Slack 부서채널 | GPT-5.4 trusted runner + repo shell + agent-specific tools | yes: ~/.codex/auth.json, repo/env creds, channel app creds | runner metadata omission / fallback handoff drift | merge -> governance-audit |
| sulsul | 술술 | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 블로그, 카피라이팅 | content brief, brand inputs, asset request | draft asset/doc plus Slack report | #003-간부회의 + Slack 부서채널 | Sonnet 4.6 worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | merge -> business-content |
| grimi | 그리미 | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | UI/비주얼 가이드 | content brief, brand inputs, asset request | draft asset/doc plus Slack report | #003-간부회의 + Slack 부서채널 | Opus 4.6 worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | merge -> business-content |
| kkumi | 꾸미 | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 카드뉴스, 썸네일 | content brief, brand inputs, asset request | draft asset/doc plus Slack report | #003-간부회의 + Slack 부서채널 | Opus 4.6 worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | merge -> business-content |
| ssakduk | 싹둑 | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 영상 편집/생성 | content brief, brand inputs, asset request | draft asset/doc plus Slack report | #003-간부회의 + Slack 부서채널 | Opus 4.6 worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | merge -> business-content |
| sori | 소리 | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | TTS, 음성 콘텐츠 | content brief, brand inputs, asset request | draft asset/doc plus Slack report | #003-간부회의 + Slack 부서채널 | Opus 4.6 worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | merge -> business-content |
| chakchak | 착착 | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | PPT, 프레젠테이션 | content brief, brand inputs, asset request | draft asset/doc plus Slack report | #003-간부회의 + Slack 부서채널 | Opus 4.6 worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | merge -> business-content |
| narae | 나래 | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 다국어 번역 | content brief, brand inputs, asset request | draft asset/doc plus Slack report | #003-간부회의 + Slack 부서채널 | Opus 4.6 worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | merge -> business-content |
| chukchuk | 척척 | L2 | Codex OAuth | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 제안서/입찰서 작성 | RFP, proposal brief, pricing inputs | proposal/estimate package | #003-간부회의 + Slack 부서채널 | GPT-5.4 trusted runner + repo shell + agent-specific tools | yes: ~/.codex/auth.json, repo/env creds, channel app creds | runner metadata omission / fallback handoff drift | merge -> business-content |
| sem | 셈 | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 비용 산출 | RFP, proposal brief, pricing inputs | proposal/estimate package | #003-간부회의 + Slack 부서채널 | Opus 4.6 worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | merge -> ops-platform |
| jjaim | 짜임 | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 교육 과정 설계 | course/learner request, rubric or LMS context | curriculum/learner ops artifact | #003-간부회의 + Slack 부서채널 | Spark worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | merge -> business-content |
| dolbom | 돌봄 | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 학습자 관리 | course/learner request, rubric or LMS context | curriculum/learner ops artifact | #003-간부회의 + Slack 부서채널 | Opus 4.6 worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | merge -> business-content |
| ggomggom | 꼼꼼 | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 평가 기준 설계 | course/learner request, rubric or LMS context | curriculum/learner ops artifact | #003-간부회의 + Slack 부서채널 | Opus 4.6 worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | merge -> business-content |
| nuri | 누리 | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 학습관리시스템 | course/learner request, rubric or LMS context | curriculum/learner ops artifact | #003-간부회의 + Slack 부서채널 | Opus 4.6 worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | merge -> business-content |
| hreum | 흐름 | L2 | Codex OAuth | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 워크플로우 자동화 | automation requirements, repo/workflow context, failure signals | workflow/agent implementation or failure report | #003-간부회의 + Slack 부서채널 | GPT-5.4 trusted runner + repo shell + agent-specific tools | yes: ~/.codex/auth.json, repo/env creds, channel app creds | runner metadata omission / fallback handoff drift | merge -> automation-dev |
| butim | 붙임 | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | API 연동, 외부 서비스 | automation requirements, repo/workflow context, failure signals | workflow/agent implementation or failure report | #003-간부회의 + Slack 부서채널 | Opus 4.6 worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | merge -> automation-dev |
| jitgi | 짓기 | L2 | Codex OAuth | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 에이전트 설계 | automation requirements, repo/workflow context, failure signals | workflow/agent implementation or failure report | #003-간부회의 + Slack 부서채널 | GPT-5.4 trusted runner + repo shell + agent-specific tools | yes: ~/.codex/auth.json, repo/env creds, channel app creds | runner metadata omission / fallback handoff drift | merge -> automation-dev |
| simgi | 심기 | L2 | Codex OAuth | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 에이전트 개발 | automation requirements, repo/workflow context, failure signals | workflow/agent implementation or failure report | #003-간부회의 + Slack 부서채널 | GPT-5.4 trusted runner + repo shell + agent-specific tools | yes: ~/.codex/auth.json, repo/env creds, channel app creds | runner metadata omission / fallback handoff drift | specialist -> codegen-specialist |
| baechi | 배치 | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 조직 인력 배치 | org/personnel change request | org change proposal or execution checklist | #003-간부회의 + Slack 부서채널 | Opus 4.6 worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | unknown (no canonical target yet) |
| seolgye | 설계 | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 조직 구조 설계 | org/personnel change request | org change proposal or execution checklist | #003-간부회의 + Slack 부서채널 | GPT-5.4 worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | unknown (no canonical target yet) |
| gaepyeon | 개편 | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 조직 변경 실행 | org/personnel change request | org change proposal or execution checklist | #003-간부회의 + Slack 부서채널 | Opus 4.6 worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | unknown (no canonical target yet) |
| jjagae | 짜개 | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 연구 문제 정의 | research briefs, artifacts, documents, audit context | research artifact, WBS, evidence, knowledge entry | #003-간부회의 + Slack 부서채널 | Spark worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | merge -> research-core |
| seolmun | 설문 | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 연구 발주 관리 | research briefs, artifacts, documents, audit context | research artifact, WBS, evidence, knowledge entry | #003-간부회의 + Slack 부서채널 | Spark worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | merge -> research-core |
| seolmun_r | 설문-R | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 연구 가설 수립 | research briefs, artifacts, documents, audit context | research artifact, WBS, evidence, knowledge entry | #003-간부회의 + Slack 부서채널 | Opus 4.6 worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | merge -> research-core |
| satssat_r | 샅샅-R | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 문헌 조사 | research briefs, artifacts, documents, audit context | research artifact, WBS, evidence, knowledge entry | #003-간부회의 + Slack 부서채널 | Opus 4.6 worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | merge -> research-core |
| jium | 지음 | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 연구 계획서 | research briefs, artifacts, documents, audit context | research artifact, WBS, evidence, knowledge entry | #003-간부회의 + Slack 부서채널 | GPT-5.4 worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | merge -> research-core |
| sallim | 살림 | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 스코프 관리 | research briefs, artifacts, documents, audit context | research artifact, WBS, evidence, knowledge entry | #003-간부회의 + Slack 부서채널 | Opus 4.6 worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | merge -> research-core |
| sallim_pmo | 살림-PMO | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 연구 과제 관리 | research briefs, artifacts, documents, audit context | research artifact, WBS, evidence, knowledge entry | #003-간부회의 + Slack 부서채널 | GPT-5.4 worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | merge -> research-core |
| salpi | 살피 | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 공모전/과제 발굴 | research briefs, artifacts, documents, audit context | research artifact, WBS, evidence, knowledge entry | #003-간부회의 + Slack 부서채널 | Opus 4.6 worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | merge -> research-core |
| salpi_rfp | 살피-RFP | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 제안 요청 분석 | research briefs, artifacts, documents, audit context | research artifact, WBS, evidence, knowledge entry | #003-간부회의 + Slack 부서채널 | Opus 4.6 worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | merge -> research-core |
| hreum_r | 흐름-R | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 작업분류체계 | research briefs, artifacts, documents, audit context | research artifact, WBS, evidence, knowledge entry | #003-간부회의 + Slack 부서채널 | Opus 4.6 worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | merge -> research-core |
| sem_r | 셈-R | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 연구 예산 관리 | research briefs, artifacts, documents, audit context | research artifact, WBS, evidence, knowledge entry | #003-간부회의 + Slack 부서채널 | Opus 4.6 worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | unknown |
| chagok | 차곡 | L2 | Codex OAuth | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 연구 데이터 정리 | research briefs, artifacts, documents, audit context | research artifact, WBS, evidence, knowledge entry | #003-간부회의 + Slack 부서채널 | GPT-5.4 trusted runner + repo shell + agent-specific tools | yes: ~/.codex/auth.json, repo/env creds, channel app creds | runner metadata omission / fallback handoff drift | merge -> archive-memory |
| chagok_r | 차곡-R | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 산출물 관리 | research briefs, artifacts, documents, audit context | research artifact, WBS, evidence, knowledge entry | #003-간부회의 + Slack 부서채널 | Opus 4.6 worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | merge -> archive-memory |
| chakchak_r | 착착-R | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 평가 발표 대응 | research briefs, artifacts, documents, audit context | research artifact, WBS, evidence, knowledge entry | #003-간부회의 + Slack 부서채널 | Opus 4.6 worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | merge -> business-content |
| sem_a | 셈-A | L2 | Claude Code | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | R&D 자원 감사 | research briefs, artifacts, documents, audit context | research artifact, WBS, evidence, knowledge entry | #003-간부회의 + Slack 부서채널 | Opus 4.6 worker + agent-specific includes | yes: runner env + Slack/Notion/app credentials as needed | legacy Slack channel references and doc/runtime mismatch | merge -> governance-audit |
| bangpae | 방패 | L2 | Codex OAuth | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | 사이버보안 감사, 취약점 진단 (Strix) | candidate output, risk signal, verification request | audit note, verification result, risk flag | #003-간부회의 + Slack 부서채널 | GPT-5.4 trusted runner + repo shell + agent-specific tools | yes: ~/.codex/auth.json, repo/env creds, channel app creds | runner metadata omission / fallback handoff drift | specialist -> incident-specialist |
| hermes_main | 헤르메스 | L2 | Hermes | 강은구 / 원혜연 (system-level only; per-agent owner undocumented) | deep work, 메모리, 장기 실행, 실험 (NousResearch Hermes Agent) | long-running task, memory sync, experimental request | deep-work result or memory artifact | none (channel unconnected) | Ollama gemma4:e2b + local memory/runtime | no direct secret read evidenced; local runtime only | channel unconnected; recovery path untested | specialist -> incident-specialist |

## 5. Channel ownership map

| Channel | Current owner | Current token/bot | Purpose | Collision risk | Proposed future owner |
|---|---|---|---|---|---|
| Telegram manager groups `ABEL` (`-1003286171878`), `은혜그룹` (`-1003881200687`) | `main` / `jarvis` ingress | Telegram bot token (`SECRETS.md`, legacy collision noted) | 대표 지시, mobile ingress, archive source; `은혜그룹`에서는 topic `92` archive topic도 관측됨 | high | `hq-router` only |
| Slack `#000-대표-똘똘이` (`C0ASNEFES4C`) | `main`, approval workflow, heartbeat escalation | Slack app/bot token (exact app split not yet exported) | 대표 direct ingress, L3/L4 escalation, admin heartbeat escalation; permalink confirmed as `https://eunhyebooboo.slack.com/archives/C0ASNEFES4C`, and recent 2026-04-15/16 message hits show the path is still live | medium | `hq-router` + human approvers |
| Slack DM `D0AS8534L01` | 강은구 ↔ `똘똘` bot | existing shared Slack app/bot token; bot member `U0ARNS78EM9` | current simple direct bot conversation | medium | temporary mirror/intake only; consider dedicated private channel if 원혜연 / governance-audit read access becomes necessary |
| Slack `#접수-자비스` (`C0ASXPG761X`) | `main`, `jarvis` | Slack app/bot token | intake / 접수 보조 | medium | `hq-router` only |
| Slack `#002-이사회` (`C0ASCNT8PFD`) | OpenClaw control plane core 7 | Slack app/bot token | control-plane collaboration | medium | core control-plane only |
| Slack `#003-간부회의` (`C0ASGQQFP8W`) | `main` + 13 team leads | Slack app/bot token | 배분, 접수, 보고, QA, route handoff | medium | consolidated core-team leads |
| Slack `#001-비서실-똘똘` (`C0AS3FQSH7V`) | `ddoldol` | Slack app/bot token | office team lead channel | medium | `comms-admin` |
| Slack `#전략실-콕콕` (`C0AT45R3YSU`) | `kokkkok` | Slack app/bot token | strategy team lead channel | medium | `research-core` |
| Slack `#제작실-술술` (`C0AS6F7U1N1`) | `sulsul` | Slack app/bot token | content team lead channel | medium | `business-content` |
| Slack `#세일즈-척척` (`C0ASNQ238QZ`) | `chukchuk` | Slack app/bot token | sales team lead channel | medium | `business-content` |
| Slack `#교육실-짜임` (`C0ARUDVA54P`) | `jjaim` | Slack app/bot token | education team lead channel | medium | `comms-admin` |
| Slack `#자동화-흐름` (`C0ASDF1NFQU`) | `hreum` | Slack app/bot token | automation team lead channel | medium | `automation-dev` |
| Slack `#인사실-설계` (`C0ASGQQSXRU`) | `seolgye` | Slack app/bot token | HR team lead channel | medium | `comms-admin` |
| Slack `#품질관리-도장` (`C0AT45S08QG`) | `gganggan` | Slack app/bot token | QA / risk team lead channel | medium | `governance-audit` |
| Slack `#연구접수-설문` (`C0AS7RAFXBQ`) | `seolmun` | Slack app/bot token | R&D intake team lead channel | medium | `research-core` |
| Slack `#연구기획-짜개` (`C0AS6F7SHK7`) | `jjagae` | Slack app/bot token | R&D planning team lead channel | medium | `research-core` |
| Slack `#연구제안-지음` (`C0AS3FRP7S7`) | `jium` | Slack app/bot token | R&D proposal team lead channel | medium | `research-core` |
| Slack `#연구운영-살림` (`C0AT45SVBQQ`) | `sallim_pmo` | Slack app/bot token | R&D operations team lead channel | medium | `archive-memory` |
| Slack `#연구감사-감사리드` (`C0AT45RBEV6`) | `pi_audit` | Slack app/bot token | R&D audit team lead channel | medium | `governance-audit` |
| Slack `#999-컨퍼런스` (`C0ASM1RBWBX`) | `main` + 13 team leads | Slack app/bot token | 팀장 간 착수, 협조, 검수 공지 | medium | consolidated core-team leads |
| Gateway UI (`http://5.182.17.93:18789`) | OpenClaw `main` | gateway token (`SECRETS.md`) | web ingress / status surface | medium | `hq-router` only |
| CLI runner paths (`run-codex-oauth-agent.sh`, `run-claude-agent.sh`) | approved team leads only | local OS auth + runner creds | trusted internal delegation | low | approved team leads only |

## 6. Tool map

| Tool / integration | Current user | Purpose | Runtime | Secret dependency | Tenant sensitivity | Proposed future location |
|---|---|---|---|---|---|---|
| GitHub | Codex OAuth majors, Claude workers, automation scripts | repo write, PR, CI, issue/workflow automation | Codex OAuth / Claude Code / GitHub Actions | yes: app/PAT/deploy creds | high | GoClaw control plane + deterministic runtime |
| Notion | office, R&D, automation, CRM agents; AX owner-absence canonical | DB/wiki CRUD, operational records | Codex OAuth / Claude Code / n8n | yes: Notion integration token | medium | MCP adapter + n8n webhook flow |
| Google Drive | secretary/content/education agents (document work) | Docs/Slides/Sheets fetch and edits | Claude Code / Codex via MCP | yes: Google OAuth | medium | MCP adapter |
| Google Sheets | sem/sem_r and ops reporting flows | estimates, tabular ops, metrics | Claude Code / deterministic runtime | yes: Google OAuth | medium | MCP adapter |
| Slack | nearly all department agents + approval workflow | ingress, department reporting, alert mirrors | OpenClaw / Claude Code / n8n | yes: Slack bot/app token | medium | GoClaw ingress + n8n notifications |
| Telegram | public manager ingress, alert mirror, archive source | mobile intake and urgency alerting | OpenClaw / archive cron / Phase A automation | yes: Telegram bot token | medium | isolated legacy ingress + alert mirror only |
| n8n | `hreum`, `butim`, Phase A automation target | webhook orchestration and connector glue | n8n | yes: connector/webhook secrets | medium | deterministic runtime default |
| Make | only legacy/exception path; no equal-first status | ad hoc connector orchestration | Make | yes: connector secrets | medium | retire or keep exception-only |

## 7. Hook map

| Hook name | Current trigger point | Purpose | Fail-open or fail-closed today | Proposed future disposition |
|---|---|---|---|---|
| `claude_post_tool_use_long_task_guard` | Claude Code `post_tool_use` hook | run block/warn rules, scan `/tmp/cc_jobs`, cmux notify, lore logging | mixed: block for matched block-rules, otherwise allow+warn | keep and normalize into canonical guard pack |
| `openclaw_rule_001_no_sync_long_task` | OpenClaw rules-engine after tool planning/execution | block long synchronous waits over cache/session boundary | fail-closed | keep |
| `openclaw_rule_002_no_bg_without_log` | OpenClaw rules-engine after tool planning/execution | block background jobs without `/tmp/cc_jobs` logging markers | fail-closed | keep |
| `openclaw_rule_101_session_start_check` | OpenClaw session-start validation | warn if `/tmp/cc_jobs` scan is skipped after reconnect | fail-open (warn only) | keep and refine into restart checklist |

## 8. Wrapper and script inventory

| File / script | Current path | Invoker | Function | Required secret | Criticality | Keep / rewrite / retire |
|---|---|---|---|---|---|---|
| `run-codex-oauth-agent.sh` | `/home/openclaw/workspace/scripts/server/run-codex-oauth-agent.sh` | approved major team leads only | strict metadata-validated Codex OAuth delegation | Codex OAuth auth + repo/env creds | high | keep |
| `run-claude-agent.sh` | `/home/openclaw/workspace/scripts/server/run-claude-agent.sh` | approved major team leads only | audited Claude Code fallback delegation | Claude Max auth + repo/env creds | high | keep |
| `run-claude.raw` | `/usr/local/bin/run-claude.raw` | wrapper only | raw audited shim for Claude runner | Claude auth | high | keep |
| `run-claude` | `/usr/local/bin/run-claude` | local operators | public guarded Claude entrypoint | Claude auth | medium | keep |
| `approval-workflow.sh` | `/home/openclaw/workspace/scripts/approval-workflow.sh` | `main` / operators | classify L0-L4 approval level and notify Slack | Slack posting creds | high | rewrite after AX matrix enforcement |
| `log-activity.sh` | `/home/openclaw/workspace/scripts/server/log-activity.sh` | wrappers / automation | activity logging by lane | none direct | medium | keep |
| `log-route.sh` | `/home/openclaw/workspace/scripts/server/log-route.sh` | wrappers / automation | delegation route logging and violation capture | none direct | medium | keep |
| `install-claude-guard.sh` | `/home/openclaw/workspace/scripts/server/install-claude-guard.sh` | operator | install local Claude guard/rules pack | none direct | medium | keep |
| `run-claude-logging-patch.sh` | `/home/openclaw/workspace/scripts/server/run-claude-logging-patch.sh` | operator | patch Claude logging/audit behavior | none direct | medium | keep |
| `sync-main-prompts.sh` | `/home/openclaw/workspace/scripts/server/sync-main-prompts.sh` | operator | sync prompt assets to runtime | none direct | medium | keep |
| `heartbeat_checks/*.py` | `/home/openclaw/workspace/scripts/heartbeat_checks/` | cron / heartbeat service | reminder, response tracking, multi-channel checks | Slack/Telegram raw archive access | high | keep |
| `daily_summary.py` | `/home/openclaw/workspace/scripts/daily_summary.py` | cron | summarize Telegram archives via local model | none direct | low | keep |

## 9. Secrets exposure list
R1 = routine secret rotation. R2 = backend or master secret operation (includes age key).
Definitions: AX_AVAILABILITY_AND_RBAC §5.2.

| Secret class | Current storage location | Currently exposed in Git/history/chat | Rotation required | R1 or R2 | Target storage model |
|---|---|---|---|---|---|
| SSH/root password | `SECRETS.md` (gitignored), server-local use | yes — legacy docs indicate prior tracked exposure history; current repo references but does not print value | yes | R1 | SOPS + age |
| gateway token | `SECRETS.md`, OpenClaw runtime | yes — historical context documents reference gateway token presence and old tracked exposure risk | yes | R1 | SOPS + age |
| Slack bot/app tokens | live runtime `openclaw.json` (`root.channels.slack.botToken`, `root.channels.slack.appToken`) + local secret files | yes — channel collision and legacy secret exposure are documented; live runtime confirms one shared Slack bot token and one shared Slack app token for all Slack surfaces | yes | R1 | SOPS + age |
| Telegram bot token | live runtime `openclaw.json` (`root.channels.telegram.botToken`) + local secret files | yes — token collision risk explicitly documented in migration notes; live runtime confirms one shared Telegram bot token across both manager groups | yes | R1 | SOPS + age |
| Notion / Google / third-party API keys | local env / secret files / integration configs | yes — old tracked config/history exposure is documented at migration level | yes | R1 | SOPS + age |
| Codex OAuth auth (`~/.codex/auth.json`) | host-local trusted runner file | no direct Git exposure evidenced in current repo | no immediate rotation unless runner is reprovisioned | R1 | host-local secret store + documented recovery |
| age key itself | not yet adopted in current stack | no current evidence | no (until migration) | R2 | hardware-backed or restricted SOPS age key custody |

Live runtime note (2026-04-20):
- Slack live config contains exactly one `botToken` and one `appToken` under `root.channels.slack`; no per-channel Slack token split is evidenced in the current runtime snapshot.
- Telegram live config contains exactly one `botToken` under `root.channels.telegram`; no per-group Telegram token split is evidenced in the current runtime snapshot.
- 강은구 confirmed the concrete bot identities and chose to reuse these existing tokens for AX after prior-flow retirement rather than minting a new AX-only token set.
- preliminary Track A repo scan across `ax-audit`, `ax_handoff_package`, and `똘똘이mk2` found no tracked `.env*` or `*secret*` files in `ax-audit`/`ax_handoff_package`; in `똘똘이mk2`, `SECRETS.md` exists locally but is gitignored, while `dashboard/.env.example` is tracked.
- Track A finalization (2026-04-26): a deeper history scan of `똘똘이mk2` confirmed a plain-text Slack bot token of the form `xoxb-9849432992692-…` is present in past commits (and is also already self-classified as "재발급 필요" inside the repo's own `SECRETS.md` audit notes). `dashboard/.env.example` itself only carries placeholder values (`changeme`). The previously suspected `src/config.ts` and `src/telegram-bot.ts` paths are no longer in the current tree — the surviving live token-handling surface is the `scripts/heartbeat.py` / `scripts/heartbeat_checks/*.py` family, which reads `OPENCLAW_GATEWAY_TOKEN`, `OPENAI_API_KEY`, and `LIGHTRAG_API_KEY` from environment only (no inlined values).
- Therefore the remaining gate is not "new credential issuance" but `prior-flow retirement + R1 rotation of the exposed Slack bot/app token (and as a precaution, the Telegram bot token) + SOPS+age migration`. R1 rotation is AI-proposer / 강은구-approver per §15.3; it is not a γ gate action.
- Owner decision (2026-04-26): the R1 rotation of the exposed Slack bot/app token and the precautionary Telegram bot rotation will NOT be performed at this time. The exposure is therefore recorded as an Owner-accepted residual risk, and AX cutover continues to reuse the existing tokens. The exposure record above is retained verbatim; future AI proposals must not auto-resurrect this rotation unless a new signal (abuse, unauthorized use, or new policy direction from the Owner) appears. SOPS+age migration of token custody remains a separate scheduled item and is not affected by this decision.

## 10. Missing asset list

| Asset | Why needed | Where expected | Blocking severity | Recovery plan |
|---|---|---|---|---|
| historical 57-skill manifest | historical handoff mentions 57-skill classification, but only later `90 -> 65` mapping evidence is currently recovered | archived handoff / legacy repo / install logs | low | recover later for archival completeness; do not block current-state skill classification on it |
| GitHub branch-protection / rulesets configuration proof | plan-gate is resolved 2026-04-26 by flipping `hakhamsolution/ax-audit` to public; branch-protection API now returns `404 Branch not protected` and rulesets API returns `[]`, confirming API access is restored. The remaining work is to actually configure protection on `main` (require PR review, required status check `validate`, and disallow direct push) so that proposer-approver separation is technically enforced rather than policy-only. | GitHub repository settings | medium | configure `main` branch protection during WB2 with `validate` as a required check; capture settings proof in PHASE0 §14 once applied |
| Slack/Telegram prior-flow retirement proof | representative confirmed existing tokens will be reused, and the current Slack admin-channel target is now confirmed as `#000-대표-똘똘이 (C0ASNEFES4C, permalink https://eunhyebooboo.slack.com/archives/C0ASNEFES4C)`, but AX cutover is not complete until the previous flow is actually retired and the shared-read path is explicitly settled | Slack / Telegram operational runtime | medium | complete prior-flow shutdown, confirm only AX path remains, decide whether DM `D0AS8534L01` stays temporary-only or is replaced by a dedicated shared channel, then store token custody in SOPS+age |

## 11. Skill-by-skill classification table

Evidence basis:
- current recoverable skill surface from `똘똘이mk2/CONTEXT.md`
- local Claude rules-pack skills under `docs/cc-rules-pack/local/claude/skills/`
- operational include docs under `똘똘이mk2/scripts/includes/`
- later skill-mapping snapshot from `똘똘이mk2/docs/HISTORY.md` (`pm-claude-skills (90개) 분석 → 65개 매핑`)

The exact historical "57 skills" manifest referenced in earlier migration notes is still unrecovered, but the table below is sufficient for current-state classification because the recoverable operational surface and a later `90 -> 65` mapping snapshot have both been recovered.

| Skill name | Current owner | Real usage | Target location | Difficulty | Dependencies | Priority | Notes |
|---|---|---|---|---|---|---|---|
| blogwatcher | OpenClaw ready skills (CONTEXT) | blog/channel watch | GoClaw tool | low | HTTP/feed creds if used | P2 | documented in CONTEXT ready skills |
| clawhub | OpenClaw ready skills (CONTEXT) | skill/package install helper | deprecated | low | none | P3 | operator convenience, not target runtime capability |
| coding-agent | OpenClaw ready skills (CONTEXT) | generic coding delegation helper | deprecated | medium | repo/env creds | P3 | superseded by core-agent consolidation |
| github | OpenClaw ready skills (CONTEXT) | GitHub repo/issue/PR operations | MCP adapter | low | GitHub auth | P1 | map to GitHub connector |
| gh-issues | OpenClaw ready skills (CONTEXT) | issue triage automation | deterministic runtime job | medium | GitHub auth | P2 | fold into GitHub Actions or governance jobs |
| healthcheck | OpenClaw ready skills (CONTEXT) | service/health monitoring | deterministic runtime job | low | none or service auth | P1 | align with ops-platform |
| nano-pdf | OpenClaw ready skills (CONTEXT) | PDF generation | GoClaw tool | low | none | P2 | used by sem/chukchuk |
| notion | OpenClaw ready skills (CONTEXT) | Notion CRUD/search | MCP adapter | low | Notion token | P1 | map to Notion connector |
| obsidian | OpenClaw ready skills (CONTEXT) | vault query and note ops | GoClaw tool | medium | vault path/local auth | P2 | currently local-only and partly inactive |
| openai-image-gen | OpenClaw ready skills (CONTEXT) | image generation | GoClaw tool | low | OpenAI API key | P2 | keep as specialized tool |
| openai-whisper-api | OpenClaw ready skills (CONTEXT) | speech-to-text | GoClaw tool | low | OpenAI API key | P2 | keep as specialized tool |
| oracle | OpenClaw ready skills (CONTEXT) | advisory lookup | deprecated | medium | unknown | P3 | no current operational evidence beyond install list |
| skill-creator | OpenClaw ready skills (CONTEXT) | create new skills | deprecated | low | none | P3 | not production runtime capability |
| slack | OpenClaw ready skills (CONTEXT) | Slack send/read ops | MCP adapter | low | Slack token | P1 | map to Slack connector |
| tmux | OpenClaw ready skills (CONTEXT) | terminal session helper | deterministic runtime job | low | host access | P3 | replace with cmux-specific ops runbook |
| trello | OpenClaw ready skills (CONTEXT) | Trello board ops | MCP adapter | medium | Trello token | P3 | no current live use evidenced |
| weather | OpenClaw ready skills (CONTEXT) | weather lookup | GoClaw tool | low | weather API key optional | P3 | low business criticality |
| long-task | local Claude rules pack | background job execution standard | deterministic runtime job | low | host access | P1 | keep; tied to `/tmp/cc_jobs` standard |
| session-recovery | local Claude rules pack | resume/recover prior session state | deterministic runtime job | low | host access | P1 | keep; align with restart checklist |
| cmux-integration | local Claude rules pack | cmux notify and workspace coupling | deterministic runtime job | low | host access | P2 | keep for operator ergonomics |
| tools-brands | scripts/includes | brand guideline fetch/use | GoClaw tool | low | brand store access | P2 | operational include, not independent runtime |
| tools-datalake | scripts/includes | raw/processed/vector store access | GoClaw tool | medium | filesystem access | P1 | supports archive-memory |
| tools-graphiti | scripts/includes | Graphiti memory operations | GoClaw tool | medium | graph store creds | P2 | keep if Graphiti remains active |
| tools-heartbeat | scripts/includes | heartbeat CLI/instructions | deterministic runtime job | low | archive access | P1 | align with ops-platform monitoring |
| tools-legal | scripts/includes | legal reference lookup | GoClaw tool | low | filesystem access | P2 | supports gijun/satssat_r |
| tools-n8n | scripts/includes | n8n workflow operations | MCP adapter | medium | n8n creds | P1 | map to deterministic runtime control |
| tools-notion | scripts/includes | shared Notion API usage pattern | MCP adapter | low | Notion token | P1 | merge with Notion connector guidance |
| tools-obsidian-cli | scripts/includes | local vault query pattern | GoClaw tool | medium | local vault access | P2 | keep but mark local-only |
| tools-pdf | scripts/includes | PDF create/convert pattern | GoClaw tool | low | none | P2 | supports content/sales |
| tools-pptx | scripts/includes | presentation generation pattern | GoClaw tool | low | none | P2 | supports chakchak/chakchak_r |
| tools-replicate | scripts/includes | Replicate image/video generation | GoClaw tool | medium | Replicate API key | P2 | supports kkumi/ssakduk |
| tools-slack | scripts/includes | Slack channel/message rules | MCP adapter | low | Slack token | P1 | current channel taxonomy still needs cleanup |
| tools-wiki | scripts/includes | wiki-agent operations | GoClaw tool | medium | filesystem access | P2 | supports archive-memory |

## 12. Session-truth locations

| System | Stores session truth? | Scope | Backup method | Recovery risk |
|---|---|---|---|---|
| GoClaw / OpenClaw control plane (`/root/.openclaw/openclaw.json`, route logs) | yes | public ingress state, live channel bindings, routing decisions, gateway-facing conversation control; recovered 2026-04-15 audit says `config/*.toml` are partially stale | sanitized runtime snapshot was captured into `AX_PHASE0_MIGRATION_ARTIFACTS` §9; future sessions should refresh it when runtime changes materially | high |
| Codex OAuth plane | partial yes | major-agent execution context, OAuth runner identity, repo worktrees | host-local auth file + repo history; no dedicated session backup evidenced | medium |
| Claude Code worker plane | yes | per-worker local context, `/tmp/cc_jobs`, wrapper audit trail | local lore/hooks + repo/log files; no central backup evidenced | medium |
| Hermes | yes | long-running deep-work and memory experiments | local service + host filesystem only | medium-high |
| deterministic runtime (`n8n`, cron, systemd`) | partial yes | workflow state, schedules, reminders, archive ingestion | cron manifests and runtime configs; n8n export not yet captured | medium |
| legacy bot / Telegram archive path | yes | message history and fallback ingress traces | daily archive files + NAS backup path documented in `HISTORY.md` | medium |

## 13. Current fallback paths

| Failure case | Current fallback exists? | Trigger | Human owner | Safe? | Proposed future fallback |
|---|---|---|---|---|---|
| GoClaw unavailable ≥10 minutes | yes | degraded-mode declaration per RBAC §4 | Operator | partial — requires verified token/channel isolation | pre-approved isolated legacy intake path |
| Codex OAuth runner unavailable | yes | wrapper validation failure or auth/runtime outage | team lead / Operator | yes | audited `run-claude-agent.sh` fallback |
| Claude long task exceeds session TTL | yes | long synchronous wait or disconnect risk | operator / local worker | yes | `/tmp/cc_jobs` + cmux notify standard |
| Notion canonical unavailable | yes | Notion outage / API failure | Owner / Deputy Owner | yes | Git as primary canonical |
| Git canonical unavailable | yes | repo/push credential outage | Owner / Deputy Owner | yes | Notion as primary canonical |
| Both canonicals unavailable | yes | dual outage | Owner / Deputy Owner | partial | temporary Slack/Telegram record then backfill within 24h |
| Hermes unavailable | yes | local service failure | Operator | yes | keep Hermes disconnected from public ingress; no production dependency |

## 14. Current approval paths

| Action | Current approver | Current method | Logged? | Proposer type today | Proposed future approver |
|---|---|---|---|---|---|
| promote automation | 강은구 | GitHub PR + written approval intended; CI execution unblocked (self-hosted runner verified 2026-04-25), and plan-gate resolved by 2026-04-26 public-flip; protection on `main` is now configurable but not yet configured — PR-only enforcement remains policy-only until WB2 applies the protection ruleset | partial | AI | 강은구 |
| demote automation | 강은구 | PR + written approval intended; active-failure containment demotion may proceed first and be reviewed afterward | partial | AI / mixed | 강은구 |
| rotate secrets R1 | 강은구 | runbook + secret-store action with Owner approval | partial | AI / mixed | 강은구 |
| rotate secrets R2 | 강은구 | γ gate required: AI proposal + independent AI review + Owner approval; backend not yet migrated | partial | AI | 강은구 |
| restart services | 강은구 (Operator emergency path exists) | direct host action under documented runbook; retrospective log required if taken as emergency containment | partial | AI / Operator | 강은구 |
| change guard rule | 강은구 | intended PR + independent AI review; plan-gate resolved 2026-04-26, but technical enforcement on `main` is still policy-only until WB2 applies branch-protection requiring PR review + reviewer comment | partial | AI | 강은구 |
| change architecture definition | 강은구 | ADR/doc PR + independent AI review before approval | yes | AI | 강은구 |

Recovered current-channel routing note:
- `approval-workflow.sh` routes L1 -> `#999-컨퍼런스`, L2 -> `#003-간부회의`, and L3/L4 -> `#000-대표-똘똘이`
- this supports using `#000-대표-똘똘이` as the present Slack admin escalation surface until a newer runtime export proves otherwise

## 15. Current humans and privileges — FILLED (Decision 15 aligned)

Confirmation source: Owner decision recorded 2026-04-18 and package-v2 supersession set adopted on 2026-04-20.

### 15.1 Canonical humans table

| Human | Current effective privileges | Formal role today | System role assignment | Practical exercise | Business-side role | Notes |
|---|---|---|---|---|---|---|
| 강은구 | full — production secret store access, GoClaw/OpenClaw host deploy-restart, guard-rule repository access, Class C·D tenant data access, GitHub repo administration, automation approval | 대표 | Owner · Approver · Operator | operational | — | sole operational Approver; current GitHub hosting plan prevents proving technical branch-protection enforcement |
| 원혜연 | broad read/write access still remains on some legacy system surfaces; exact platform-by-platform reduction proof is not yet exported | 대표 | Deputy Owner (dormant) · Approver (formal) · Operator (available) | dormant for system governance in normal operation | Business Work Partner: accept/reject/modify work assignments | current access realignment remains a WB2 task; daily governance authority is intentionally not exercised |

### 15.2 Role assignment summary

- Owner (operational): 강은구
- Deputy Owner (dormant, formal only): 원혜연
- Approver (operational): 강은구
- Approver (formal, dormant): 원혜연
- Operator (primary): 강은구
- Operator (available): 원혜연
- Business Work Partner: 원혜연
- Requester: either human when requesting work

Proposer-approver separation is satisfied by design only when AI proposes and 강은구 approves. The remaining gap is technical enforcement, not role definition.

### 15.3 Proposer-approver separation register

| Action class | Proposer (default) | Reviewer (default, γ gate only) | Approver | Audit check |
|---|---|---|---|---|
| promote_automation | Codex | — | 강은구 | proposer ≠ approver |
| demote_automation | Codex | — | 강은구 | same; active-failure containment exception logged |
| R1 rotate_secret | Codex | — | 강은구 | same |
| R2 rotate_secret | Codex | Claude Code | 강은구 | γ gate complete |
| change_guard_rule | Codex | Claude Code | 강은구 | γ gate complete |
| change_secret_backend | Codex | Claude Code | 강은구 | γ gate complete |
| retire_legacy_component | Codex | Claude Code | 강은구 | γ gate complete |
| change_architecture_definition | Codex | Claude Code | 강은구 | γ gate complete |

Manual override tracker: any action in the above classes executed without going through the proposer pipeline must be logged here with rationale. Empty at current evidence cut.

| Date | Action class | Override actor | Rationale | Resolution |
|---|---|---|---|---|
| _(empty)_ |  |  |  |  |

### 15.4 Owner-absence declaration log destination — CONFIRMED

Owner decision 2026-04-18: γ two-canonical + two alert mirrors.

| Destination | Role |
|---|---|
| Notion database | canonical — structured |
| Git append-only file | canonical — immutable |
| Slack admin channel | alert mirror (not audit evidence) |
| Telegram | alert mirror (not audit evidence) |

Conflict resolution by later append timestamp; discrepancies are audit incidents reviewed by governance-audit.

Full policy: `AX_OWNER_ABSENCE_LOG_DESTINATION_POLICY` v3.

Automation status:
- Phase A (Notion → Git, Slack, Telegram one-way sync): target within 30 days of activation (deadline 2026-05-19)
- Phase B (two-way sync with conflict detection): target within 60 days of activation (deadline 2026-06-18)
- Interim: manual dual-canonical entry required within the policy sync window

### 15.5 AI agents and effective privileges

Every AI agent that can read secrets, write repos/docs, or trigger privileged actions must appear here.

| Agent | Runtime | Effective tool access | Secret read access | Write access scope | AX role (proposer / reviewer / neither) | Self-approval path possible? | Proposed future restriction |
|---|---|---|---|---|---|---|---|
| Codex | Codex OAuth trusted runner | repo shell, git push, GitHub/Notion/Google/Slack connectors when invoked, automation design | yes — `~/.codex/auth.json` plus delegated env creds | repos, workflow artifacts, Git canonical, selected connector-backed records | proposer | yes — current repo still permits direct push because branch protection is plan-gated | keep to approved trusted runners only; enforce PR-only once hosting gate is resolved |
| Claude Code reviewer lane | guarded Claude worker plane | repo shell, review comments, local hooks, selected connectors | yes — worker env and delegated connector creds | repos, docs, internal reports | reviewer | yes — technical direct-write path exists on legacy surfaces even though reviewer role should not use it | distinct session/context only; no production promotion path |
| n8n workflow runners | deterministic runtime | webhook ingestion, connector glue, outbound notifications | yes — workflow secrets and webhook secrets | Notion/Git/Slack/Telegram sync actions | proposer (narrow, per workflow) | yes — if promoted without PR artifact or isolated runtime review | require exported workflow review, promote_automation approval, and explicit audit logging |
| OpenClaw public/control-plane agents (`main`, `jarvis`, team leads) | OpenClaw | ingress, routing, archive polling, Slack/Telegram messaging | yes — gateway token, model creds, shared channel creds | routing logs, archive state, alerts, manager-channel responses | neither | yes — current legacy runtime still has direct messaging authority on shared credentials | isolate public ingress to `hq-router`; remove privileged config mutation from legacy lanes |
| Heartbeat / cron archive jobs | cron / helper scripts | reminders, archive polling, summary generation | yes — archive and channel creds | reminders, archive-derived reports | neither | no direct approval path evidenced, but can post operator-facing messages | keep deterministic only; no privileged mutation role |
| Hermes | local Hermes runtime | long-running deep work, local memory, experimental tasks | no direct secret read evidenced | local experimental artifacts only | neither | no current privileged path evidenced | keep non-public and non-canonical until explicit approval |

### 15.6 Immediate follow-up actions from filled §15

1. Complete WB2 access realignment for 원혜연: keep business-side write paths where required, but reduce governance surfaces to read or approval-only where policy demands.
2. Establish and preserve an independent Claude Code reviewer session for γ gate actions; reviewer and proposer must remain distinct sessions with distinct context.
3. Configure `main` branch protection on the now-public `hakhamsolution/ax-audit` so PR-only enforcement is technical rather than policy-only. Required-check baseline: `validate` (the existing self-hosted-runner job). This is the first concrete WB2 deliverable.
4. Slack/Telegram cutover stance is now finalized by Owner decision (2026-04-26): the exposed Slack bot/app token (and the precautionary Telegram bot token) will NOT be rotated at this time. The exposure is recorded as Owner-accepted residual risk and AX cutover continues to reuse the existing tokens. PHASE0 §9 retains the exposure record; future AI-proposed rotation must not be auto-suggested unless new signal (e.g., abuse, unauthorized use) appears.
5. Continue Phase A owner-absence automation build only under the proposer-approver pipeline.
6. Keep the Notion operational DB title mismatch (`AX 소유자 부재 신고` vs package-v2 canonical English title) as an explicit reconciliation item rather than silently renaming it.

## 16. Exit criteria for Phase 0

Phase 0 is complete only when:
- every currently active channel has an owner — **done for recovered current-state mapping (§5); sanitized live token/app binding evidence is captured**
- every current secret has a known storage location and an R1/R2 classification — **partial (§9 classified major secret classes and live runtime paths; current runtime still uses shared Slack/Telegram credentials and console-level custody records remain incomplete)**
- every current critical script is inventoried — **done (§8)**
- every current agent has a target-state disposition — **done (§4)**
- every current skill has a target-location classification — **done (§11 for current recoverable surface; historical manifest gap is archival only)**
- every known missing asset has a blocking severity — **done (§10)**
- token collision risks are explicitly listed — **done (§5, §9)**
- approval paths and privilege paths are written down — **done (§14, §15)**
- role assignment is documented for Owner / Deputy Owner / Approver / Operator — **done (§15.2)**
- the Owner-absence declaration mechanism is documented and has a log destination in the central audit log — **done (§15.4; broadcast automation still pending)**
- the proposer-approver separation register is populated for privileged action classes — **done (§15.3)**
- AI agents with privileged access are inventoried — **done (§15.5)**

## 17. Instruction to future sessions

Do not skip this document.
If someone asks for migration planning without a completed Phase 0 inventory, the correct response is to say the migration is still evidence-incomplete.

As of 2026-04-20, §§4–15.5 are populated from the current recoverable evidence set and are re-aligned to the package-v2 Decision 15 baseline.
As of 2026-04-26: the GitHub Actions billing gate is resolved by self-hosted runner cutover; the GitHub plan-gate is resolved by Owner-approved public-flip of `hakhamsolution/ax-audit` and verified via the now-200/`[]` responses from the branch-protection and rulesets APIs; Track A is finalized with a confirmed Slack bot-token exposure in `똘똘이mk2` history but the Owner has explicitly elected NOT to rotate the exposed token, so the exposure is now an Owner-accepted residual risk rather than a pending rotation task; the remaining hosting work is to actually configure `main` branch protection during WB2 with the `validate` job as a required check; Slack/Telegram prior-flow retirement is still pending; and a few non-blocking historical archival gaps remain as listed in §10 and §16.
