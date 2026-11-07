# FINZANJIR — concept-aligned prototype

This folder is a separate experimental implementation. Existing root-level app.py and files are intentionally untouched.

## Run
Python 3.10+:
- pip install -r finzanjir_v2/requirements.txt
- streamlit run finzanjir_v2/app.py

## Test
- cd finzanjir_v2
- python -m unittest -v

## Implemented in this prototype
- Local SQLite event, Case, and audit records.
- Deterministic signal checks with signal IDs and source fields.
- Explicit unknowns when history or fields are missing.
- Provisional Case-review heuristic; no automatic blocking.
- Human review outcomes and audit entries.
- Local pseudonym-attribute relationship view.
- Synthetic demo data and conservative 16-layer status panel.

## Limitations
- No real bank/payment integration or cross-bank data.
- No production identity, access control, encryption/key management, retention policy, or immutable audit.
- Synthetic and manually entered test data only.
- Weights and Case criteria are provisional assumptions, not calibrated probabilities.
- No FP/FN/precision/recall claims without independently labelled ground truth.
- A signal, score, Case, or graph relationship is not proof of fraud or guilt.
- No card or transaction blocking. The prototype does not replace banks, law enforcement, or human decisions.
