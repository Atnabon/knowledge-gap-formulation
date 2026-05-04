# Canonical — raw research artifacts

This folder holds the working artifacts behind each day's explainer:
hands-on tool runs, notebooks, downloaded paper PDFs (gitignored if licence
prohibits redistribution), and small synthetic-data demonstrations.

## Conventions

- One subfile or notebook per day: `day1_<topic>.ipynb`, `day2_<topic>.py`, …
- Notebooks must be runnable end-to-end on a stock Python 3.12 + numpy environment unless explicitly noted.
- Heavy artifacts (model checkpoints, large datasets) are referenced by URL, not committed.

## Day 1 — `day1_prefix_cache_probe.ipynb`

OpenRouter / OpenAI-compatible chat-completion probe referenced from
[`../pair_DAY_1/explainer.md`](../pair_DAY_1/explainer.md). Issues two
consecutive calls with the same long system prompt, logs
`usage.prompt_tokens_details.cached_tokens`, and confirms the byte-for-byte
tokenized-prefix invalidation rule by re-running with a per-call timestamp
prepended to the system prompt.

_(Days 2–5 land here as the week runs.)_
