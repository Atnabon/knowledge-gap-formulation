# Question — Day 4

**Topic:** Evaluation & statistics
**Subtopic:** Statistical significance and confidence intervals on small binary-outcome eval sets
**Asker:** Atnabon Deressa
**Partner (explainer):** Zemzem Hibet
**Date:** 2026-05-08
**Status:** Final (post Slack correction)

---

## My sharpened question

> In `ablations/held_out_traces.jsonl`, I have 89 held-out transcripts scored by
> my LLM judge on a binary `regex_positive` / `regex_negative` rubric. My v0.2
> fails 3 of 89 on `regex_positive`. If v0.3 (with corrected LoRA targets) fails
> 0 instead of 3 — a 3.4 percentage-point improvement — I cannot explain whether
> that difference is statistically meaningful or sampling noise, what null
> hypothesis is appropriate for a rubric pass-rate comparison, or whether
> bootstrap resampling vs a binomial proportion test is the right method when
> N=89 and the outcome is binary.

## Why this is the gap I picked (asker's triage)

Coming into Day 4 I surfaced four candidate gaps. (1) LoRA rank per module after
expanding `target_modules` — rejected by my pair at first pass as a training
mechanics question, not evaluation and statistics. (2) "Which spans to instrument
in Langfuse?" — discarded; production observability, not evaluation methodology.
(3) "Rubric placement in the judge prompt (system vs user, top vs bottom)" — a
real gap but about prompt sensitivity, not statistical validity of a result.
(4) **"How do I know a 3-failure → 0-failure improvement on 89 samples is
real?"** — this is the one. The v0.2 → v0.3 comparison in `methodology.md`
currently asserts a directional improvement with no confidence interval or
significance test. A reviewer cannot judge whether the claim is meaningful or
within the margin of random variation on a small held-out set. The gap is
load-bearing for every version-comparison claim in the benchmark.

## Connection to a specific Week 10 or 11 artifact

**Artifact:** [`ablations/held_out_traces.jsonl`](../../sales-eval-bench/ablations/held_out_traces.jsonl)
and the v0.2 → v0.3 comparison section of [`methodology.md`](../../sales-eval-bench/methodology.md)

**Current claim/choice in that artifact:**

> v0.3 eliminates all 3 residual SOC failures observed in v0.2, improving
> `regex_positive` pass-rate from 96.6% to 100% on the 89-sample held-out set.

**What closing this gap will let me change:**

After Zemzem's explainer lands I will add a confidence interval and an explicit
significance test (or a clearly stated reason one is not applicable) to the
v0.2 vs v0.3 comparison table in `methodology.md`, so the improvement claim is
statistically defensible rather than directional only.

## Four-property self-check

- [x] **Diagnostic** — names a specific statistical question (null hypothesis
  and test selection for binary pass-rate comparison on N=89), not just "what
  is statistical significance?"
- [x] **Grounded in cohort work** — points to `held_out_traces.jsonl` with the
  actual failure count (3/89) and the specific rubric criterion (`regex_positive`).
- [x] **Generalizable** — every FDE comparing model versions on a small eval set
  faces this; the choice between bootstrap CI and exact binomial test is a
  recurring decision in LLM evaluation.
- [x] **Resolvable** — 600–1,000 words can cover the null hypothesis, exact
  binomial vs bootstrap for small N, and a concrete worked example on the 3/89
  numbers.
