.PHONY: notion-dry notion-verify notion-create owner-absence-validate phasea-dry-run

NOTION_PARENT_PAGE_ID ?= 
NOTION_DATABASE_ID ?= 
OWNER_ABSENCE_DATA_FILE ?= audit/owner_absence.jsonl
OWNER_ABSENCE_SCHEMA_FILE ?= audit/owner_absence.schema.json
AGAINST_REF ?= 

notion-dry:
	@if [ -z "$(NOTION_PARENT_PAGE_ID)" ]; then \
		echo "error: NOTION_PARENT_PAGE_ID is required"; \
		exit 1; \
	fi
	NOTION_PARENT_PAGE_ID="$(NOTION_PARENT_PAGE_ID)" python3 scripts/init_notion_owner_absence_db.py --dry-run

notion-verify:
	@if [ -z "$(NOTION_DATABASE_ID)" ]; then \
		echo "error: NOTION_DATABASE_ID is required"; \
		exit 1; \
	fi
	@if [ -z "$(NOTION_TOKEN)" ]; then \
		echo "error: NOTION_TOKEN is required"; \
		exit 1; \
	fi
	NOTION_TOKEN="$(NOTION_TOKEN)" python3 scripts/init_notion_owner_absence_db.py --verify --database-id "$(NOTION_DATABASE_ID)"

notion-create:
	@if [ -z "$(NOTION_PARENT_PAGE_ID)" ]; then \
		echo "error: NOTION_PARENT_PAGE_ID is required"; \
		exit 1; \
	fi
	@if [ -z "$(NOTION_TOKEN)" ]; then \
		echo "error: NOTION_TOKEN is required"; \
		exit 1; \
	fi
	NOTION_PARENT_PAGE_ID="$(NOTION_PARENT_PAGE_ID)" NOTION_TOKEN="$(NOTION_TOKEN)" python3 scripts/init_notion_owner_absence_db.py

owner-absence-validate:
	@args="--data-file $(OWNER_ABSENCE_DATA_FILE) --schema-file $(OWNER_ABSENCE_SCHEMA_FILE)"; \
	if [ -n "$(AGAINST_REF)" ]; then \
		args="$$args --against-ref $(AGAINST_REF)"; \
	fi; \
	python3 scripts/validate_owner_absence.py $$args

phasea-dry-run:
	@if [ ! -s "$(OWNER_ABSENCE_DATA_FILE)" ]; then \
		echo "error: $(OWNER_ABSENCE_DATA_FILE) is empty or missing"; \
		exit 1; \
	fi
	tail -n 1 "$(OWNER_ABSENCE_DATA_FILE)" | python3 scripts/sync_owner_absence_phase_a.py --record-stdin --data-file "$(OWNER_ABSENCE_DATA_FILE)" --schema-file "$(OWNER_ABSENCE_SCHEMA_FILE)"
