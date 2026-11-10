import unittest

from merge_knowledge_assets import merge


def rec(rid, text, source="source-a"):
    return {
        "id": rid, "text": text, "approval": "candidate_not_authoritative",
        "source_id": source, "source_version": "v1", "source_section": "section",
        "source_path": "fixture.json", "record_type": "knowledge_chunk",
        "audience": "general", "domain": "test", "language": "uz",
    }


class MergeKnowledgeAssetsTests(unittest.TestCase):
    def test_identical_id_and_text_merge_without_duplicate(self):
        active = [rec("A", "Bir xil matn", "old-source")]
        candidate = [rec("A", "Bir xil matn", "new-source")]
        merged, stats = merge(active, candidate)
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["id"], "A")
        self.assertEqual(stats["same_id_same_text"], 1)
        self.assertEqual(merged[0]["legacy_provenance"][0]["source_id"], "old-source")

    def test_changed_text_preserves_previous_version_and_search_alias(self):
        active = [rec("A", "Oldingi mazmun")]
        candidate = [rec("A", "Yangi mazmun")]
        merged, stats = merge(active, candidate)
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["text"], "Yangi mazmun")
        self.assertEqual(merged[0]["legacy_versions"][0]["text"], "Oldingi mazmun")
        self.assertIn("Oldingi mazmun", merged[0]["search_aliases"])
        self.assertEqual(stats["same_id_changed_text"], 1)

    def test_active_only_record_is_preserved(self):
        merged, stats = merge([rec("OLD", "Eski yozuv")], [rec("NEW", "Yangi yozuv")])
        self.assertEqual({x["id"] for x in merged}, {"OLD", "NEW"})
        self.assertEqual(stats["active_only_preserved"], 1)

    def test_different_ids_with_same_text_are_not_deleted(self):
        merged, stats = merge([], [rec("A", "Bir xil"), rec("B", "Bir xil")])
        self.assertEqual(len(merged), 2)
        self.assertEqual(stats["merged_count"], 2)

    def test_output_has_unique_ids(self):
        merged, stats = merge([rec("A", "bir")], [rec("A", "ikki"), rec("B", "uch")])
        ids = [x["id"] for x in merged]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(stats["unique_ids"], len(merged))


if __name__ == "__main__":
    unittest.main()
