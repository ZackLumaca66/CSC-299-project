"""Schema metadata for JSON persistence."""

SCHEMA_VERSION = 1

def base_document() -> dict:
    return {"schema_version": SCHEMA_VERSION, "tasks": []}