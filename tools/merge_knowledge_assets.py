#!/usr/bin/env python3
"""Safely merge FINZANJIR knowledge assets without dropping active records.

The script uses only Python's standard library. It never deletes records merely
because their text looks similar. Same-ID exact matches merge provenance;
same-ID text conflicts preserve the prior version as metadata and a search alias.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
import re
import unicodedata

EXPECTED_CANDIDATE_SHA256 = "f3457b372c5e7f79a0875603cb33987a7720f96061c1ac23ea038b69f2dfb250"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def norm(value: str) -> str:
    value = unicodedata.normalize("NFKC", value or "").casefold()
    return re.sub(r"\s+", " ", value).strip()


def provenance(record: dict, label: str) -> dict:
    fields = (
        "id", "source_id", "source_package", "source_version", "source_section",
        "source_path", "source_page", "language", "source_language", "approval",
        "record_type", "record_status",
    )
    return {"snapshot": label, **{k: record[k] for k in fields if k in record}}


def load_records(path: Path) -> tuple[bytes, list[dict]]:
    raw = path.read_bytes()
    parsed = json.loads(raw.decode("utf-8"))
    if not isinstance(parsed, list):
        raise ValueError(f"{path}: root JSON must be an array")
    seen = set()
    for i, record in enumerate(parsed):
        if not isinstance(record, dict):
            raise ValueError(f"{path}: record {i} is not an object")
        rid = str(record.get("id", "")).strip()
        text = str(record.get("text", "")).strip()
        if not rid or not text:
            raise ValueError(f"{path}: record {i} has empty id/text")
        if rid in seen:
            raise ValueError(f"{path}: duplicate ID {rid}")
        seen.add(rid)
    return raw, parsed


def merge(active: list[dict], candidate: list[dict]) -> tuple[list[dict], dict]:
    active_by_id = {r["id"]: r for r in active}
    candidate_by_id = {r["id"]: r for r in candidate}
    merged = [dict(r) for r in candidate]
    merged_by_id = {r["id"]: r for r in merged}
    same_text = 0
    changed_text = 0
    active_only = 0

    for old in active:
        rid = old["id"]
        new = merged_by_id.get(rid)
        if new is None:
            # Preserve all active-only records unchanged.
            merged.append(dict(old))
            active_only += 1
            continue

        old_prov = provenance(old, "previous_active_android_asset")
        new.setdefault("legacy_provenance", [])
        if old_prov not in new["legacy_provenance"]:
            new["legacy_provenance"].append(old_prov)

        if norm(old.get("text", "")) == norm(new.get("text", "")):
            same_text += 1
        else:
            changed_text += 1
            old_version = {
                "version_status": "historical_candidate_not_authoritative",
                "text": old["text"],
                "provenance": old_prov,
            }
            new.setdefault("legacy_versions", [])
            if not any(v.get("text") == old["text"] for v in new["legacy_versions"]):
                new["legacy_versions"].append(old_version)
            new.setdefault("search_aliases", [])
            if old["text"] not in new["search_aliases"]:
                new["search_aliases"].append(old["text"])

    ids = [r["id"] for r in merged]
    duplicates = [rid for rid, count in Counter(ids).items() if count > 1]
    if duplicates:
        raise ValueError(f"merge produced duplicate IDs: {duplicates[:10]}")

    stats = {
        "active_count": len(active),
        "candidate_count": len(candidate),
        "same_id_same_text": same_text,
        "same_id_changed_text": changed_text,
        "active_only_preserved": active_only,
        "merged_count": len(merged),
        "unique_ids": len(set(ids)),
    }
    if stats["merged_count"] != stats["unique_ids"]:
        raise ValueError("unique ID invariant failed")
    return merged, stats


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--active", required=True, type=Path)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--output-manifest", required=True, type=Path)
    parser.add_argument("--allow-candidate-sha-mismatch", action="store_true")
    args = parser.parse_args()

    active_raw, active = load_records(args.active)
    candidate_raw, candidate = load_records(args.candidate)
    candidate_sha = sha256(candidate_raw)
    if candidate_sha != EXPECTED_CANDIDATE_SHA256 and not args.allow_candidate_sha_mismatch:
        raise ValueError(
            "candidate SHA-256 does not match the audited source; "
            f"expected {EXPECTED_CANDIDATE_SHA256}, got {candidate_sha}"
        )

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    expected = manifest.get("asset_sha256")
    if expected and expected != candidate_sha:
        raise ValueError("candidate manifest SHA-256 does not match candidate asset")
    expected_count = manifest.get("target_record_count")
    if expected_count and expected_count != len(candidate):
        raise ValueError("candidate record count does not match manifest")

    merged, stats = merge(active, candidate)
    output_bytes = (json.dumps(merged, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    output_sha = sha256(output_bytes)

    manifest.update({
        "status": "MERGED_CANDIDATE_NOT_DEVICE_VERIFIED",
        "activation_status": "MERGED_ASSET_REQUIRES_ANDROID_FTS4_VALIDATION",
        "record_count": len(merged),
        "asset_sha256": output_sha,
        "candidate_asset_sha256": candidate_sha,
        "previous_active_asset_sha256": sha256(active_raw),
        "merge_stats": stats,
        "duplicate_policy": {
            "same_id_same_text": "one canonical record; prior provenance retained",
            "same_id_changed_text": "candidate text retained; prior text stored in legacy_versions and search_aliases",
            "different_ids_same_text": "records retained; no automatic deletion",
        },
        "note": "Candidate and active records are not automatically promoted to authoritative knowledge.",
    })
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output_manifest.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(output_bytes)
    args.output_manifest.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({**stats, "candidate_sha256": candidate_sha,
                      "merged_sha256": output_sha}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
