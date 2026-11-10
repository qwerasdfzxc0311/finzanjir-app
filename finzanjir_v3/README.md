# FINZANJIR v3 — Synthetic Bank Lab + Uzbek Offline Knowledge Core

Development branch: finzanjir-v3-synthetic-ai-uz

This is a separate development track. The existing main and concept-aligned-v1 branches are not overwritten.

## Run in Streamlit

Set the Streamlit main file path to:

    finzanjir_v3/app.py

Requirements (repository root):

    streamlit>=1.36,<2
    streamlit-autorefresh>=1.0.1,<2

## Synthetic bank laboratory

- Four fictional bank sources.
- 400 deterministic synthetic event scenarios.
- START / PAUSE / STOP / RESUME / RESET and emergency KILL SWITCH controls.
- SQLite queue and audit trail.
- Missing or contradictory fields route to DATA_REVIEW.
- A single unresolved indicator routes to RECHECK.
- Multi-indicator cases route to HUMAN_REVIEW.
- No detected indicator routes to MONITOR.
- Public card-based home page with open synthetic demo pages.
- Historical UX restored safely: signal registry, pseudonymous graph, audit journal, KPI panel and honest 16-layer status panel.
- Separate synthetic interbank attribute-match view and citizen-facing explanation page; no real citizen case lookup.
- Dashboard/lab/events pages auto-refresh while monitoring.
- A response package is prepared for demonstration; no real bank API call is made.

Pause and stop retain queued events. Resume continues the remaining queue. L11 emergency KILL SWITCH locks normal controls until an operator explicitly confirms recovery. Reset requires explicit confirmation and is blocked during emergency stop.

## Offline Uzbek AI

The first AI stage is an extractive evidence retrieval assistant, not a generative LLM. It makes no network calls and uses the included Uzbek knowledge cards extracted from the supplied V317 source package.

All imported cards are marked candidate_not_authoritative. The assistant:
- returns source-linked knowledge excerpts;
- abstains when matching evidence is insufficient;
- never promotes candidate material into authoritative knowledge;
- does not issue legal or fraud verdicts.

A true generative offline model (for example Qwen GGUF through a local runtime) is a later, separate integration gate. The V317 archive documents a Qwen3-1.7B integration candidate, but it explicitly does not establish that Android JNI, model loading, APK packaging, or on-device inference have passed.

## Important limitations

This is a prototype test harness, not a bank integration or production system. Scenario labels are not used by the classifier; outcomes are derived from synthetic payload fields. Duplicate transport is metadata-only (two attempts indicated), not a real webhook retry/delivery test. The scenario labels are synthetic expected labels and require expert validation. The rule outcomes are not measured fraud probabilities. No cards, accounts, or transactions are blocked.


## Private visitor feedback and analytics

- Public visitors can open the synthetic demo pages without signing in. Feedback is closed by default until durable storage and privacy requirements are verified; name and contact fields remain optional when enabled.
- Feedback is not shown to other visitors. It is only displayed in the author-only panel after password verification.
- The author panel is not listed in public navigation. It is routed through the private ?view=author view and still requires a password; hiding the menu entry is not treated as an access-control boundary.
- The author panel stays disabled unless Streamlit Secrets contains both visitor_analytics.admin_password_hash and visitor_analytics.session_hmac_secret. No default password exists.
- Generate a PBKDF2 password hash in a trusted local Python environment by importing visitor_analytics and calling make_password_hash("your-strong-password"). The password must be at least 12 characters. Store only the returned hash in Streamlit Secrets. Never commit plaintext passwords or secrets.
- session_hmac_secret must be a long random secret (at least 32 random bytes encoded as text).
- Failed author logins are limited to five attempts per app session in a 15-minute window. This is a basic prototype control, not a substitute for platform-level identity controls or distributed rate limiting.
- Author login expires after 15 minutes of inactivity. The session is refreshed while the protected panel is actively used.
- SQLite uses WAL and a busy timeout. This improves local concurrent access but does not make Streamlit local disk persistent. Configure a durable private database before collecting real public feedback.
- The module records page views, a random per-app-session pseudonym, approximate device/OS/browser family, and last activity. It does not store IP addresses, GPS, raw user-agent strings, or browser fingerprinting data.
- Device brand/model detection is approximate and may be masked. Counts represent app sessions, not verified unique people.
- Browser close/exit time cannot be reliably determined; last activity is shown. Code copying cannot be reliably detected.
- Streamlit-hosted local SQLite storage may be ephemeral. Before public real-world use, configure durable private storage, access controls, backups, retention/deletion policy, and a suitable privacy notice after legal review.
- The feedback form advises visitors not to submit card numbers, PIN, CVV, OTP, passwords, identity documents, or other sensitive financial/personal data.
- Feedback text is rendered as plain text in the author panel to reduce markup/script injection risk.

