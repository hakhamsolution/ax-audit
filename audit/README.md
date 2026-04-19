# audit/owner_absence

This directory hosts the **Git canonical** of the Owner-absence declaration log for the AX system.

This is one of two canonical stores. The other is the Notion database `AX Owner Absence Declarations`. Both canonicals must contain the same records. See `AX_OWNER_ABSENCE_LOG_DESTINATION_POLICY v2` for the consistency rules.

## Files

- `owner_absence.jsonl` — append-only JSONL; one declaration record per line (or one update-line per edit per §5.5 of the schema design)
- `owner_absence.schema.json` — JSON Schema v1.0 for validating records
- `README.md` — this file

## Writing a new declaration

Only Owner or Deputy Owner may write. Automation may sync from Notion.

1. Construct the record conforming to `owner_absence.schema.json`.
2. Append as a single JSONL line to `owner_absence.jsonl`.
3. Commit via a branch + PR. Direct pushes to main are disallowed.
4. PR is reviewed by the non-proposer (self-approval rule).
5. After merge, verify the Notion canonical contains the same record.

## Updating an existing declaration

Updates are allowed only for the mutable fields listed in `AX_OWNER_ABSENCE_LOG_SCHEMA_DESIGN §3 R7`:

- expected_end_time
- ratification_status
- ratified_at
- linked_actions (append only)
- sync_state
- last_updated_at

To update, append a **new line** with the same `declaration_id` and the updated values. Never modify an existing line. The reader rule is: the line with the latest `last_updated_at` is the authoritative version.

## Append-only enforcement

Three layers, defense in depth:

1. Protected branch + PR-only merges
2. Pre-commit hook that rejects modification of existing lines
3. CI validation that re-checks on every PR

Layers 2 and 3 are implemented as a follow-up task. Until they exist, append-only discipline is enforced by PR review and by this README.

## Schema migrations

A schema version bump (e.g. 1.0 → 1.1) is a four-eyes-required action per `AX_OWNER_ABSENCE_LOG_SCHEMA_DESIGN §7`. Migration notes are appended here.

### Migration log

- 2026-04-18: schema v1.0 initialized.

## Do not

- Do not delete this file.
- Do not rewrite history with `git rebase -i`, `git filter-branch`, or `git push --force` on the `audit/` directory.
- Do not bypass PR review for declarations made under Owner-absence.
- Do not treat this Git store as the only canonical. Notion is equally canonical and must be kept aligned.
