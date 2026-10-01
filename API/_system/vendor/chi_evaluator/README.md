# chi_evaluator (vendored)

Copied 2026-10-01 from `API 2/01_chi-evaluator` (the newer copy: it has `synthesize_statements.py`). Only change: both `DEEPSEEK_BASE_URL`
lines read the environment, so calls pass through the relay (`engine/gateway.py`). Run by `engine/bundle.py` step `chi`, which copies these files
into a scratch folder per note, so the script's own INBOX/OUTBOX/config paths work unchanged. OpenAI is switched off there (only DeepSeek and mock are allowed).
Needs `pip install openai openpyxl`.
