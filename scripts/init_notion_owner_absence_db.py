#!/usr/bin/env python3
"""
init_notion_owner_absence_db.py

Purpose
-------
Create the Notion database `AX Owner Absence Declarations` with the properties
defined in AX_OWNER_ABSENCE_LOG_SCHEMA_DESIGN v1 §4.

This script is the programmatic alternative to manual Notion UI setup. It is
idempotent in the sense that it refuses to create a duplicate database under
the same parent page; you may also choose to create the DB manually in Notion
and use this script only to verify property parity.

Preconditions
-------------
1. A Notion integration exists and has been shared with the parent page.
2. The integration token is available. Per AX_OPERATIONS_POLICY §6.3, the
   token must not be hardcoded or committed. The script reads it from the
   environment variable `NOTION_TOKEN`.
3. The parent page ID is available. Set the environment variable
   `NOTION_PARENT_PAGE_ID` to the ID of a page the integration can write to.
4. Python 3.9+ and the `notion-client` library are installed:
       pip install notion-client

Usage
-----
    export NOTION_TOKEN='secret_xxx'          # from an age-encrypted source
    export NOTION_PARENT_PAGE_ID='<page-id>'
    python3 init_notion_owner_absence_db.py

    # or in dry-run mode (no API calls, just prints the payload):
    python3 init_notion_owner_absence_db.py --dry-run

    # or in verify mode (queries existing DB by title and checks schema parity):
    python3 init_notion_owner_absence_db.py --verify --database-id <db-id>

Safety
------
- `--dry-run` performs no API calls.
- Without `--force`, the script refuses to create a second DB if a DB with the
  same title is already a child of the parent page.
- The script does not write any record into the DB. The first real declaration
  is a separate operational action.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

SCHEMA_VERSION = "1.0"
DB_TITLE = "AX Owner Absence Declarations"

# Property schema in Notion API format (matching AX_OWNER_ABSENCE_LOG_SCHEMA_DESIGN §4.2)
PROPERTIES: dict[str, dict[str, Any]] = {
    "declaration_id": {"title": {}},
    "schema_version": {"rich_text": {}},
    "declared_by": {
        "select": {
            "options": [
                {"name": "owner", "color": "blue"},
                {"name": "deputy_owner", "color": "purple"},
            ]
        }
    },
    "declared_by_name": {"rich_text": {}},
    "start_time": {"date": {}},
    "expected_end_time": {"date": {}},
    "open_ended": {"checkbox": {}},
    "trigger_condition": {
        "select": {
            "options": [
                {"name": "planned_leave", "color": "green"},
                {"name": "incapacitated", "color": "red"},
                {"name": "unreachable", "color": "orange"},
                {"name": "explicit_delegation", "color": "blue"},
            ]
        }
    },
    "response_window_used": {
        "select": {
            "options": [
                {"name": "general", "color": "default"},
                {"name": "emergency", "color": "red"},
                {"name": "overnight_non_emergency", "color": "gray"},
            ]
        }
    },
    "scope": {"rich_text": {}},
    "ratification_status": {
        "select": {
            "options": [
                {"name": "pending", "color": "yellow"},
                {"name": "ratified", "color": "green"},
                {"name": "reversed", "color": "red"},
            ]
        }
    },
    "ratified_at": {"date": {}},
    "linked_actions": {"rich_text": {}},
    "canonical_source": {
        "select": {
            "options": [
                {"name": "notion", "color": "blue"},
                {"name": "git", "color": "gray"},
            ]
        }
    },
    "sync_state": {
        "select": {
            "options": [
                {"name": "pending", "color": "yellow"},
                {"name": "synced", "color": "green"},
                {"name": "conflict", "color": "red"},
            ]
        }
    },
    "created_at": {"created_time": {}},
    "last_updated_at": {"last_edited_time": {}},
}


def build_create_payload(parent_page_id: str) -> dict[str, Any]:
    """Build the Notion API payload for creating the database."""
    return {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "title": [
            {
                "type": "text",
                "text": {"content": DB_TITLE},
            }
        ],
        "description": [
            {
                "type": "text",
                "text": {
                    "content": (
                        f"Canonical (Notion) for Owner-absence declarations. "
                        f"Schema v{SCHEMA_VERSION}. "
                        f"Paired with Git canonical at audit/owner_absence.jsonl. "
                        f"See AX_OWNER_ABSENCE_LOG_DESTINATION_POLICY v2."
                    )
                },
            }
        ],
        "properties": PROPERTIES,
    }


def dry_run(parent_page_id: str) -> None:
    payload = build_create_payload(parent_page_id)
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def check_existing(notion, parent_page_id: str) -> str | None:
    """Search for an existing database with the same title under the parent page.

    Returns the ID of the first match, or None if no match.
    """
    # The search API returns objects the integration can see; filter to databases.
    results = notion.search(
        query=DB_TITLE,
        filter={"property": "object", "value": "database"},
    ).get("results", [])
    for db in results:
        parent = db.get("parent", {})
        if parent.get("type") != "page_id":
            continue
        if parent.get("page_id") != parent_page_id:
            continue
        title = db.get("title", [])
        if title and title[0].get("plain_text") == DB_TITLE:
            return db.get("id")
    return None


def verify_schema(notion, database_id: str) -> int:
    """Compare the live DB's properties against the canonical schema.

    Returns the number of mismatches (0 if fully aligned).
    """
    db = notion.databases.retrieve(database_id=database_id)
    live_props = db.get("properties", {})
    mismatches = 0

    # Check presence and type family
    for name, spec in PROPERTIES.items():
        if name not in live_props:
            print(f"[verify] MISSING: {name}")
            mismatches += 1
            continue
        live_type = next(iter(live_props[name].keys() - {"id", "name", "type"}), None)
        expected_type = next(iter(spec.keys()))
        if live_type != expected_type:
            # Notion stores the type key under the type name itself; compare via 'type' field
            live_type = live_props[name].get("type")
            if live_type != expected_type:
                print(f"[verify] TYPE MISMATCH: {name} expected={expected_type} live={live_type}")
                mismatches += 1

    # Check select options
    for name, spec in PROPERTIES.items():
        if "select" not in spec:
            continue
        expected_names = {opt["name"] for opt in spec["select"]["options"]}
        live_select = live_props.get(name, {}).get("select", {})
        live_names = {opt["name"] for opt in live_select.get("options", [])}
        missing = expected_names - live_names
        extra = live_names - expected_names
        if missing:
            print(f"[verify] OPTIONS MISSING in {name}: {sorted(missing)}")
            mismatches += 1
        if extra:
            print(f"[verify] OPTIONS EXTRA in {name}: {sorted(extra)} (not in canonical schema)")
            mismatches += 1

    # Check extra properties
    canonical_names = set(PROPERTIES.keys())
    live_names_all = set(live_props.keys())
    extra_props = live_names_all - canonical_names
    if extra_props:
        print(f"[verify] EXTRA PROPERTIES in live DB (not in canonical schema): {sorted(extra_props)}")
        mismatches += len(extra_props)

    if mismatches == 0:
        print("[verify] schema aligned.")
    else:
        print(f"[verify] {mismatches} mismatch(es) found.")
    return mismatches


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1] if __doc__ else "")
    parser.add_argument("--dry-run", action="store_true", help="Print the API payload without calling Notion")
    parser.add_argument("--verify", action="store_true", help="Verify an existing DB instead of creating one")
    parser.add_argument("--database-id", help="Database ID for --verify")
    parser.add_argument("--force", action="store_true", help="Create even if a DB with the same title already exists")
    args = parser.parse_args()

    parent_page_id = os.environ.get("NOTION_PARENT_PAGE_ID", "").strip()
    if not parent_page_id and not args.verify:
        print("error: NOTION_PARENT_PAGE_ID env var is required (unless --verify)", file=sys.stderr)
        return 2

    if args.dry_run:
        dry_run(parent_page_id)
        return 0

    token = os.environ.get("NOTION_TOKEN", "").strip()
    if not token:
        print("error: NOTION_TOKEN env var is required", file=sys.stderr)
        return 2

    try:
        from notion_client import Client  # type: ignore
    except ImportError:
        print("error: notion-client is not installed. Run: pip install notion-client", file=sys.stderr)
        return 2

    notion = Client(auth=token)

    if args.verify:
        if not args.database_id:
            print("error: --verify requires --database-id", file=sys.stderr)
            return 2
        return 0 if verify_schema(notion, args.database_id) == 0 else 1

    existing = check_existing(notion, parent_page_id)
    if existing and not args.force:
        print(f"error: a database titled {DB_TITLE!r} already exists under this parent page (id={existing}).", file=sys.stderr)
        print("       pass --force to create another, or use --verify --database-id to check schema.", file=sys.stderr)
        return 3

    payload = build_create_payload(parent_page_id)
    db = notion.databases.create(**payload)
    db_id = db.get("id")
    db_url = db.get("url")
    print(f"created database: {DB_TITLE}")
    print(f"  id:  {db_id}")
    print(f"  url: {db_url}")
    print(f"  schema_version: {SCHEMA_VERSION}")
    print()
    print("Next steps:")
    print("  1. open the URL above in Notion")
    print("  2. share the database with Owner and Deputy Owner as Full access")
    print("  3. share read access with Approver and governance-audit as required")
    print("  4. create the views listed in AX_OWNER_ABSENCE_LOG_SCHEMA_DESIGN §4.3")
    print("  5. record the database id in the AX operational bookmark store")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
