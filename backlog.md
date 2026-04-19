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

_(empty — append as found; these are human-in-the-loop gates not anticipated in the handoff §8 table)_

## access_realignment_log

_(empty — populate during WB2; one line per access change with before/after)_

## operational_bookmarks

- notion_database_id: _(populate after WB1 Track C)_
- notion_integration_name: _(populate after WB1 Track C)_
- audit_repo_url: _(populate after WB1 Track B)_
- owner_absence_log_path_git: `audit/owner_absence.jsonl`
- slack_admin_channel: _(populate during WB1 Track C)_
- telegram_admin_endpoint: _(populate during WB1 Track C)_

## gaps_at_handoff

- 2026-04-18: `docs/active/AX_GUARD_FAILMODE_AND_RUNTIME_POLICY.md` (v1) is referenced by `AX_SUPERSESSION_AND_NAMING_NOTICE.md` §1 and by `docs/handoff/AX_HANDOFF_TO_CLAUDE_CODE.md` §5 but is not present in this handoff package. It was authored in an earlier session. Recovery: retrieve from prior chat export, original working copy, or the Anthropic session history. Until restored, fall back to `AX_OPERATIONS_POLICY.md` §7 (which summarizes guard policy at a higher level) and do not design guard logic from scratch — that would be scope expansion.

## cycle_log

- 2026-04-18: cycle opened; WB1 scheduled.
- 2026-04-18: handoff package assembled; one document gap noted (see gaps_at_handoff).
