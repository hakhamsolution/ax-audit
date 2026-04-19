#!/usr/bin/env python3
"""
validate_owner_absence.py

Validate the append-only owner-absence JSONL file and individual records
against schema v1.0 rules. The script uses the canonical JSON Schema file as
the source for required fields and property order, but performs the rule checks
locally so it does not depend on third-party packages.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

DECLARATION_ID_RE = re.compile(r"^OA-\d{8}-\d{3}$")
SCOPE_RE = re.compile(r"^(full|partial:.+)$")
DECLARED_BY = {"owner", "deputy_owner"}
TRIGGER_CONDITIONS = {
    "planned_leave",
    "incapacitated",
    "unreachable",
    "explicit_delegation",
}
RESPONSE_WINDOWS = {"general", "emergency", "overnight_non_emergency"}
RATIFICATION_STATES = {"pending", "ratified", "reversed"}
CANONICAL_SOURCES = {"notion", "git"}
SYNC_STATES = {"pending", "synced", "conflict"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate AX owner-absence records.")
    parser.add_argument(
        "--data-file",
        default="audit/owner_absence.jsonl",
        help="JSONL file to validate.",
    )
    parser.add_argument(
        "--schema-file",
        default="audit/owner_absence.schema.json",
        help="Canonical JSON Schema file.",
    )
    parser.add_argument(
        "--against-ref",
        help="Optional git ref for append-only prefix validation (for example: HEAD or origin/main).",
    )
    parser.add_argument(
        "--record-file",
        help="Validate a single record from a JSON file instead of the JSONL log.",
    )
    parser.add_argument(
        "--record-stdin",
        action="store_true",
        help="Validate a single JSON record read from stdin.",
    )
    return parser.parse_args()


def load_schema(schema_file: str) -> dict[str, Any]:
    path = Path(schema_file)
    if not path.is_file():
        raise FileNotFoundError(f"schema file not found: {schema_file}")
    with path.open("r", encoding="utf-8") as handle:
        schema = json.load(handle)
    if not isinstance(schema, dict):
        raise ValueError("schema root must be an object")
    return schema


def parse_datetime(value: str, field_name: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string date-time")
    candidate = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError as exc:
        raise ValueError(f"{field_name} must be RFC3339-compatible: {value}") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{field_name} must include an explicit timezone offset")
    return parsed


def ordered_record(record: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    properties = schema.get("properties", {})
    ordered: dict[str, Any] = {}
    for key in properties:
        if key in record:
            ordered[key] = record[key]
    for key, value in record.items():
        if key not in ordered:
            ordered[key] = value
    return ordered


def dump_record(record: dict[str, Any], schema: dict[str, Any]) -> str:
    return json.dumps(
        ordered_record(record, schema),
        ensure_ascii=False,
        separators=(",", ":"),
    )


def validate_record(record: dict[str, Any], schema: dict[str, Any], source: str) -> list[str]:
    errors: list[str] = []
    properties = schema.get("properties", {})
    required = set(schema.get("required", []))

    if not isinstance(record, dict):
        return [f"{source}: record must be a JSON object"]

    missing = sorted(required - set(record))
    if missing:
        errors.append(f"{source}: missing required fields: {', '.join(missing)}")

    extra = sorted(set(record) - set(properties))
    if extra:
        errors.append(f"{source}: unexpected fields: {', '.join(extra)}")

    def require_string(field: str) -> str | None:
        value = record.get(field)
        if value is None:
            return None
        if not isinstance(value, str):
            errors.append(f"{source}: {field} must be a string")
            return None
        return value

    declaration_id = require_string("declaration_id")
    if declaration_id and not DECLARATION_ID_RE.fullmatch(declaration_id):
        errors.append(f"{source}: declaration_id must match OA-YYYYMMDD-NNN")

    schema_version = require_string("schema_version")
    if schema_version and schema_version != "1.0":
        errors.append(f"{source}: schema_version must be exactly 1.0")

    declared_by = require_string("declared_by")
    if declared_by and declared_by not in DECLARED_BY:
        errors.append(f"{source}: declared_by must be one of {sorted(DECLARED_BY)}")

    declared_by_name = require_string("declared_by_name")
    if declared_by_name is not None and not declared_by_name.strip():
        errors.append(f"{source}: declared_by_name must not be empty")

    trigger_condition = require_string("trigger_condition")
    if trigger_condition and trigger_condition not in TRIGGER_CONDITIONS:
        errors.append(
            f"{source}: trigger_condition must be one of {sorted(TRIGGER_CONDITIONS)}"
        )

    response_window = require_string("response_window_used")
    if response_window and response_window not in RESPONSE_WINDOWS:
        errors.append(
            f"{source}: response_window_used must be one of {sorted(RESPONSE_WINDOWS)}"
        )

    scope = require_string("scope")
    if scope and not SCOPE_RE.fullmatch(scope):
        errors.append(f"{source}: scope must be `full` or start with `partial:`")

    ratification_status = require_string("ratification_status")
    if ratification_status and ratification_status not in RATIFICATION_STATES:
        errors.append(
            f"{source}: ratification_status must be one of {sorted(RATIFICATION_STATES)}"
        )

    canonical_source = require_string("canonical_source")
    if canonical_source and canonical_source not in CANONICAL_SOURCES:
        errors.append(
            f"{source}: canonical_source must be one of {sorted(CANONICAL_SOURCES)}"
        )

    sync_state = require_string("sync_state")
    if sync_state and sync_state not in SYNC_STATES:
        errors.append(f"{source}: sync_state must be one of {sorted(SYNC_STATES)}")

    open_ended = record.get("open_ended")
    if open_ended is not None and type(open_ended) is not bool:
        errors.append(f"{source}: open_ended must be a boolean")

    linked_actions = record.get("linked_actions")
    if linked_actions is not None:
        if not isinstance(linked_actions, list) or not all(
            isinstance(item, str) for item in linked_actions
        ):
            errors.append(f"{source}: linked_actions must be an array of strings")

    for field in ("start_time", "created_at", "last_updated_at"):
        value = record.get(field)
        if value is None:
            continue
        try:
            parse_datetime(value, field)
        except ValueError as exc:
            errors.append(f"{source}: {exc}")

    expected_end_time = record.get("expected_end_time")
    if open_ended is True:
        if expected_end_time is not None:
            errors.append(f"{source}: expected_end_time must be null when open_ended=true")
    elif open_ended is False:
        if not isinstance(expected_end_time, str):
            errors.append(
                f"{source}: expected_end_time must be a string date-time when open_ended=false"
            )
        else:
            try:
                parse_datetime(expected_end_time, "expected_end_time")
            except ValueError as exc:
                errors.append(f"{source}: {exc}")
    elif "open_ended" in record:
        # The type error above already captures non-bool values.
        pass

    ratified_at = record.get("ratified_at")
    if ratification_status == "pending":
        if ratified_at is not None:
            errors.append(f"{source}: ratified_at must be null when ratification_status=pending")
    elif ratification_status in {"ratified", "reversed"}:
        if not isinstance(ratified_at, str):
            errors.append(
                f"{source}: ratified_at must be a string date-time when ratification_status is not pending"
            )
        else:
            try:
                parse_datetime(ratified_at, "ratified_at")
            except ValueError as exc:
                errors.append(f"{source}: {exc}")

    return errors


def load_record_from_text(text: str, source: str) -> dict[str, Any]:
    try:
        record = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{source}: invalid JSON: {exc}") from exc
    if not isinstance(record, dict):
        raise ValueError(f"{source}: JSON root must be an object")
    return record


def load_single_record(args: argparse.Namespace) -> tuple[str, dict[str, Any]] | None:
    if args.record_file:
        text = Path(args.record_file).read_text(encoding="utf-8")
        return args.record_file, load_record_from_text(text, args.record_file)
    if args.record_stdin:
        text = sys.stdin.read().strip()
        if not text:
            raise ValueError("stdin record is empty")
        return "stdin", load_record_from_text(text, "stdin")
    return None


def load_jsonl_records(data_file: str) -> list[tuple[int, dict[str, Any]]]:
    path = Path(data_file)
    if not path.is_file():
        raise FileNotFoundError(f"data file not found: {data_file}")
    records: list[tuple[int, dict[str, Any]]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line:
                continue
            records.append((line_number, load_record_from_text(line, f"{data_file}:{line_number}")))
    return records


def validate_jsonl_file(data_file: str, schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    latest_by_declaration: dict[str, datetime] = {}
    for line_number, record in load_jsonl_records(data_file):
        source = f"{data_file}:{line_number}"
        record_errors = validate_record(record, schema, source)
        errors.extend(record_errors)
        if record_errors:
            continue
        declaration_id = str(record["declaration_id"])
        last_updated_at = parse_datetime(str(record["last_updated_at"]), "last_updated_at")
        previous = latest_by_declaration.get(declaration_id)
        if previous is not None and last_updated_at <= previous:
            errors.append(
                f"{source}: last_updated_at must strictly increase for declaration_id {declaration_id}"
            )
        latest_by_declaration[declaration_id] = last_updated_at
    return errors


def git_repo_root_for(path: Path) -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=path.parent,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError("not inside a git repository")
    return Path(result.stdout.strip())


def check_append_only(data_file: str, against_ref: str) -> list[str]:
    path = Path(data_file).resolve()
    repo_root = git_repo_root_for(path)
    relative = path.relative_to(repo_root).as_posix()
    result = subprocess.run(
        ["git", "show", f"{against_ref}:{relative}"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        stderr = result.stderr.lower()
        if "exists on disk, but not in" in stderr or "path '" in stderr and "does not exist" in stderr:
            old_lines: list[str] = []
        else:
            return [f"append-only check failed to read {against_ref}:{relative}: {result.stderr.strip()}"]
    else:
        old_lines = result.stdout.splitlines()

    new_lines = path.read_text(encoding="utf-8").splitlines()
    if len(new_lines) < len(old_lines):
        return [f"append-only violation: {relative} has fewer lines than {against_ref}"]

    for index, old_line in enumerate(old_lines):
        if new_lines[index] != old_line:
            return [
                "append-only violation: existing content changed before file end "
                f"(first mismatch at line {index + 1})"
            ]
    return []


def main() -> int:
    args = parse_args()
    schema = load_schema(args.schema_file)

    single_record = load_single_record(args)
    errors: list[str] = []

    if single_record is not None:
        source, record = single_record
        errors.extend(validate_record(record, schema, source))
        if not errors:
            print(f"[validate] ok: single record from {source}")
    else:
        errors.extend(validate_jsonl_file(args.data_file, schema))
        if args.against_ref:
            errors.extend(check_append_only(args.data_file, args.against_ref))
        if not errors:
            record_count = len(load_jsonl_records(args.data_file))
            print(
                "[validate] ok: "
                f"{args.data_file} ({record_count} record lines)"
                + (f", append-only verified against {args.against_ref}" if args.against_ref else "")
            )

    if errors:
        for error in errors:
            print(f"[validate][error] {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
