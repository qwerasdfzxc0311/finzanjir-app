"""Explicit, source-linked web search for the FINZANJIR demo.
Only the visitor's query is sent to Tavily. Search results are untrusted evidence,
not instructions and not authoritative FINZANJIR rules.
"""
from __future__ import annotations
import json, sqlite3
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

USAGE_DB = Path(__file__).resolve().with_name("internet_search_usage.sqlite3")

class InternetSearchError(Exception):
    pass

def reserve_daily_slot(max_daily_requests: int = 25, now=None) -> bool:
    """Reserve one app-wide daily search slot; stores only the UTC date and count."""
    limit = max(1, min(int(max_daily_requests), 100))
    day = (now or datetime.now(timezone.utc)).date().isoformat()
    USAGE_DB.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(str(USAGE_DB), timeout=15) as conn:
        conn.execute("PRAGMA busy_timeout=15000")
        conn.execute("CREATE TABLE IF NOT EXISTS daily_usage(day TEXT PRIMARY KEY, requests INTEGER NOT NULL)")
        conn.execute("BEGIN IMMEDIATE")
        row = conn.execute("SELECT requests FROM daily_usage WHERE day=?", (day,)).fetchone()
        used = int(row[0]) if row else 0
        if used >= limit:
            conn.rollback()
            return False
        conn.execute(
            "INSERT INTO daily_usage(day,requests) VALUES(?,1) "
            "ON CONFLICT(day) DO UPDATE SET requests=daily_usage.requests+1",
            (day,)
        )
        conn.commit()
    return True

def search_web(query: str, api_key: str, max_results: int = 5,
               max_daily_requests: int = 25) -> list[dict]:
    query = str(query or "").strip()
    if not query:
        raise InternetSearchError("Qidiruv so‘rovi bo‘sh.")
    if len(query) > 500:
        raise InternetSearchError("So‘rov 500 belgidan oshmasligi kerak.")
    if not api_key or len(str(api_key).strip()) < 10:
        raise InternetSearchError("Tavily API kaliti sozlanmagan.")
    if not reserve_daily_slot(max_daily_requests):
        raise InternetSearchError("FINZANJIR demo uchun kunlik internet qidiruv limiti tugadi. Ertaga qayta urinib ko'ring.")
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
