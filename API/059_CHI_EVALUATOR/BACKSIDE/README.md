# 59_CHI_EVALUATOR

chi-Evaluator v2, pulled out of `API 2\\01_chi-evaluator` into a front folder. Each note's claims are scored on the Master Equation's ten channels
(chi = G x M x E x S_eff x T x K x R x Q x F x C), then synthesized into four statements: 2 calls per claim, DeepSeek only (OpenAI is off).

Same buttons as every station: `1 RUN HERE`, `2 RUN ON FOLDER` (pick input and output folder, how many at once). Papers run in parallel.
Code: `vendor/chi_evaluator` (copy of the original, one change: calls go through the relay), driven by `engine/bundle.py` step `chi`.
Results: `<note> · 59_CHI.md` flat in the output folder, JSON in `_json\\`, and the layer on the note. Needs `pip install openai openpyxl`.
