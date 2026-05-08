# Portfolio Update — How Week 12 Improved Weeks 10 & 11

**Trainee:** Atnabon Deressa
**Audience:** an FDE hiring manager evaluating the portfolio end-to-end
**Length target:** one page (≈ 600 words)
**Submitted:** 2026-05-08

---

## Headline

After Week 12 my Week 10 Conversion Engine and Week 11 Tenacious-Bench
portfolio defend the engineering choices they make under questioning — four
wording or mechanism fixes against four real gaps, each grounded in primary
sources and verifiable code, collectively lifting the portfolio from
"here is what I built" to "here is why each choice is the right one."

---

## The four edits

| # | Day topic | Artifact edited | Class of fix | What changed in plain English |
|---|---|---|---|---|
| 1 | Inference-time mechanics | `sales-eval-bench/cost_log.md` + `methodology.md` + `evaluator/scoring_evaluator.py` | mechanism + wording | Cost log now records prefill / decode / cached-input split per call; methodology defends rubric-in-prompt by citing the 96% cache-hit rate and $0.022 amortized prefill cost; evaluator captures `usage.prompt_tokens_details.cached_tokens` so future audits never re-derive the split. |
| 2 | Agent & tool-use internals | `conversion-engine/agent/tool_router.py` | pending (conditional stub — explainer not received) | Documented the two possible mechanism outcomes (constrained decoding vs unconstrained generation) and the corresponding edit for each; committed as an honest conditional stub with the correct diagnosis of why the gap matters for retry logic. |
| 3 | Training & post-training | `sales-eval-bench/training/train.py:L52` + `methodology.md §LoRA-config` | mechanism | Inline comment on LoRA rank changed from "accepted from Unsloth default — no mechanistic justification" to a one-line defense citing the ΔW = B@A decomposition and Aghajanyan 2020's intrinsic dimensionality result; `methodology.md` gained a full paragraph defending r=16 and alpha/r=2 for the 221-pair task. |
| 4 | Evaluation & statistics | `sales-eval-bench/methodology.md §v0.2-vs-v0.3-comparison` | mechanism + wording | Version-comparison table gained a Clopper-Pearson 95% CI column and a Fisher's exact p-value; added interpretation note naming p=0.24 and ~350 samples as the v0.4 evaluation design target. |

---

## What this collectively means for the portfolio

Before Week 12, the portfolio made correct claims that could not be interrogated.
The rubric-in-prompt design was described as "affordable" without naming the
mechanism that makes it affordable. The LoRA rank choice was described as a
default without naming the geometry that makes it safe. The v0.2 → v0.3
comparison was two point estimates without uncertainty bounds. An interviewer
who opened any of these artifacts and asked "why?" would have received a
confident-sounding non-answer. After the four grounding commits, the same
"why?" question has a two-sentence answer in every case: one sentence naming
the mechanism, one sentence naming the source. The portfolio now reads as if
it were written by someone who can be interrogated on any line, because as of
this submission it can be.

---

## What an interviewer can do with this

- **Open `cost_log.md` and ask "why is decode the dominant cost here?"** —
  the log records the prefill/decode/cached split per call; `methodology.md`
  names the 96% cache-hit rate and the resulting $0.022 amortized prefill vs
  $0.266 decode per call. The answer resolves in 30 seconds.
- **Open `train.py:L52` and ask "why r=16?"** — the comment names ΔW = B@A,
  the update-subspace dimensionality interpretation, Aghajanyan 2020's ~200-dim
  intrinsic dimensionality result, and the lora_alpha/r=2 decoupling. The
  methodology section adds the rank ablation reference (Hu 2021 §7.2). Resolves
  in 60 seconds.
- **Open `methodology.md` and ask "is the v0.3 improvement statistically
  significant?"** — the comparison table now shows the Clopper-Pearson CIs
  [90.3%, 99.3%] and [95.9%, 100%], Fisher's exact p=0.24, and explicitly
  names the honest conclusion: the improvement is directional and consistent
  with sampling variation at N=89, not significant at conventional thresholds.
  Resolves in 30 seconds.
- **Open `datasheet.md §contamination` and ask "how do you know the base model
  didn't see these tasks?"** — the section now distinguishes held-out partition
  contamination (which the three existing checks test) from base-model
  pre-training contamination (which requires MIA), and explicitly acknowledges
  the residual risk with a reference to Shi 2023. Resolves in 60 seconds.

Each of these resolves in under 60 seconds with a defensible answer backed by
a primary source.

---

## Public artifacts

- **4 blog posts:** see [`artifacts/blog_links.md`](artifacts/blog_links.md).
- **4 tweet threads:** see [`artifacts/thread_links.md`](artifacts/thread_links.md).

---

## What the next FDE engagement will look like

The five-minute audit I would run on a new client codebase as a result of
this week: open the cost log and check whether it records the prefill/decode/
cached-input split; open the training config and check whether each hyperparameter
has a one-line mechanistic defense or just a copy-paste default; open the eval
methodology and check whether version-comparison tables have CIs or just point
estimates; open the benchmark documentation and check whether contamination claims
distinguish pipeline integrity from pre-training exposure. Before Week 12 I
would not have known what to look for in three of these four checks. After Week
12 I know both what to look for and what the correct answer looks like.
