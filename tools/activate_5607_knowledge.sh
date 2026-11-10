#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE_JSON="${SOURCE_JSON:-}"
TARGET="$ROOT/app/src/main/assets/finzanjir_knowledge.json"
MANIFEST="$ROOT/app/src/main/assets/knowledge_manifest.json"
EXPECTED_COUNT=5607
EXPECTED_SHA="f3457b372c5e7f79a0875603cb33987a7720f96061c1ac23ea038b69f2dfb250"

if [[ -z "$SOURCE_JSON" || ! -f "$SOURCE_JSON" ]]; then
  echo "SOURCE_JSON yo‘lini mavjud 5,607 yozuvli JSON faylga ko‘rsating."
  echo 'Misol: SOURCE_JSON="$HOME/Downloads/finzanjir_knowledge_5607.json" bash tools/activate_5607_knowledge.sh'
  exit 2
fi
ACTUAL_SHA="$(sha256sum "$SOURCE_JSON" | awk '{print $1}')"
if [[ "$ACTUAL_SHA" != "$EXPECTED_SHA" ]]; then
  echo "SHA-256 mos emas. Kutilgan: $EXPECTED_SHA ; topilgan: $ACTUAL_SHA"
  exit 3
fi
python3 - "$SOURCE_JSON" "$EXPECTED_COUNT" <<'PY'
import json, sys, collections
path, expected = sys.argv[1], int(sys.argv[2])
with open(path, encoding="utf-8") as f: rows = json.load(f)
if not isinstance(rows, list) or len(rows) != expected:
    raise SystemExit(f"Record count mismatch: {len(rows) if isinstance(rows,list) else 'not-list'} / {expected}")
ids = [r.get("id") for r in rows]
if any(not x for x in ids) or len(ids) != len(set(ids)):
    raise SystemExit("ID missing or duplicate ID detected; import stopped.")
layers = {r.get("id") for r in rows if r.get("record_type") == "layer_catalog_candidate"}
required = {f"V4-L{i:02d}" for i in range(1,17)}
if not required.issubset(layers): raise SystemExit("One or more V4-L01 ... V4-L16 records are missing.")
visual = [r for r in rows if r.get("record_type") == "visual_ocr_candidate"]
if len(visual) != 27: raise SystemExit(f"Expected 27 visual OCR candidates; found {len(visual)}.")
print(f"PASS: {len(rows)} records, unique IDs, 16 layer records, {len(visual)} visual OCR candidates.")
PY

TMP_ASSET="$TARGET.tmp"
TMP_MANIFEST="$MANIFEST.tmp"
BACKUP_DIR="$ROOT/.knowledge-backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp "$TARGET" "$BACKUP_DIR/finzanjir_knowledge.previous.json"
cp "$MANIFEST" "$BACKUP_DIR/knowledge_manifest.previous.json"
cp "$SOURCE_JSON" "$TMP_ASSET"
python3 - "$TMP_ASSET" "$MANIFEST" "$TMP_MANIFEST" "$EXPECTED_COUNT" "$EXPECTED_SHA" <<'PY'
import json, sys, os, collections
asset, manifest_path, output, expected_count, expected_sha = sys.argv[1:]
expected_count = int(expected_count)
with open(asset, encoding="utf-8") as f: rows = json.load(f)
with open(manifest_path, encoding="utf-8") as f: manifest = json.load(f)
if len(rows) != expected_count: raise SystemExit("Asset count changed during activation.")
manifest["schema_version"] = manifest.get("schema_version", "1.0")
manifest["knowledge_base_version"] = "0.6.0-5607-lightweight"
manifest["updated_date"] = "2026-11-10"
manifest["record_count"] = expected_count
manifest["asset_sha256"] = expected_sha
manifest["asset_size_bytes"] = os.path.getsize(asset)
manifest["activation_status"] = "CANDIDATE_ASSET_INSTALLED_RUNTIME_VERIFICATION_REQUIRED"
manifest["records_by_type"] = dict(collections.Counter(r.get("record_type","unknown") for r in rows))
manifest["known_gaps"] = list(dict.fromkeys(manifest.get("known_gaps", []) + [
    "5,607-record candidate asset installed; Android FTS4 import and runtime retrieval still require build/device verification.",
    "Visual OCR records remain candidate_not_authoritative and require expert visual review."
]))
with open(output, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)
    f.write("\n")
PY
mv "$TMP_ASSET" "$TARGET"
mv "$TMP_MANIFEST" "$MANIFEST"
echo "5,607-record candidate asset installed after SHA/count/ID/layer/OCR checks."
echo "Backup: $BACKUP_DIR"
echo "Next: run Android Gradle build, install APK, test all 16 layers and core questions."
