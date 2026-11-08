from __future__ import annotations
import hashlib, hmac, os, secrets, sqlite3, time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VISITOR_DB = Path(os.environ.get("FINZANJIR_VISITOR_DB", str(ROOT / "visitor_analytics.sqlite3")))
MAX_TEXT = 4000
ADMIN_SESSION_TTL_SECONDS = 15 * 60
ADMIN_LOGIN_WINDOW_SECONDS = 15 * 60
ADMIN_LOGIN_MAX_ATTEMPTS = 5

def _now():
    return datetime.now(timezone.utc).isoformat()

def _connect():
    VISITOR_DB.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(str(VISITOR_DB), timeout=15)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA foreign_keys=ON")
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("PRAGMA busy_timeout=15000")
    return c

def init_store():
    with _connect() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS visits(session_key TEXT PRIMARY KEY,first_seen TEXT NOT NULL,last_seen TEXT NOT NULL,device_family TEXT NOT NULL,os_family TEXT NOT NULL,browser_family TEXT NOT NULL,page_count INTEGER NOT NULL DEFAULT 0);
        CREATE TABLE IF NOT EXISTS page_events(id INTEGER PRIMARY KEY AUTOINCREMENT,session_key TEXT NOT NULL,page_name TEXT NOT NULL,event_type TEXT NOT NULL,created_at TEXT NOT NULL,FOREIGN KEY(session_key) REFERENCES visits(session_key));
        CREATE TABLE IF NOT EXISTS feedback(id INTEGER PRIMARY KEY AUTOINCREMENT,created_at TEXT NOT NULL,usefulness TEXT NOT NULL,missing TEXT NOT NULL,improve TEXT NOT NULL,feature TEXT NOT NULL,concerns TEXT NOT NULL,collaboration TEXT NOT NULL,name TEXT NOT NULL DEFAULT '',contact TEXT NOT NULL DEFAULT '',extra TEXT NOT NULL DEFAULT '');
        CREATE TABLE IF NOT EXISTS admin_login_attempts(session_key TEXT PRIMARY KEY,window_started REAL NOT NULL,attempts INTEGER NOT NULL,locked_until REAL NOT NULL DEFAULT 0);
        CREATE INDEX IF NOT EXISTS idx_events_time ON page_events(created_at);
        CREATE INDEX IF NOT EXISTS idx_feedback_time ON feedback(created_at);
        """)

def _classify_device(user_agent):
    ua = (user_agent or "").lower()
    device, os_name, browser = "Noma'lum qurilma", "Noma'lum OS", "Noma'lum brauzer"
    if any(x in ua for x in ("iphone", "ipad", "ipod")):
        device, os_name = "Apple qurilmasi (taxminiy)", "iOS/iPadOS"
    elif "android" in ua:
        os_name = "Android"
        if "samsung" in ua: device = "Samsung (model kafolatlanmaydi)"
        elif any(x in ua for x in ("xiaomi", "redmi", "poco")): device = "Xiaomi/Redmi/POCO (taxminiy)"
        elif any(x in ua for x in ("huawei", "honor")): device = "Huawei/Honor (taxminiy)"
        elif any(x in ua for x in ("oppo", "realme")): device = "OPPO/realme (taxminiy)"
        else: device = "Android qurilmasi (marka noma'lum)"
    elif "windows" in ua: device, os_name = "Kompyuter", "Windows"
    elif "mac os" in ua or "macintosh" in ua: device, os_name = "Apple kompyuteri", "macOS"
    elif "linux" in ua: device, os_name = "Kompyuter", "Linux"
    if "edg/" in ua: browser = "Microsoft Edge"
    elif "firefox/" in ua: browser = "Firefox"
    elif "opr/" in ua or "opera" in ua: browser = "Opera"
    elif "chrome/" in ua and "chromium" not in ua: browser = "Chrome"
    elif "safari/" in ua and "chrome/" not in ua: browser = "Safari"
    return device, os_name, browser

def _session_key(session_id, secret):
    return hmac.new(secret.encode(), session_id.encode(), hashlib.sha256).hexdigest()

def record_page_view(session_id, page_name, user_agent, secret):
    if not session_id or not secret:
        return
    init_store()
    key = _session_key(session_id, secret)
    stamp = _now()
    device, os_name, browser = _classify_device(user_agent)
    with _connect() as c:
        c.execute("""INSERT INTO visits VALUES(?,?,?,?,?,?,1)
        ON CONFLICT(session_key) DO UPDATE SET last_seen=excluded.last_seen,page_count=visits.page_count+1""",
        (key, stamp, stamp, device, os_name, browser))
        c.execute("INSERT INTO page_events(session_key,page_name,event_type,created_at) VALUES(?,?,?,?)",
        (key, str(page_name)[:100], "PAGE_VIEW", stamp))

def save_feedback(data):
    init_store()
    fields = ["usefulness", "missing", "improve", "feature", "concerns", "collaboration", "name", "contact", "extra"]
    values = [str(data.get(k, "")).strip()[:MAX_TEXT] for k in fields]
    if not any(values[:6] + values[8:]):
        raise ValueError("Kamida bitta fikr yoki taklif yozing.")
    with _connect() as c:
        c.execute("INSERT INTO feedback(created_at,usefulness,missing,improve,feature,concerns,collaboration,name,contact,extra) VALUES(?,?,?,?,?,?,?,?,?,?)",
        (_now(), *values))

def verify_admin_password(password, encoded):
    try:
        if not isinstance(password, str) or len(password) > 1024:
            return False
        algorithm, rounds, salt_hex, expected_hex = encoded.split("$", 3)
        iterations = int(rounds)
        if algorithm != "pbkdf2_sha256" or not 200000 <= iterations <= 2000000:
            return False
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(expected_hex)
        if len(salt) < 16 or len(expected) != 32:
            return False
        actual = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
        return hmac.compare_digest(actual, expected)
    except Exception:
        return False

def make_password_hash(password, iterations=310000):
    if not isinstance(password, str) or len(password) < 12:
        raise ValueError("Muallif paroli kamida 12 belgidan iborat bo‘lsin.")
    if not 200000 <= int(iterations) <= 2000000:
        raise ValueError("PBKDF2 iteratsiyasi ruxsat etilgan chegarada bo‘lishi kerak.")
    salt = secrets.token_bytes(16)
    derived = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, int(iterations))
    return "pbkdf2_sha256$" + str(int(iterations)) + "$" + salt.hex() + "$" + derived.hex()

def admin_login_status(session_id, secret, now=None):
    if not session_id or not secret:
        return {"allowed": False, "retry_after": ADMIN_LOGIN_WINDOW_SECONDS, "attempts_left": 0}
    now = float(now if now is not None else time.time())
    init_store()
    key = _session_key(session_id, secret)
    with _connect() as c:
        row = c.execute("SELECT window_started,attempts,locked_until FROM admin_login_attempts WHERE session_key=?", (key,)).fetchone()
    if not row:
        return {"allowed": True, "retry_after": 0, "attempts_left": ADMIN_LOGIN_MAX_ATTEMPTS}
    if row["locked_until"] > now:
        return {"allowed": False, "retry_after": int(row["locked_until"] - now) + 1, "attempts_left": 0}
    if now - row["window_started"] >= ADMIN_LOGIN_WINDOW_SECONDS:
        return {"allowed": True, "retry_after": 0, "attempts_left": ADMIN_LOGIN_MAX_ATTEMPTS}
    return {"allowed": row["attempts"] < ADMIN_LOGIN_MAX_ATTEMPTS, "retry_after": 0,
            "attempts_left": max(0, ADMIN_LOGIN_MAX_ATTEMPTS - row["attempts"])}

def record_admin_login_attempt(session_id, secret, success, now=None):
    if not session_id or not secret:
        return
    now = float(now if now is not None else time.time())
    init_store()
    key = _session_key(session_id, secret)
    with _connect() as c:
        if success:
            c.execute("DELETE FROM admin_login_attempts WHERE session_key=?", (key,))
            return
        row = c.execute("SELECT window_started,attempts FROM admin_login_attempts WHERE session_key=?", (key,)).fetchone()
        if not row or now - row["window_started"] >= ADMIN_LOGIN_WINDOW_SECONDS:
            started, attempts = now, 0
        else:
            started, attempts = row["window_started"], row["attempts"]
        attempts += 1
        locked_until = now + ADMIN_LOGIN_WINDOW_SECONDS if attempts >= ADMIN_LOGIN_MAX_ATTEMPTS else 0
        c.execute("""INSERT INTO admin_login_attempts(session_key,window_started,attempts,locked_until)
        VALUES(?,?,?,?) ON CONFLICT(session_key) DO UPDATE SET
        window_started=excluded.window_started,attempts=excluded.attempts,locked_until=excluded.locked_until""",
        (key, started, attempts, locked_until))

def admin_snapshot():
    init_store()
    with _connect() as c:
        visitors = c.execute("SELECT COUNT(*) FROM visits").fetchone()[0]
        page_views = c.execute("SELECT COUNT(*) FROM page_events").fetchone()[0]
        feedback_count = c.execute("SELECT COUNT(*) FROM feedback").fetchone()[0]
        devices = [dict(r) for r in c.execute("SELECT device_family,os_family,browser_family,COUNT(*) sessions FROM visits GROUP BY 1,2,3 ORDER BY sessions DESC")]
        popular = [dict(r) for r in c.execute("SELECT page_name,COUNT(*) views FROM page_events GROUP BY page_name ORDER BY views DESC")]
        recent = [dict(r) for r in c.execute("SELECT first_seen,last_seen,device_family,os_family,browser_family,page_count FROM visits ORDER BY last_seen DESC LIMIT 200")]
        feedback = [dict(r) for r in c.execute("SELECT * FROM feedback ORDER BY id DESC LIMIT 500")]
    return {"visitors": visitors, "page_views": page_views, "feedback_count": feedback_count,
            "devices": devices, "popular_pages": popular, "recent_visits": recent, "feedback": feedback}
