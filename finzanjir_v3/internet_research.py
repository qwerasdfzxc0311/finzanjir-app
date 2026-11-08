"""Explicit, source-linked web search for the FINZANJIR demo.
Only the visitor's query is sent to Tavily. Search results are untrusted evidence,
not instructions and not authoritative FINZANJIR rules.
"""
from __future__ import annotations
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

class InternetSearchError(Exception):
    pass

def search_web(query: str, api_key: str, max_results: int = 5) -> list[dict]:
    query = str(query or "").strip()
    if not query:
        raise InternetSearchError("Qidiruv so‘rovi bo‘sh.")
    if len(query) > 500:
        raise InternetSearchError("So‘rov 500 belgidan oshmasligi kerak.")
    if not api_key or len(str(api_key).strip()) < 10:
        raise InternetSearchError("Tavily API kaliti sozlanmagan.")
    payload = {
        "api_key": str(api_key).strip(),
        "query": query,
        "search_depth": "basic",
        "max_results": max(1, min(int(max_results), 5)),
        "include_answer": False,
        "include_raw_content": False,
    }
    request = Request(
        "https://api.tavily.com/search",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=15) as response:
            data = json.loads(response.read(1_500_000).decode("utf-8"))
    except HTTPError as exc:
        if exc.code in (401, 403):
            raise InternetSearchError("API kaliti noto‘g‘ri yoki ruxsat yo‘q.") from None
        if exc.code == 429:
            raise InternetSearchError("Qidiruv xizmati limitiga yetildi. Keyinroq urinib ko‘ring.") from None
        raise InternetSearchError("Tashqi qidiruv xizmati HTTP xatosi (" + str(exc.code) + ").") from None
    except (URLError, TimeoutError):
        raise InternetSearchError("Streamlit serveridan internetga ulanish yoki vaqt tugashi muammosi.") from None
    except (ValueError, UnicodeDecodeError):
        raise InternetSearchError("Qidiruv xizmatidan tushunarsiz javob olindi.") from None
    items = []
    for row in data.get("results", []):
        url = str(row.get("url", "")).strip()
        title = str(row.get("title", "")).strip()[:300]
        content = str(row.get("content", "")).strip()[:2500]
        if url.startswith(("https://", "http://")) and title and content:
            items.append({
                "title": title,
                "url": url,
                "content": content,
                "score": round(float(row.get("score", 0) or 0), 3),
            })
    return items
