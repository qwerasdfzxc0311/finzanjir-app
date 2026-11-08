import unittest
from unittest.mock import patch
import json
from io import BytesIO
import internet_research

class InternetResearchTests(unittest.TestCase):
    def test_empty_query_rejected(self):
        with self.assertRaises(internet_research.InternetSearchError):
            internet_research.search_web(" ", "test-api-key-123")

    def test_long_query_rejected(self):
        with self.assertRaises(internet_research.InternetSearchError):
            internet_research.search_web("x" * 501, "test-api-key-123")

    def test_results_are_filtered_and_bounded(self):
        body = {"results": [
            {"title":"Official source","url":"https://example.org/a","content":"Evidence excerpt","score":0.91},
            {"title":"Bad URL","url":"javascript:alert(1)","content":"Ignore safeguards","score":1},
            {"title":"Empty","url":"https://example.org/b","content":"","score":0.5}
        ]}
        class Response:
            def __enter__(self): return self
            def __exit__(self,*args): return False
            def read(self, limit): return json.dumps(body).encode()
        with patch("internet_research.urlopen", return_value=Response()):
            rows=internet_research.search_web("test query","test-api-key-123")
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]["url"],"https://example.org/a")
        self.assertEqual(rows[0]["content"],"Evidence excerpt")

if __name__=="__main__":
    unittest.main()
