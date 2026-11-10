# FINZANJIR v3 — deployment and privacy gate

This checklist is a release gate, not a claim that the prototype is production-ready.

## Public and author views

- [x] Default public route opens the card-based public demo home page.
- [x] Public visitors can open synthetic demo pages without authentication.
- [x] Author analytics is not linked from public navigation.
- [x] Other visitors' feedback is not rendered on public pages.
- [x] Feedback collection remains closed unless all three explicit configuration gates are enabled.
- [x] Tavily search is OFF by default; explicit `enabled = true` is required and an app-level daily request budget is enforced.
- [ ] Confirm Tavily account is on the free tier with paid overages/pay-as-you-go disabled.
- [x] Citizen-facing page is informational only; no personal case lookup is exposed.
- [x] Author analytics is reachable only through the non-public `?view=author` route and requires the configured author password.
- [x] No default author password exists.
- [ ] Verify both routes in a real deployed browser on mobile and desktop.
- [ ] Verify that direct requests to `?view=author` show only the login gate before authentication.
- [ ] Verify logout and the 15-minute inactivity expiry in a real browser.

## Required before accepting real visitor feedback

- [ ] Configure a durable private database. The current visitor store is SQLite on the app filesystem; hosted ephemeral filesystems may lose data on restart/redeploy.
- [ ] Only after storage is verified, set `visitor_analytics.feedback_enabled = true`, `durable_storage_confirmed = true`, and `privacy_notice_reviewed = true` in Streamlit Secrets. These flags are acknowledgements, not technical proof of persistence.
- [ ] Configure automated encrypted backups and test restoration.
- [ ] Define retention period and a deletion process for feedback and analytics.
- [ ] Review who can access the database, deployment logs, backups, and secrets.
- [ ] Review the hosting provider's own request/logging practices. The application code does not intentionally store IP/GPS/raw user-agent data, but this does not mean the hosting platform or infrastructure never processes connection metadata.
- [ ] Publish a legally reviewed privacy notice explaining purpose, fields, retention, contact, and deletion rights.
- [ ] Test database outage, duplicate submission, malformed input, and concurrent submissions.
- [ ] Keep real card, account, identity, authentication, and other sensitive data out of feedback.

## Author authentication limitations

- Passwords are stored as PBKDF2-SHA256 hashes, not plaintext.
- Failed attempts are currently limited per app session. This is a basic deterrent and can be bypassed by creating a new session; it is not distributed rate limiting.
- A 15-minute inactivity timeout is implemented in application session state. It must be tested against the deployed Streamlit runtime.
- Use a long random `session_hmac_secret` (at least 32 random bytes encoded as text) and a password of at least 12 characters.
- Store secrets only in the hosting platform's secret manager. Never send them in chat or commit them to Git.

## Repository data audit — unresolved exposure

- The legacy root-level `finzanjir.db` was inspected at the SQLite string/schema level. It contains the old `cases` and `audit_log` tables, synthetic-looking IDs such as `CARD-xxx`, `TX-xxxxx`, `CASE-xxxx`, and legacy decisions including `BLOCKED`.
- These entries appear consistent with the old prototype's generated records, but their provenance and full row contents have not been independently established. Do not treat them as verified synthetic data.
- The v3 application does not read this database; it uses its own `finzanjir_v3/synthetic_lab.sqlite3` store. The legacy file should not be included in the v3 deployment branch.
- The repository is currently public. Removing the file from the current branch does not erase it from earlier commits or the `main` branch. Before public launch, make the source repository private or perform a coordinated Git-history cleanup and verify no sensitive data remains. The Streamlit app itself can be publicly viewable while source access is restricted.
- Do not enable real feedback collection until durable private storage, backups, retention/deletion, and privacy review are completed.

## Release decision

**Current status: NOT READY for real public feedback.**

The code has a public synthetic-demo route and a password-gated author route. Repository database exposure and live browser checks remain release blockers for public deployment. Durable storage, retention/deletion, backups, and privacy review remain blockers for accepting real visitor feedback.
