# FINZANJIR v3 — Synthetic Bank Lab + Uzbek Offline Knowledge Core

Development branch: finzanjir-v3-synthetic-ai-uz

This is a separate development track. The existing main and concept-aligned-v1 branches are not overwritten.

## Run in Streamlit

Set the Streamlit main file path to:

    finzanjir_v3/app.py

Requirements:

    streamlit>=1.36,<2

## Synthetic bank laboratory

- Four fictional bank sources.
- 400 deterministic synthetic event scenarios.
- START / PAUSE / STOP / RESUME / RESET controls.
- SQLite queue and audit trail.
- Missing or contradictory fields route to DATA_REVIEW.
- Multi-indicator cases route to HUMAN_REVIEW.
- Other events route to MONITOR.
- A response package is prepared for demonstration; no real bank API call is made.

Pause and stop retain queued events. Resume continues the remaining queue. Reset requires explicit confirmation.

## Offline Uzbek AI

The first AI stage is an extractive evidence retrieval assistant, not a generative LLM. It makes no network calls and uses the included Uzbek knowledge cards extracted from the supplied V317 source package.

All imported cards are marked candidate_not_authoritative. The assistant:
- returns source-linked knowledge excerpts;
- abstains when matching evidence is insufficient;
- never promotes candidate material into authoritative knowledge;
- does not issue legal or fraud verdicts.

A true generative offline model (for example Qwen GGUF through a local runtime) is a later, separate integration gate. The V317 archive documents a Qwen3-1.7B integration candidate, but it explicitly does not establish that Android JNI, model loading, APK packaging, or on-device inference have passed.

## Important limitations

This is a prototype test harness, not a bank integration or production system. The scenario labels are synthetic expected labels and require expert validation. The rule outcomes are not measured fraud probabilities. No cards, accounts, or transactions are blocked.
