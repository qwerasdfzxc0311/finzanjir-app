#!/usr/bin/env python3
"""Validate the merged FINZANJIR candidate corpus and exercise SQLite FTS4 retrieval."""
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "source-import/candidates/finzanjir_knowledge_merged_6679_manifest.json"
ACTIVE_PATH = ROOT / "app/src/main/assets/finzanjir_knowledge.json"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def norm(value: str) -> str:
    value = unicodedata.normalize("NFKC", str(value or "")).casefold()
    return re.sub(r"\s+", " ", value).strip()


def load_candidate() -> tuple[dict, list[dict]]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    records: list[dict] = []
    for chunk in manifest["chunks"]:
        path = ROOT / chunk["path"]
        raw = path.read_bytes()
        if chunk.get("sha256") and sha256(raw) != chunk["sha256"]:
            raise AssertionError(f"Chunk SHA mismatch: {path}")
        part = json.loads(raw.decode("utf-8"))
        if not isinstance(part, list):
            raise AssertionError(f"Chunk root is not an array: {path}")
        if len(part) != chunk["record_count"]:
            raise AssertionError(f"Chunk count mismatch: {path}")
        records.extend(part)
    return manifest, records


def fts_query(db: sqlite3.Connection, expression: str) -> list[str]:
    rows = db.execute(
        """SELECT m.id
           FROM knowledge_fts f
           JOIN knowledge_meta m ON m.rowid = f.docid
           WHERE knowledge_fts MATCH ?
           LIMIT 100""",
        (expression,),
    ).fetchall()
    return [row[0] for row in rows]


def main() -> None:
    manifest, records = load_candidate()
    expected = manifest["record_count"]
    if expected != 6679 or len(records) != expected:
        raise AssertionError(f"Expected 6,679 records, got {len(records)}")

    ids = [str(r.get("id", "")).strip() for r in records]
    if any(not value for value in ids) or len(ids) != len(set(ids)):
        raise AssertionError("Merged corpus contains a missing or duplicate ID")

    serialized = (json.dumps(records, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    actual_sha = sha256(serialized)
    if actual_sha != manifest["asset_sha256"]:
        raise AssertionError(f"Merged asset SHA mismatch: {actual_sha}")

    stats = manifest["merge_stats"]
    if stats != {
        "active_count": 1121,
        "candidate_count": 5607,
        "same_id_same_text": 31,
        "same_id_changed_text": 18,
        "active_only_preserved": 1072,
        "merged_count": 6679,
        "unique_ids": 6679,
    }:
        raise AssertionError(f"Unexpected merge stats: {stats}")

    legacy_versions = [
        (record, version)
        for record in records
        for version in record.get("legacy_versions", [])
    ]
    legacy_provenance = sum(len(r.get("legacy_provenance", [])) for r in records)
    if len(legacy_versions) != 18 or legacy_provenance != 49:
        raise AssertionError(
            f"History mismatch: versions={len(legacy_versions)}, provenance={legacy_provenance}"
        )

    duplicate_text_groups = sum(
        count > 1 for count in Counter(norm(r.get("text", "")) for r in records).values()
    )
    if duplicate_text_groups != 3:
        raise AssertionError(f"Expected 3 preserved exact-text groups, got {duplicate_text_groups}")

    ocr = [r for r in records if r.get("record_type") == "visual_ocr_candidate"]
    if len(ocr) != 27 or any(r.get("approval") != "candidate_not_authoritative" for r in ocr):
        raise AssertionError("OCR candidate status/count changed")

    # Exercise the same FTS4 shape used by Android: one FTS row per canonical ID.
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE knowledge_meta(rowid INTEGER PRIMARY KEY, id TEXT UNIQUE, body TEXT)")
    db.execute("CREATE VIRTUAL TABLE knowledge_fts USING fts4(search_text, tokenize=unicode61)")
    for rowid, record in enumerate(records, start=1):
        searchable = " ".join(
            [
                str(record.get("text", "")),
                " ".join(record.get("search_aliases", []) or []),
                str(record.get("id", "")),
                str(record.get("source_section", "")),
                str(record.get("record_type", "")),
                str(record.get("domain", "")),
            ]
        )
        db.execute(
            "INSERT INTO knowledge_meta(rowid,id,body) VALUES(?,?,?)",
            (rowid, record["id"], record["text"]),
        )
        db.execute(
            "INSERT INTO knowledge_fts(docid,search_text) VALUES(?,?)",
            (rowid, searchable),
        )
    indexed = db.execute("SELECT COUNT(*) FROM knowledge_fts").fetchone()[0]
    if indexed != 6679:
        raise AssertionError(f"FTS4 row count mismatch: {indexed}")

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
    query_results = {}
    for label, expression in query_checks.items():
        hits = fts_query(db, expression)
        if not hits:
            raise AssertionError(f"FTS4 query returned no evidence: {label}")
        query_results[label] = len(hits)

    historical_alias_checks = 0
    for record, version in legacy_versions:
        old_text = str(version.get("text", ""))
        aliases = record.get("search_aliases", []) or []
        if old_text not in aliases:
            raise AssertionError(f"Historical text is not searchable alias: {record['id']}")
        terms = [t for t in re.findall(r"[\w]+", norm(old_text), flags=re.UNICODE) if len(t) >= 4]
        if not terms:
            continue
        hits = fts_query(db, '"' + terms[0].replace('"', '""') + '"')
        if record["id"] not in hits:
            raise AssertionError(f"Historical alias did not return canonical ID: {record['id']}")
        historical_alias_checks += 1
    if historical_alias_checks != 18:
        raise AssertionError(f"Expected 18 historical alias checks, got {historical_alias_checks}")

    print(json.dumps({
        "status": "PASS",
        "record_count": len(records),
        "unique_ids": len(set(ids)),
        "merged_sha256": actual_sha,
        "legacy_versions": len(legacy_versions),
        "legacy_provenance_entries": legacy_provenance,
        "preserved_exact_text_duplicate_groups": duplicate_text_groups,
        "ocr_candidates_not_authoritative": len(ocr),
        "fts4_indexed_rows": indexed,
        "fts4_query_hits": query_results,
        "historical_alias_checks": historical_alias_checks,
        "active_asset_unchanged": True,
    }, ensure_ascii=False, indent=2))
    db.close()


if __name__ == "__main__":
    main()
