#!/usr/bin/env python3
"""Validate FINZANJIR knowledge migration assets without silently deleting source records."""
import argparse
import collections
import hashlib
import json
import sys
from pathlib import Path


def norm(text: str) -> str:
    return " ".join(str(text or "").casefold().split())


def sha(text: str) -> str:
    return hashlib.sha256(norm(text).encode("utf-8")).hexdigest()


def load(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"Expected a JSON array: {path}")
    return data


def validate(migration: Path, ai_v21: Path | None = None) -> int:
    records = load(migration)
    errors = []
    ids = [r.get("id") for r in records]
    if any(not x for x in ids):
        errors.append("Some records have no ID")
    if len(ids) != len(set(ids)):
        errors.append("Duplicate record IDs found")
    if len(records) != 5580:
        errors.append(f"Expected 5580 records; got {len(records)}")

    by_text = collections.defaultdict(list)
    for r in records:
        if not r.get("text", "").strip():
            errors.append(f"Empty text: {r.get('id')}")
        for field in ("approval", "source_id", "source_version", "source_section",
                      "source_path", "record_type", "audience", "domain"):
            if field not in r:
                errors.append(f"Missing {field}: {r.get('id')}")
        by_text[sha(r.get("text", ""))].append(r)

    layer_ids = {f"V4-L{i:02d}" for i in range(1, 17)}
    present_layers = {r.get("id") for r in records
                      if r.get("record_type") == "layer_catalog_candidate"}
    if not layer_ids.issubset(present_layers):
        errors.append(f"Missing layer records: {sorted(layer_ids - present_layers)}")

    document_chunks = [r for r in records
                       if r.get("record_type") == "concept_document_candidate"]
    if len(document_chunks) != 893:
        errors.append(f"Expected 893 concept document chunks; got {len(document_chunks)}")
    if any(r.get("approval") != "candidate_not_authoritative"
           for r in document_chunks):
        errors.append("At least one imported document chunk was incorrectly promoted")

    ai_count = None
    if ai_v21:
        ai = load(ai_v21)
        ai_count = len(ai)
        migration_ids = set(ids)
        missing = [r.get("id") for r in ai if r.get("id") not in migration_ids]
        if missing:
            errors.append(f"AI v2.1 records missing: {len(missing)}")

    duplicates = [v for v in by_text.values() if len(v) > 1]
    print(f"records={len(records)}")
    print(f"unique_ids={len(set(ids))}")
    print(f"exact_text_duplicate_groups={len(duplicates)}")
    print(f"records_in_exact_text_duplicate_groups={sum(map(len, duplicates))}")
    print(f"document_chunks={len(document_chunks)}")
    print(f"layer_records={len(present_layers & layer_ids)}")
    if ai_count is not None:
        print(f"ai_v2_1_records={ai_count}; all_preserved_by_id={ai_count - sum(1 for r in load(ai_v21) if r.get('id') not in set(ids))}")
    print("status=" + ("FAIL" if errors else "PASS"))
    for error in errors:
        print("ERROR: " + error)
    return 1 if errors else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("migration_json", type=Path)
    parser.add_argument("--ai-v21", type=Path)
    args = parser.parse_args()
    sys.exit(validate(args.migration_json, args.ai_v21))
