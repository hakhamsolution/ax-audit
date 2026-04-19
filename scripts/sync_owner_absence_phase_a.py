#!/usr/bin/env python3
"""
sync_owner_absence_phase_a.py

Phase A helper for owner-absence records:
- validate a single record against schema v1.0
- append it to the Git canonical when applying
- fan out alert messages to Slack / Telegram when configured

The script intentionally does not read Notion directly. It consumes a normalized
record payload so it can be wired from n8n, Make, manual export, or a future
Notion-triggered bridge.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any
from urllib import error, parse, request

from validate_owner_absence import (
    dump_record,
    load_jsonl_records,
    load_record_from_text,
    load_schema,
    ordered_record,
    parse_datetime,
    validate_record,
)

SLACK_WEBHOOK_ENV = "OWNER_ABSENCE_SLACK_WEBHOOK_URL"
TELEGRAM_BOT_TOKEN_ENV = "OWNER_ABSENCE_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID_ENV = "OWNER_ABSENCE_TELEGRAM_CHAT_ID"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Phase A owner-absence sync helper.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--record-file", help="Path to a single JSON record file.")
    group.add_argument("--record-json", help="Inline JSON string containing one record.")
    group.add_argument(
        "--record-stdin",
        action="store_true",
        help="Read one JSON record from stdin.",
    )
    parser.add_argument(
        "--data-file",
        default="audit/owner_absence.jsonl",
        help="Git canonical JSONL file.",
    )
    parser.add_argument(
        "--schema-file",
        default="audit/owner_absence.schema.json",
        help="Canonical JSON Schema file.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply append/send actions. Without this flag the script stays in dry-run mode.",
    )
    parser.add_argument(
        "--skip-alerts",
        action="store_true",
        help="Skip Slack/Telegram fanout even in apply mode.",
    )
    parser.add_argument(
        "--slack-webhook-url",
        help=f"Slack webhook URL. Defaults to ${SLACK_WEBHOOK_ENV} if unset.",
    )
    parser.add_argument(
        "--telegram-bot-token",
        help=f"Telegram bot token. Defaults to ${TELEGRAM_BOT_TOKEN_ENV} if unset.",
    )
    parser.add_argument(
        "--telegram-chat-id",
        help=f"Telegram chat id. Defaults to ${TELEGRAM_CHAT_ID_ENV} if unset.",
    )
    return parser.parse_args()


def load_input_record(args: argparse.Namespace) -> dict[str, Any]:
    if args.record_file:
        text = Path(args.record_file).read_text(encoding="utf-8")
        return load_record_from_text(text, args.record_file)
    if args.record_json:
        return load_record_from_text(args.record_json, "inline-json")
    text = sys.stdin.read().strip()
    if not text:
        raise ValueError("stdin record is empty")
    return load_record_from_text(text, "stdin")


def find_latest_record(data_file: str, declaration_id: str) -> dict[str, Any] | None:
    latest_record: dict[str, Any] | None = None
    latest_time = None
    if not Path(data_file).exists():
        return None

    for _, record in load_jsonl_records(data_file):
        if record.get("declaration_id") != declaration_id:
            continue
        candidate_time = parse_datetime(record["last_updated_at"], "last_updated_at")
        if latest_time is None or candidate_time > latest_time:
            latest_time = candidate_time
            latest_record = record
    return latest_record


def ensure_record_progression(record: dict[str, Any], latest_record: dict[str, Any] | None) -> tuple[str, str]:
    declaration_id = str(record["declaration_id"])
    if latest_record is None:
        return "append", f"new declaration {declaration_id}"

    normalized_current = json.dumps(record, ensure_ascii=False, sort_keys=True)
    normalized_latest = json.dumps(latest_record, ensure_ascii=False, sort_keys=True)
    if normalized_current == normalized_latest:
        return "noop", f"declaration {declaration_id} is already authoritative"

    current_time = parse_datetime(record["last_updated_at"], "last_updated_at")
    latest_time = parse_datetime(latest_record["last_updated_at"], "last_updated_at")
    if current_time <= latest_time:
        raise ValueError(
            f"record for {declaration_id} is stale: "
            f"{record['last_updated_at']} <= {latest_record['last_updated_at']}"
        )
    return "append", f"declaration {declaration_id} updates the authoritative record"


def build_alert_text(record: dict[str, Any]) -> str:
    linked_actions = record.get("linked_actions") or []
    linked_text = ", ".join(linked_actions) if linked_actions else "(none)"
    expected_end_time = record.get("expected_end_time") or "(open-ended)"
    return "\n".join(
        [
            "[AX] Owner-absence declaration",
            f"declaration_id: {record['declaration_id']}",
            f"declared_by: {record['declared_by']} ({record['declared_by_name']})",
            f"start_time: {record['start_time']}",
            f"expected_end_time: {expected_end_time}",
            f"trigger_condition: {record['trigger_condition']}",
            f"response_window_used: {record['response_window_used']}",
            f"scope: {record['scope']}",
            f"ratification_status: {record['ratification_status']}",
            f"sync_state: {record['sync_state']}",
            f"linked_actions: {linked_text}",
            f"canonical_source: {record['canonical_source']}",
            f"last_updated_at: {record['last_updated_at']}",
        ]
    )


def post_json(url: str, payload: dict[str, Any]) -> None:
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with request.urlopen(req, timeout=15) as response:
        if response.status >= 300:
            raise RuntimeError(f"unexpected HTTP status {response.status}")


def send_slack_alert(webhook_url: str, message: str) -> None:
    post_json(webhook_url, {"text": message})


def send_telegram_alert(bot_token: str, chat_id: str, message: str) -> None:
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    data = parse.urlencode(payload).encode("utf-8")
    req = request.Request(url, data=data, method="POST")
    with request.urlopen(req, timeout=15) as response:
        if response.status >= 300:
            raise RuntimeError(f"unexpected HTTP status {response.status}")


def append_to_git_log(data_file: str, line: str) -> None:
    path = Path(data_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line)
        handle.write("\n")


def main() -> int:
    args = parse_args()
    schema = load_schema(args.schema_file)
    record = load_input_record(args)

    errors = validate_record(record, schema, "phase-a-record")
    if errors:
        for error_message in errors:
            print(f"[phase-a][error] {error_message}", file=sys.stderr)
        return 1

    latest_record = find_latest_record(args.data_file, str(record["declaration_id"]))
    try:
        action, reason = ensure_record_progression(record, latest_record)
    except ValueError as exc:
        print(f"[phase-a][error] {exc}", file=sys.stderr)
        return 1

    slack_webhook_url = args.slack_webhook_url or os.getenv(SLACK_WEBHOOK_ENV, "")
    telegram_bot_token = args.telegram_bot_token or os.getenv(TELEGRAM_BOT_TOKEN_ENV, "")
    telegram_chat_id = args.telegram_chat_id or os.getenv(TELEGRAM_CHAT_ID_ENV, "")
    alert_text = build_alert_text(record)
    line = dump_record(record, schema)

    mode = "apply" if args.apply else "dry-run"
    print(f"[phase-a] mode={mode}")
    print(f"[phase-a] decision={action}: {reason}")

    if not args.apply:
        if action == "append":
            print(f"[phase-a] would append to {args.data_file}")
        else:
            print(f"[phase-a] would not append to {args.data_file}")
        if args.skip_alerts:
            print("[phase-a] alerts skipped by flag")
        else:
            print(
                "[phase-a] slack webhook configured="
                + ("yes" if slack_webhook_url else "no")
                + ", telegram configured="
                + ("yes" if telegram_bot_token and telegram_chat_id else "no")
            )
        print("[phase-a] alert preview follows:")
        print(alert_text)
        return 0

    if action == "append":
        append_to_git_log(args.data_file, line)
        print(f"[phase-a] appended record to {args.data_file}")
    else:
        print(f"[phase-a] no append needed for {record['declaration_id']}")
        print("[phase-a] alerts skipped because nothing changed")
        return 0

    if args.skip_alerts:
        print("[phase-a] alerts skipped by flag")
        return 0

    if slack_webhook_url:
        try:
            send_slack_alert(slack_webhook_url, alert_text)
            print("[phase-a] Slack alert sent")
        except (RuntimeError, error.URLError) as exc:
            print(f"[phase-a][error] Slack alert failed: {exc}", file=sys.stderr)
            return 1
    else:
        print(f"[phase-a] Slack alert skipped: ${SLACK_WEBHOOK_ENV} not configured")

    if telegram_bot_token and telegram_chat_id:
        try:
            send_telegram_alert(telegram_bot_token, telegram_chat_id, alert_text)
            print("[phase-a] Telegram alert sent")
        except (RuntimeError, error.URLError) as exc:
            print(f"[phase-a][error] Telegram alert failed: {exc}", file=sys.stderr)
            return 1
    else:
        print(
            "[phase-a] Telegram alert skipped: "
            f"${TELEGRAM_BOT_TOKEN_ENV} or ${TELEGRAM_CHAT_ID_ENV} not configured"
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
