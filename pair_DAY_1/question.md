# Question — Day 1

**Topic:** Inference-time mechanics
**Subtopic:** The actual cost of a single inference call broken into prefill and decode phases
**Asker:** Atnabon Deressa
**Partner (explainer):** Efrate
**Date:** 2026-05-04
**Status:** Final (post morning-call)

---

## My sharpened question

> When my Tenacious-Bench evaluator calls `qwen3-next-80b-a3b` to score a
> candidate email — long rubric and style guide in the prompt, short JSON
> verdict out — what fraction of the per-call dollar figure I log in
> `cost_log.md` is **prefill** (one-shot, scaling with input tokens) versus
> **decode** (per-output-token, scaling with sampling) at the *provider's*
> billing layer, and through what concrete mechanism does prefix caching
> change the prefill side without changing the decode side?

## Why this is the gap I picked (asker's triage)

I read [`sales-eval-bench/cost_log.md`](../../sales-eval-bench/cost_log.md)
as a hostile reviewer this morning and surfaced four candidate gaps. (1)
"Why DeepSeek vs Qwen vs GPT-5 for synthesis?" — discarded; that is a price
shopping question I can already defend. (2) "How is `claude-sonnet-4.6
$0.412` calculated end-to-end?" — discarded; OpenRouter's pricing page
answers it. (3) "What is the variance on a single per-call cost?" — kept
as a candidate but it is statistical, not mechanistic. (4) **"What is the
prefill / decode split inside one of these numbers?"** — this is the one.
Every row in my cost log puts a long rubric (~ 1,200 input tokens) in
front of a short verdict (~ 80 output tokens). My audit memo and methodology
both *assume* the cost shape lets me afford the rubric-in-prompt design.
I cannot defend that assumption without the split, and I cannot project
what happens to my budget when the rubric grows by 30 % for v0.2.

## Connection to a specific Week 11 artifact

**Artifact:** [`sales-eval-bench/cost_log.md`](../../sales-eval-bench/cost_log.md)
(every row), and the design choice in [`sales-eval-bench/evaluator/scoring_evaluator.py`](../../sales-eval-bench/evaluator/scoring_evaluator.py)
to ship the rubric inside the user prompt rather than as a constrained-output
schema.

**Current claim/choice in that artifact:**

> | 12:38 | dataset_authoring | Judge filter pass — pointwise on 240 candidates | qwen3-next-80b-a3b | $0.288 |
>
> (Single dollar amount. No prefill/decode split. No prefix-cache hit-rate.
> Methodology defends the rubric-in-prompt design with a one-line cost
> claim that I cannot decompose if pressed.)

**What closing this gap will let me change:**

After the explainer lands I will (a) re-run a representative call with
provider-side usage breakdown logged (`input_tokens`, `cached_input_tokens`,
`output_tokens`), (b) add a `prefill_usd / decode_usd / prefix_cache_hit`
triple to every row in `cost_log.md` going forward, and (c) rewrite the
methodology paragraph that defends rubric-in-prompt to cite the actual
prefill share, not a hand-wave. If the prefill share is over ~ 70 %, the
rationale changes: rubric-in-prompt is only defensible because prefix
caching makes the rubric ~ free after the first call, and that
dependency must be named.

## Four-property self-check

- [x] **Diagnostic** — names the specific mechanism (provider-side prefill / decode billing split + prefix-cache effect on prefill), not "LLM costs" in general.
- [x] **Grounded in cohort work** — names `cost_log.md` rows and the rubric-in-prompt choice in `scoring_evaluator.py`.
- [x] **Generalizable** — every FDE who ships a long-prompt / short-output evaluator or agent has this gap; the same decomposition recipe applies.
- [x] **Resolvable** — 600–1,000 words can cover the prefill/decode mechanism, the prefix-cache invalidation rules, and a measurement recipe with one provider's usage object.
