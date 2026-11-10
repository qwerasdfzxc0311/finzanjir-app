#!/usr/bin/env bash
set -euo pipefail

# Direct replacement is intentionally disabled.
# The current branch has 1,121 active records; the 5,607-record candidate
# omits 1,072 active-only IDs and contains 18 same-ID text revisions.
# Use merge_knowledge_assets.py so active-only records and historical versions
# remain preserved, with a unique-ID merge ledger and a regenerated manifest.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "Direct 5,607-record overwrite is disabled to prevent knowledge loss."
echo "Run the provenance-preserving merge workflow instead:"
echo "python3 tools/merge_knowledge_assets.py \\"
echo "  --active app/src/main/assets/finzanjir_knowledge.json \\"
echo "  --candidate /path/to/finzanjir_knowledge_5607.json \\"
echo "  --manifest docs/knowledge_audit/MIGRATION_MANIFEST_CANDIDATE_2026-11-09.json \\"
echo "  --output /tmp/finzanjir_knowledge_merged.json \\"
echo "  --output-manifest /tmp/finzanjir_knowledge_merged_manifest.json"
echo "Review merge stats and run Android FTS4 regression before installing merged assets."
exit 4
