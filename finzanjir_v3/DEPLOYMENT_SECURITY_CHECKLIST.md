# FINZANJIR v3 — deployment and privacy gate

This checklist is a release gate, not a claim that the prototype is production-ready.

## Public and author views

- [x] Default public route displays only the visitor feedback page.
- [x] Public sidebar navigation is hidden.
- [x] Other visitors' feedback is not rendered on public pages.
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

## Repository data audit — unresolved

- The repository contains a legacy root-level `finzanjir.db` SQLite file that is not used by the v3 lab or visitor store.
- Its contents have not yet been audited, so it must not be assumed to contain only synthetic or non-sensitive data.
- Do not collect real visitor feedback or publish the repository as a public source until this file has been inspected.
- Removing the file from the current branch alone would not erase it from earlier Git commits. If sensitive data is found, treat it as an exposure: restrict repository access, rotate any credentials found, and plan a coordinated Git-history cleanup. History rewriting can invalidate existing clones and must be handled deliberately.

## Release decision

**Current status: NOT READY for real public feedback.**

The code has a feedback-only public route and a password-gated author route, but durable storage, deployment/browser checks, repository database audit, retention/deletion, and hosting privacy review remain outstanding.
