# Canonical List — Atnabon Deressa's Week 12 contribution

**Trainee:** Atnabon Deressa
**Programme:** TRP1 / FDE — Week 12
**Audience:** other Forward-Deployed Engineers in the cohort and the wider community

> Annotated. Each entry says what the source actually claims, why it is
> load-bearing for FDE work, and which Week 10/11 artifact in my own
> portfolio it grounded. Items added across the week as gaps close.

---

## Papers (primary literature)

### DeepSeek-AI — *DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model* (2024)

- **Why it earns the canon slot:** Section 4 is the canonical public
  reference for the server-side context-cache architecture that became
  the industry pattern. Names the KV-state reuse mechanism precisely and
  is the load-bearing source for "what state is reused on a hit, what
  is recomputed on a miss".
- **Where I used it:** [Day 1 explainer](pair_DAY_1/explainer.md) and the
  [Day 1 grounding commit](pair_DAY_1/grounding_commit.md) on
  `sales-eval-bench/cost_log.md`.
- **Link:** <https://arxiv.org/abs/2405.04434>

### Anthropic — *Prompt caching* developer documentation (2024–2026)

- **Why it earns the canon slot:** the most explicit public description
  of the byte-for-byte tokenized-prefix invalidation rule, the discounted-
  rate pricing structure, and the cache TTL. Resolves the "narrow my
  prompt edit to the bottom" footgun that almost every long-prompt
  agent hits silently.
- **Where I used it:** [Day 1 explainer](pair_DAY_1/explainer.md).
- **Link:** <https://docs.claude.com/en/docs/build-with-claude/prompt-caching>

### Liu et al. (2023) — *Lost in the Middle: How Language Models Use Long Contexts*

- **Why it earns the canon slot:** Names and quantifies the U-shaped
  attention curve over long contexts — models attend strongly to
  beginning and end, weakly to the middle — with the specific result that
  mid-prompt information is computationally suppressed at decode time
  even when it appears in the context. The load-bearing source for
  diagnosing why enrichment data placed in the middle of a prompt
  produces generic outputs.
- **Where I used it:** [Day 2 explainer](pair_DAY_2/explainer.md) on mode
  collapse in the Conversion Engine Draft stage.
- **Link:** <https://arxiv.org/abs/2307.03172>

### Hu et al. (2021) — *LoRA: Low-Rank Adaptation of Large Language Models*

- **Why it earns the canon slot:** §7.2 contains the rank ablation that
  shows r=4–8 is sufficient across a range of NLP tasks with diminishing
  returns at r=32+; §6.2 identifies which target modules matter for which
  task types. The load-bearing source for rank choice and for understanding
  why Q+V-only LoRA is inappropriate for generative phrase-composition tasks.
- **Where I used it:** [Day 3 explainer](pair_DAY_3/explainer.md) and the
  [Day 3 grounding commit](pair_DAY_3/grounding_commit.md) on
  `training/train.py`.
- **Link:** <https://arxiv.org/abs/2106.09685>

### Shi et al. (2023) — *Detecting Pretraining Data from Large Language Models* (MIN-K% Prob)

- **Why it earns the canon slot:** Introduces MIN-K% Prob — the most
  robust available method for base-model pre-training membership inference
  without access to the training corpus. Uses minimum-probability tokens
  rather than average perplexity, which eliminates the stopword-dominance
  false-positive problem. The load-bearing source for the distinction between
  held-out-partition contamination checks and base-model pre-training
  contamination.
- **Where I used it:** [Day 4 explainer](pair_DAY_4/explainer.md) on
  membership inference for benchmark contamination.
- **Link:** <https://arxiv.org/abs/2310.16789>

---

## Engineering tools / libraries (battle-tested in this week)

### Provider `usage` object inspection for prefill / decode / cached-input attribution

- **Why it earns the canon slot:** every OpenAI-compatible chat-completion
  endpoint exposes per-call token counts in `resp.usage`; pulling
  `prompt_tokens_details.cached_tokens` is the single highest-signal
  cost-attribution probe an FDE can run against a long-prompt system.
- **Pattern:** see [`pair_DAY_1/explainer.md`](pair_DAY_1/explainer.md) for
  the 25-line probe; ~ $0.001 per run.

### `scipy.stats` Clopper-Pearson CI + `binom_test` for binary eval comparison

- **Why it earns the canon slot:** every LLM benchmark comparison at small N
  (< 200 samples) needs an exact binomial CI, not a t-interval. `scipy.stats`
  provides both the exact Clopper-Pearson via `beta.ppf` and Fisher's exact via
  `binom_test`. The 10-line probe in `canonical/day4_binomial_ci_probe.py` is
  runnable in any Python environment with `scipy` installed and produces the CI
  and p-value needed for a defensible methodology comparison table.
- **Pattern:** see [`pair_DAY_4/grounding_commit.md`](pair_DAY_4/grounding_commit.md)
  for the probe and the methodology diff.

---

## Engineering patterns (production-shaped)

### Per-call cost decomposition: `(uncached_in × $/in) + (cached_in × $/cached_in) + (out × $/out)`

- **What:** every cost-log row for a long-prompt agent should record the
  uncached-input / cached-input / output split and the resulting prefill /
  decode dollar split, not a single dollar amount.
- **Why it earns the canon slot:** without it, an FDE cannot tell whether
  a design decision (rubric-in-prompt, long system prompt, structured
  output) is defensible on cost. With it, the dependency on cache-hit
  rate is auditable from day one.
- **Reference implementation:** [`pair_DAY_1/grounding_commit.md`](pair_DAY_1/grounding_commit.md).

### LoRA target-module triage: route-vs-transform cuts tells you which projections to target

- **What:** before choosing LoRA target modules, classify the behavior you are
  teaching as *routing* (suppressing or amplifying attention to tokens —
  attention Q/V/K/O) or *transformation* (composing new token sequences from
  key-value memory — FFN gate/up/down). Q+V-only is appropriate for routing
  tasks; FFN modules are required for generative phrase-composition tasks.
- **Why it earns the canon slot:** this triage prevents the Q+V-only default
  from silently failing on generative rubric criteria while passing suppression
  criteria, which is the exact failure mode visible in the `regex_positive`
  vs `regex_negative` split in `held_out_traces.jsonl`.
- **Reference implementation:** [`pair_DAY_3/grounding_commit.md`](pair_DAY_3/grounding_commit.md).

### Binary eval table with Clopper-Pearson CI + Fisher's exact p-value

- **What:** any version-comparison table in a benchmark methodology section
  that reports pass-rates on binary outcomes must include the exact binomial
  95% CI and a Fisher's exact p-value for the comparison. Bare point estimates
  without CIs are not interpretable at small N.
- **Why it earns the canon slot:** the 3/89 vs 0/89 difference in
  `held_out_traces.jsonl` looks like a clear improvement as a point estimate
  but has overlapping CIs and p=0.24 — which is the honest result, and it
  changes the action (design v0.4 for ~350 samples rather than claiming
  statistical significance).
- **Reference implementation:** [`pair_DAY_4/grounding_commit.md`](pair_DAY_4/grounding_commit.md).

---

## How to use this list

If you are an FDE who shipped a system in Weeks 10 or 11 and wrote a paragraph
you cannot fully defend, this list is a ranked surface of the canonical sources
that closed analogous gaps for me. The entries are deliberately narrow — each
one says **what the source proves**, not "interesting paper on X". The
narrower the claim, the more useful the citation.
