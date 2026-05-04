# Day 1 — Inference-time mechanics

**Date:** 2026-05-04 (Mon)
**Topic:** Inference-time mechanics
**Subtopic (asker side):** The actual cost of a single inference call broken into prefill and decode phases
**Subtopic (explainer side):** Prefix-cache invalidation rules at the level a Forward-Deployed Engineer needs
**Pair:** Atnabon Deressa ↔ Efrate
**Submission deadline:** 2026-05-05 02:00 UTC

## Files

| File | Role | Status |
|---|---|---|
| [`question.md`](question.md) | Atnabon's sharpened question (asker side) | Final, post morning-call |
| [`morning_call_summary.md`](morning_call_summary.md) | What sharpened in the morning call | Final |
| [`explainer.md`](explainer.md) | The 600–1,000 word post **Atnabon wrote for Efrate** on prefix-cache invalidation | Post evening-call revision |
| [`thread.md`](thread.md) | 6-tweet thread for the explainer | Post evening-call revision |
| [`evening_call_summary.md`](evening_call_summary.md) | Asker feedback + revisions | Final |
| [`signoff.md`](signoff.md) | Atnabon's sign-off on Efrate's explainer to Atnabon's question | To be filled post evening call |
| [`grounding_commit.md`](grounding_commit.md) | Atnabon's planned edit to `sales-eval-bench/cost_log.md` + `methodology.md` + `scoring_evaluator.py` | Plan committed; SHA pending |
| [`sources.md`](sources.md) | Two canonical sources (DeepSeek-V2; Anthropic prompt-caching docs) + the OpenRouter probe | Final |

## Four-property check on `question.md`

- [x] **Diagnostic** — names the provider-side prefill / decode billing split + prefix-cache effect on prefill, not "LLM costs" in general.
- [x] **Grounded in cohort work** — names `cost_log.md` rows + the rubric-in-prompt design choice in `scoring_evaluator.py`.
- [x] **Generalizable** — every FDE who ships a long-prompt / short-output evaluator or agent has this gap.
- [x] **Resolvable** — 600–1,000 words is enough.

## Public-artifact quality bar (on `explainer.md` + `thread.md`)

- [x] Two canonical sources cited with links (DeepSeek-V2 paper; Anthropic prompt-caching docs).
- [x] Code or concrete demonstration a reader can run, inspect, or directly verify (the `usage.prompt_tokens_details.cached_tokens` probe).
- [ ] Tutor pre-publication review passed _(to be confirmed)_.
- [ ] Asker (Efrate) sign-off received on the post-revision version _(to be confirmed)_.
- [x] Tweet thread reads standalone (a reader who never clicks through still gets the mechanism).
- [x] Attribution clean — every paper, tool, and source credited; nothing fabricated.
