#!/usr/bin/env python3
"""Read-only validation of the staged FINZANJIR 6,679-record corpus and FTS4.

The script verifies Git blob identities for every staged part and the current
active asset, then builds a temporary SQLite FTS4 index. It never writes to or
replaces the Android asset and never promotes candidate records.
"""
from __future__ import annotations

import collections
import hashlib
import json
import re
import sqlite3
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTS_DIR = ROOT / "source-import" / "candidates"
ACTIVE_PATH = ROOT / "app" / "src" / "main" / "assets" / "finzanjir_knowledge.json"

# Git object IDs from the inspected PR head commit. These pin the exact staged
# inputs without requiring a second, separately maintained manifest.
EXPECTED_PART_BLOBS = [
    "34c204b7e9c2c056fdebbc3531ceb98c0ed806e5",
    "cfefa45830c53e2dad33f08ca2e1e9abd9d4940f",
    "c7858da12fdc8f0e3ff8dcb8a3c87a942d4ee083",
    "7b480db7deabf41d8f7d3c980284a748fe2fb70e",
    "08e94ea80495a9d9e8f03a463948d944fc656938",
    "0b61d8b3a73dddf1c4794f221c50f5f6c55abdae",
    "08679187ff89f318e33d970fbf2612fb62a6a179",
    "59fc8b28b78d6027bc34dd1ed44440e9bc128cf1",
    "15eaa47d5f3796a9462e12c14c0df92d7e88af47",
    "19c67db50a93cf347faffa954533acc9bb80631f",
    "40f7648350040edbbf0075ce60d3c8f25cc65fe4",
    "83e7876ccee417910a44f215030616942fe00dab",
]
EXPECTED_ACTIVE_BLOB = "fc57872f98b33ecec0d182e58354f63ee9d4b7c1"
EXPECTED_PART_COUNTS = [600] * 11 + [79]
EXPECTED_RECORDS = 6679
EXPECTED_ACTIVE = 1121
EXPECTED_CHANGED_TEXT = 18
EXPECTED_PROVENANCE_ENTRIES = 49
EXPECTED_HISTORICAL_VERSIONS = 18
EXPECTED_DUPLICATE_TEXT_GROUPS = 3
EXPECTED_DUPLICATE_TEXT_ROWS = 6


def fail(message: str) -> None:
    raise ValueError(message)


