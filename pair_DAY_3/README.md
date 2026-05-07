# Day 3 — Training & post-training (LoRA design knobs)

**Status:** Submitted (async pair-day).
**Date:** 2026-05-07
**Pair:** Atnabon Deressa ↔ Yohannes Dereje
**My question (asker):** LoRA rank vs adapter expressivity (r=8 / r=16 / r=32) — see [`question.md`](question.md).
**Partner's question (explainer):** Why Q+V-only LoRA suppresses banned phrases but cannot generate required ones — see [`explainer.md`](explainer.md).
**Pair-day theme:** The two questions deliberately cover the two main LoRA design knobs — Yohannes asks *which* weight matrices LoRA touches (target modules); I ask *how much* expressive capacity per matrix (rank). Together they cover the LoRA design space.
**Honesty note:** This pair-day ran asynchronously over Slack rather than as live morning + evening calls (partner had unreliable battery / connectivity through the afternoon). See [`morning_call_summary.md`](morning_call_summary.md) and [`evening_call_summary.md`](evening_call_summary.md) for the actual record. Sign-off and grounding-commit are marked **pending** in their respective files until partner confirms.

## Pre-staged candidate gaps (so Act II is real triage, not blank-page)

| Topic | Subtopic | Candidate gap I have already surfaced from my work | Anchor artifact |
|---|---|---|---|
| Training & post-training | DPO vs SimPO vs ORPO gradient mechanics | I picked SimPO for the Tenacious judge over DPO. My justification in the methodology doc is "lower memory and no reference model"; I cannot defend the gradient mechanics that make that trade-off real (length-normalized log-likelihood vs reference-anchored). | [`sales-eval-bench/methodology.md`](../../sales-eval-bench/methodology.md), [`sales-eval-bench/training/`](../../sales-eval-bench/training/) |
| Training & post-training | Reward-model overoptimization & KL | I have no KL term in my SimPO recipe and I do not actually understand why SimPO claims to need none. | [`sales-eval-bench/methodology_rationale.md`](../../sales-eval-bench/methodology_rationale.md) |
| Multimodal & embedding | Embedding-space geometry & cosine | The `enrich` step in Conversion Engine does similarity search over public-signal documents. I quote cosine similarity without being able to defend why cosine vs dot-product matters once the embedding model is normalized. | [`conversion-engine/agent/enrich.py`](../../conversion-engine/agent/enrich.py) |
| Evaluation & statistics | LLM-as-a-judge biases (length / position / self-preference) | _(Already used as Day 1 anchor — re-use only if the cohort lands here on Day 3 with a different sub-aspect, e.g. position bias in pairwise.)_ | — |
| Production patterns | Prompt-caching mechanics | _(Same as Day 2 candidate. Use here if Day 2 voted differently.)_ | [`conversion-engine/agent/draft.py`](../../conversion-engine/agent/draft.py) |
| Inference-time mechanics | Speculative decoding | I do not run speculative decoding anywhere; the gap is whether I should at the eval-tier judge call where Sonnet 4.6 dominates cost. | [`sales-eval-bench/cost_log.md`](../../sales-eval-bench/cost_log.md) |

## Files in this folder

Templates pre-populated from `_templates/`. Fill in across the day per the brief.
