#!/usr/bin/env python3
"""Validate FINZANJIR 5,607-record candidate migration without deleting provenance."""
import argparse
import collections
import hashlib
import json
import sys
from pathlib import Path

EXPECTED_COUNT = 5607
EXPECTED_SHA256 = "f3457b372c5e7f79a0875603cb33987a7720f96061c1ac23ea038b69f2dfb250"
EXPECTED_DOCUMENT_CHUNKS = 893
EXPECTED_OCR_CANDIDATES = 27


def norm(text: str) -> str:
    return " ".join(str(text or "").casefold().split())


def load(path: Path):
    raw = path.read_bytes()
    data = json.loads(raw.decode("utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"Expected a JSON array: {path}")
    return raw, data


def validate(migration: Path, ai_v21: Path | None = None, strict_hash: bool = True) -> int:
    raw, records = load(migration)
    errors = []
    actual_sha = hashlib.sha256(raw).hexdigest()
    if strict_hash and actual_sha != EXPECTED_SHA256:
        errors.append(f"SHA-256 mismatch: {actual_sha}; expected {EXPECTED_SHA256}")
    if len(records) != EXPECTED_COUNT:
        errors.append(f"Expected {EXPECTED_COUNT} records; got {len(records)}")

    ids = [r.get("id") for r in records]
    if any(not x for x in ids):
        errors.append("Some records have no ID")
    duplicate_ids = [key for key, count in collections.Counter(ids).items() if count > 1]
    if duplicate_ids:
        errors.append(f"Duplicate record IDs found: {len(duplicate_ids)}")

    required_fields = ("text", "approval", "source_id", "source_version",
                       "source_section", "source_path", "record_type", "audience", "domain")
    for record in records:
        rid = record.get("id", "<missing>")
        for field in required_fields:
            if field not in record:
                errors.append(f"Missing {field}: {rid}")
        if not str(record.get("text", "")).strip():
            errors.append(f"Empty text: {rid}")

    # Identical text is reported, never silently deleted: distinct source provenance matters.
    by_text = collections.defaultdict(list)
    for record in records:
        by_text[norm(record.get("text", ""))].append(record)
    exact_groups = [group for group in by_text.values() if len(group) > 1]

    expected_layers = {f"V4-L{i:02d}" for i in range(1, 17)}
    present_layers = {r.get("id") for r in records
                      if r.get("record_type") == "layer_catalog_candidate"}
    missing_layers = expected_layers - present_layers
    if missing_layers:
        errors.append(f"Missing layer records: {sorted(missing_layers)}")

    document_chunks = [r for r in records
                       if r.get("record_type") == "concept_document_candidate"]
    if len(document_chunks) != EXPECTED_DOCUMENT_CHUNKS:
        errors.append(f"Expected {EXPECTED_DOCUMENT_CHUNKS} document chunks; got {len(document_chunks)}")
    if any(r.get("approval") != "candidate_not_authoritative" for r in document_chunks):
        errors.append("At least one document chunk was incorrectly promoted")

    ocr = [r for r in records if r.get("record_type") == "visual_ocr_candidate"]
    if len(ocr) != EXPECTED_OCR_CANDIDATES:
        errors.append(f"Expected {EXPECTED_OCR_CANDIDATES} OCR candidates; got {len(ocr)}")
    if any(r.get("approval") != "candidate_not_authoritative" for r in ocr):
        errors.append("At least one OCR candidate was incorrectly promoted")

    ai_count = None
    if ai_v21:
        _, ai_records = load(ai_v21)
        ai_count = len(ai_records)
        migration_ids = set(ids)
        missing = [r.get("id") for r in ai_records if r.get("id") not in migration_ids]
        if missing:
            errors.append(f"AI v2.1 records missing by ID: {len(missing)}")

    print(f"records={len(records)}")
    print(f"unique_ids={len(set(ids))}")
    print(f"sha256={actual_sha}")
    print(f"exact_text_duplicate_groups={len(exact_groups)} (preserved; provenance not discarded)")
    print(f"records_in_exact_text_duplicate_groups={sum(map(len, exact_groups))}")
    print(f"document_chunks={len(document_chunks)}")
    print(f"layer_records={len(present_layers & expected_layers)}")
    print(f"visual_ocr_candidates={len(ocr)} (candidate_not_authoritative)")
    if ai_count is not None:
        print(f"ai_v2_1_records={ai_count}")
    print("status=" + ("FAIL" if errors else "PASS"))
    for error in errors:
        print("ERROR: " + error)
    return 1 if errors else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("migration_json", type=Path)
    parser.add_argument("--ai-v21", type=Path)
    parser.add_argument("--skip-hash", action="store_true",
                        help="Skip canonical SHA-256 enforcement for diagnostic use only.")
    args = parser.parse_args()
    sys.exit(validate(args.migration_json, args.ai_v21, strict_hash=not args.skip_hash))