## User interface and author access update

- The default public route opens a mobile-friendly card-based home page. Synthetic dashboards, lab, case/review, signal registry, graph, audit, KPI, AI and explanation pages are publicly viewable.
- The author analytics page is not linked from public navigation and is reachable only through `?view=author` plus the configured password gate. Other visitors' feedback is never displayed publicly.
- The citizen explanation page is informational only; there is no real citizen case lookup or personal-data portal.
- The author view is reachable through the non-public `?view=author` route and then a password gate. The route itself is not a security control.
- Public pages now explain the prototype purpose and limitations in plain Uzbek. Technical sections include short explanations of START/PAUSE/STOP/RESET, Signal, and Case.
- The feedback page is grouped into clear sections and labels; contact details remain optional.
- This is a prototype, not production-secure until deployment configuration and access-control tests are completed.


## Deployment security gate

See [DEPLOYMENT_SECURITY_CHECKLIST.md](DEPLOYMENT_SECURITY_CHECKLIST.md). The checklist records the remaining requirements before real public feedback can be accepted. Current status: **synthetic public demonstration may be deployed after the repository data exposure is resolved and live browser checks pass; real feedback collection remains disabled** until durable storage, backups, retention/deletion, and privacy review are completed.


### Feedback collection activation gate

The public feedback form is **closed by default**. It accepts submissions only when all three boolean Streamlit Secrets are explicitly set to true under `visitor_analytics`: `feedback_enabled`, `durable_storage_confirmed`, and `privacy_notice_reviewed`. Do not enable these flags until a durable private database/volume, backups, retention/deletion process, and reviewed privacy notice are actually in place. These flags are an operator acknowledgement, not a technical proof that the hosting filesystem is persistent.


## Optional internet research

- The AI page has separate local-knowledge and internet-search modes, plus a comparison mode.
- Internet search is explicit and user-triggered; it is not silently run in the background.
- Configure Tavily only in Streamlit Secrets. Example (replace the placeholder locally; never commit or send a real key):

```toml
[internet_research]
enabled = true
api_key = "YOUR_TAVILY_API_KEY"
max_daily_requests = 25
```

- Internet search is OFF unless `enabled = true` is explicitly set. The app enforces a default 25-search daily budget (configurable up to 100) using a local SQLite counter. Hosted restarts/ephemeral storage can reset this app-level guard, so it is not a billing cap. Keep Tavily on the free plan and disable pay-as-you-go/paid overages in the Tavily account.
- Only the visitor's search query is sent to Tavily; do not enter personal, card, customer, credential, or confidential bank data.
- The app displays source titles, URLs, and short search excerpts. It does not treat web text as trusted instructions or automatically add it to the FINZANJIR knowledge base.
- Internet search requires outbound network access from the Streamlit hosting environment and a valid API key; this is not a direct unrestricted browser or a live bank-data connection.
- Test module: `python -m unittest discover -s finzanjir_v3 -p 'test_internet_research.py'`.
