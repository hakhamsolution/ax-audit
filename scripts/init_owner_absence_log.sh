#!/usr/bin/env bash
# init_owner_absence_log.sh
# Purpose: initialize the Git canonical of the Owner-absence declaration log
# per AX_OWNER_ABSENCE_LOG_SCHEMA_DESIGN v1 §5 and §8.
#
# Usage:
#   cd <your audit-hosting repository root>
#   bash init_owner_absence_log.sh
#
# Behavior:
#   - creates audit/ directory if missing
#   - creates audit/owner_absence.jsonl as an empty file (never overwrites if present)
#   - creates audit/owner_absence.schema.json with the schema v1.0 JSON Schema
#   - creates audit/README.md with usage notes
#   - stages the files with git add (does NOT commit — commit is a four-eyes action)
#
# Safety:
#   - refuses to run if audit/owner_absence.jsonl already exists and is non-empty
#   - refuses to run outside a git repository
#   - prints what it did; makes no irreversible change beyond file creation

set -euo pipefail

SCHEMA_VERSION="1.0"
AUDIT_DIR="audit"
DATA_FILE="${AUDIT_DIR}/owner_absence.jsonl"
SCHEMA_FILE="${AUDIT_DIR}/owner_absence.schema.json"
README_FILE="${AUDIT_DIR}/README.md"

log() { printf '[init] %s\n' "$*"; }
fail() { printf '[init][error] %s\n' "$*" >&2; exit 1; }

# Precondition: inside a git repo
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  fail "not inside a git repository; cd into the audit-hosting repo first"
fi

# Precondition: don't clobber existing data
if [[ -f "${DATA_FILE}" ]]; then
  if [[ -s "${DATA_FILE}" ]]; then
    fail "${DATA_FILE} already exists and is non-empty; aborting to avoid data loss"
  else
    log "${DATA_FILE} exists but is empty; leaving as is"
  fi
fi

mkdir -p "${AUDIT_DIR}"

# Data file (empty)
if [[ ! -f "${DATA_FILE}" ]]; then
  : > "${DATA_FILE}"
  log "created empty ${DATA_FILE}"
fi

# Schema file
cat > "${SCHEMA_FILE}" <<'JSON'
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://ax.internal/schemas/owner_absence/1.0",
  "title": "AX Owner Absence Declaration",
  "description": "Schema v1.0 for Owner-absence declaration records. See AX_OWNER_ABSENCE_LOG_SCHEMA_DESIGN §2-3.",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "declaration_id",
    "schema_version",
    "declared_by",
    "declared_by_name",
    "start_time",
    "open_ended",
    "trigger_condition",
    "response_window_used",
    "scope",
    "ratification_status",
    "linked_actions",
    "canonical_source",
    "sync_state",
    "created_at",
    "last_updated_at"
  ],
  "properties": {
    "declaration_id": {
      "type": "string",
      "pattern": "^OA-\\d{8}-\\d{3}$"
    },
    "schema_version": {
      "type": "string",
      "const": "1.0"
    },
    "declared_by": {
      "type": "string",
      "enum": ["owner", "deputy_owner"]
    },
    "declared_by_name": {
      "type": "string",
      "minLength": 1
    },
    "start_time": {
      "type": "string",
      "format": "date-time"
    },
    "expected_end_time": {
      "type": ["string", "null"],
      "format": "date-time"
    },
    "open_ended": {
      "type": "boolean"
    },
    "trigger_condition": {
      "type": "string",
      "enum": ["planned_leave", "incapacitated", "unreachable", "explicit_delegation"]
    },
    "response_window_used": {
      "type": "string",
      "enum": ["general", "emergency", "overnight_non_emergency"]
    },
    "scope": {
      "type": "string",
      "pattern": "^(full|partial:.+)$"
    },
    "ratification_status": {
      "type": "string",
      "enum": ["pending", "ratified", "reversed"]
    },
    "ratified_at": {
      "type": ["string", "null"],
      "format": "date-time"
    },
    "linked_actions": {
      "type": "array",
      "items": { "type": "string" }
    },
    "canonical_source": {
      "type": "string",
      "enum": ["notion", "git"]
    },
    "sync_state": {
      "type": "string",
      "enum": ["pending", "synced", "conflict"]
    },
    "created_at": {
      "type": "string",
      "format": "date-time"
    },
    "last_updated_at": {
      "type": "string",
      "format": "date-time"
    }
  },
  "allOf": [
    {
      "description": "R2: open_ended and expected_end_time are mutually exclusive",
      "if": { "properties": { "open_ended": { "const": true } } },
      "then": { "properties": { "expected_end_time": { "type": "null" } } },
      "else": { "properties": { "expected_end_time": { "type": "string", "format": "date-time" } } }
    },
    {
      "description": "R3: ratification_status and ratified_at consistency",
      "if": { "properties": { "ratification_status": { "const": "pending" } } },
      "then": { "properties": { "ratified_at": { "type": "null" } } },
      "else": { "properties": { "ratified_at": { "type": "string", "format": "date-time" } } }
    }
  ]
}
JSON
log "wrote ${SCHEMA_FILE}"

# README
cat > "${README_FILE}" <<'MARKDOWN'
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
MARKDOWN
log "wrote ${README_FILE}"

# Stage
git add "${AUDIT_DIR}/"
log "staged ${AUDIT_DIR}/ for commit"

cat <<EOF

Next steps (run manually so the commit is attributable):

  git commit -m "audit: initialize owner-absence declaration log (schema v${SCHEMA_VERSION})"
  git push origin <your branch>
  open a PR and request review from the non-proposer

Schema version initialized: ${SCHEMA_VERSION}
Files ready:
  ${DATA_FILE}     (empty)
  ${SCHEMA_FILE}   (v${SCHEMA_VERSION})
  ${README_FILE}

EOF