def git_blob_sha(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode("ascii") + b"\0"
    return hashlib.sha1(header + data).hexdigest()


def norm(value: object) -> str:
    value = unicodedata.normalize("NFKC", str(value or "")).casefold()
    return re.sub(r"\s+", " ", value).strip()


def read_array(path: Path) -> tuple[bytes, list[dict]]:
    raw = path.read_bytes()
    value = json.loads(raw.decode("utf-8"))
    if not isinstance(value, list):
        fail(f"{path}: JSON root must be an array")
    if any(not isinstance(row, dict) for row in value):
        fail(f"{path}: every array item must be an object")
    return raw, value


def fts_ids(db: sqlite3.Connection, expression: str) -> list[str]:
    rows = db.execute(
        """SELECT m.id
           FROM knowledge_fts f
           JOIN knowledge_meta m ON m._id = f.docid
           WHERE knowledge_fts MATCH ?
           LIMIT 100""",
        (expression,),
    ).fetchall()
    return [row[0] for row in rows]


def fts_contains(db: sqlite3.Connection, expression: str, record_id: str) -> bool:
    row = db.execute(
        """SELECT 1
           FROM knowledge_fts f
           JOIN knowledge_meta m ON m._id = f.docid
           WHERE knowledge_fts MATCH ? AND m.id = ?
           LIMIT 1""",
        (expression, record_id),
    ).fetchone()
    return row is not None


def main() -> None:
    part_paths = [
        PARTS_DIR / f"finzanjir_knowledge_merged_6679_part_{index:02d}.json"
        for index in range(1, 13)
    ]
    if len(EXPECTED_PART_BLOBS) != len(part_paths):
        fail("Internal part/blob manifest length mismatch")

    merged: list[dict] = []
    part_counts: list[int] = []
    for path, expected_blob in zip(part_paths, EXPECTED_PART_BLOBS):
        raw, part = read_array(path)
        actual_blob = git_blob_sha(raw)
        if actual_blob != expected_blob:
            fail(f"Git blob mismatch for {path.name}: {actual_blob}")
        part_counts.append(len(part))
        merged.extend(part)

    if part_counts != EXPECTED_PART_COUNTS:
        fail(f"Unexpected split sizes: {part_counts}")
    if len(merged) != EXPECTED_RECORDS:
        fail(f"Expected {EXPECTED_RECORDS} merged records; found {len(merged)}")

    active_raw, active = read_array(ACTIVE_PATH)
    active_blob = git_blob_sha(active_raw)
    if active_blob != EXPECTED_ACTIVE_BLOB:
        fail(f"Active Android asset changed unexpectedly: {active_blob}")
    if len(active) != EXPECTED_ACTIVE:
        fail(f"Expected {EXPECTED_ACTIVE} active records; found {len(active)}")

    ids = [str(row.get("id", "")).strip() for row in merged]
    if any(not rid for rid in ids):
        fail("Merged candidate contains an empty ID")
    id_counts = collections.Counter(ids)
    duplicates = [rid for rid, count in id_counts.items() if count > 1]
    if duplicates:
        fail(f"Merged candidate contains duplicate IDs: {duplicates[:10]}")
    if len(set(ids)) != EXPECTED_RECORDS:
        fail("Unique ID count does not equal 6,679")

    required = ("text", "approval", "source_id", "source_version", "source_section",
                "source_path", "record_type", "audience", "domain")
    for row in merged:
        rid = row.get("id", "<missing>")
        for field in required:
            if field not in row or row[field] is None or str(row[field]).strip() == "":
                fail(f"{rid}: missing required provenance/content field {field}")
        if not str(row["text"]).strip():
            fail(f"{rid}: empty text")

    active_by_id = {str(row["id"]): row for row in active}
    merged_by_id = {str(row["id"]): row for row in merged}
    missing_active = set(active_by_id) - set(merged_by_id)
    if missing_active:
        fail(f"Merged candidate dropped {len(missing_active)} active IDs")

    changed = {
        rid for rid, old in active_by_id.items()
        if norm(old.get("text")) != norm(merged_by_id[rid].get("text"))
    }
    if len(changed) != EXPECTED_CHANGED_TEXT:
        fail(f"Expected {EXPECTED_CHANGED_TEXT} changed active text versions; found {len(changed)}")

    provenance_entries = 0
    historical_versions = []
    for row in merged:
        provenance = row.get("legacy_provenance", [])
        versions = row.get("legacy_versions", [])
        if not isinstance(provenance, list) or not isinstance(versions, list):
            fail(f"{row['id']}: historical metadata must be arrays")
        provenance_entries += len(provenance)
        historical_versions.extend((row, version) for version in versions)

    if provenance_entries != EXPECTED_PROVENANCE_ENTRIES:
        fail(f"Expected {EXPECTED_PROVENANCE_ENTRIES} legacy provenance entries; found {provenance_entries}")
    if len(historical_versions) != EXPECTED_HISTORICAL_VERSIONS:
        fail(f"Expected {EXPECTED_HISTORICAL_VERSIONS} historical versions; found {len(historical_versions)}")

    for rid in changed:
        old_text = str(active_by_id[rid].get("text", ""))
        row = merged_by_id[rid]
        versions = row.get("legacy_versions", [])
        aliases = row.get("search_aliases", [])
        if not any(isinstance(v, dict) and v.get("text") == old_text for v in versions):
            fail(f"{rid}: old text is missing from legacy_versions")
        if not isinstance(aliases, list) or old_text not in aliases:
            fail(f"{rid}: old text is missing from search_aliases")

    by_text: dict[str, list[dict]] = collections.defaultdict(list)
    for row in merged:
        by_text[norm(row.get("text"))].append(row)
    duplicate_groups = [rows for rows in by_text.values() if len(rows) > 1]
    duplicate_rows = sum(len(rows) for rows in duplicate_groups)
    if len(duplicate_groups) != EXPECTED_DUPLICATE_TEXT_GROUPS:
        fail(f"Expected {EXPECTED_DUPLICATE_TEXT_GROUPS} exact-text duplicate groups; found {len(duplicate_groups)}")
    if duplicate_rows != EXPECTED_DUPLICATE_TEXT_ROWS:
        fail(f"Expected {EXPECTED_DUPLICATE_TEXT_ROWS} rows in exact-text duplicate groups; found {duplicate_rows}")

    ocr = [row for row in merged if row.get("record_type") == "visual_ocr_candidate"]
    if len(ocr) != 27 or any(row.get("approval") != "candidate_not_authoritative" for row in ocr):
        fail("OCR candidate count/status changed; expected 27 candidate_not_authoritative rows")

    # Temporary SQLite FTS4 index with the same tokenizer and fields as Android.
    db = sqlite3.connect(":memory:")
    try:
        db.execute(
            "CREATE TABLE knowledge_meta(_id INTEGER PRIMARY KEY, id TEXT UNIQUE, body TEXT)"
        )
        db.execute(
            "CREATE VIRTUAL TABLE knowledge_fts USING fts4(search_text, tokenize=unicode61)"
        )
        for rowid, row in enumerate(merged, start=1):
            aliases = row.get("search_aliases", [])
            if not isinstance(aliases, list):
                fail(f"{row['id']}: search_aliases must be an array")
            searchable = " ".join([
                str(row["text"]),
                " ".join(str(value) for value in aliases),
                str(row["id"]),
                str(row["source_section"]),
                str(row["record_type"]),
                str(row["domain"]),
            ])
            db.execute(
                "INSERT INTO knowledge_meta(_id,id,body) VALUES(?,?,?)",
                (rowid, row["id"], row["text"]),
            )
            db.execute(
                "INSERT INTO knowledge_fts(docid,search_text) VALUES(?,?)",
                (rowid, searchable),
            )

        indexed = db.execute("SELECT COUNT(*) FROM knowledge_fts").fetchone()[0]
        if indexed != EXPECTED_RECORDS:
            fail(f"FTS4 row count mismatch: {indexed}")

        query_checks = {
            "risk_engine": '"risk" AND "engine"',
            "cross_match": '"cross" AND "match"',
            "fraud_graph": '"fraud" AND "graph"',
            "timeline": '"timeline"',
            "fin_recovery": '"fin" AND "recovery"',
            "human_review": '"human" AND "review"',
            "citizen_cards": '"mening" AND "kartalarim"',
            "otp_safety": '"otp"',
            "cvv_safety": '"cvv"',
        }
        query_hits = {}
        for label, expression in query_checks.items():
            hits = fts_ids(db, expression)
            if not hits:
                fail(f"FTS4 returned no result for {label}")
            query_hits[label] = len(hits)

        alias_checks = 0
        for row, version in historical_versions:
            old_text = str(version.get("text", ""))
            aliases = row.get("search_aliases", [])
            if old_text not in aliases:
                fail(f"{row['id']}: historical text is not an FTS search alias")
            terms = [
                term for term in re.findall(r"[\w]+", norm(old_text), flags=re.UNICODE)
                if len(term) >= 4
            ][:2]
            if not terms:
                fail(f"{row['id']}: historical text has no usable FTS terms")
            expression = " AND ".join('"' + term.replace('"', '""') + '"' for term in terms)
            if not fts_contains(db, expression, row["id"]):
                fail(f"{row['id']}: historical alias does not retrieve its canonical ID")
            alias_checks += 1
        if alias_checks != EXPECTED_HISTORICAL_VERSIONS:
            fail(f"Expected {EXPECTED_HISTORICAL_VERSIONS} historical alias checks; got {alias_checks}")
    finally:
        db.close()

    print(json.dumps({
        "status": "PASS",
        "candidate_records": len(merged),
        "unique_ids": len(set(ids)),
        "active_records": len(active),
        "active_ids_preserved": len(active) - len(missing_active),
        "changed_active_text_versions": len(changed),
        "legacy_provenance_entries": provenance_entries,
        "historical_versions": len(historical_versions),
        "preserved_exact_text_duplicate_groups": len(duplicate_groups),
        "preserved_exact_text_duplicate_rows": duplicate_rows,
        "ocr_candidates_not_authoritative": len(ocr),
        "fts4_indexed_rows": indexed,
        "fts4_query_hits": query_hits,
        "historical_alias_checks": alias_checks,
        "active_asset_unchanged": True,
        "activation_status": "NOT_ACTIVATED",
        "ranking": "bounded lexical; BM25 not used",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("status=FAIL", file=sys.stderr)
        print(f"error={error}", file=sys.stderr)
        sys.exit(1)
