# FINZANJIR Native Offline Android

This project is a native Android demo port of the initial FINZANJIR Streamlit commit (`0b1cb9fd8ff23002ec5ee17da86e93b81d4441d2`). It is intentionally kept on a separate branch and does not modify the original Streamlit app.

## Build
GitHub Actions runs on pushes to `android-native-offline-2026-11-10` and can also be started manually from Actions. On success, download `FINZANJIR-native-offline-debug-apk` from the workflow run's Artifacts section.

## Offline behavior
The app uses local SQLite and contains no network permission, API key, hosted backend, or required model download. The Gemini explanation call from the original Streamlit app is omitted because it requires internet and a secret key; risk explanations use the original deterministic demo rules.

## Scope and limitations
This is a native Android demonstration, not a production banking security system. It is not connected to real banks, does not process real transactions, and does not actually block cards or payments. The original operator actions are represented only as local demo status labels. Some original Streamlit visualizations are simplified for native mobile screens.
