# Week 12 Synthesis — Knowledge Gap Formulation for Compounding

**Trainee:** Atnabon Deressa
**Programme:** TRP1 / FDE — Week 12
**Submitted:** 2026-05-08
**Length target:** ≈ 1,500 words

---

## 1. The four gaps I named (asker side)

| Day | Topic | Gap (mechanism, not topic) | Grounding commit |
|---|---|---|---|
| 1 | Inference-time mechanics | Prefill vs decode cost split + prefix-cache invalidation rule: any byte-different token at position i in the system prompt collapses cache-hit rate to 0% silently | [`pair_DAY_1/grounding_commit.md`](pair_DAY_1/grounding_commit.md) |
| 2 | Agent & tool-use internals | Function-calling at the token level: whether the model performs constrained decoding over a tool-name vocabulary or unconstrained generation + post-hoc parse — the two have categorically different failure modes and retry logic | [`pair_DAY_2/grounding_commit.md`](pair_DAY_2/grounding_commit.md) |
| 3 | Training & post-training | LoRA rank as update-subspace dimensionality via the ΔW = B@A decomposition: rank controls the geometry of possible weight updates, not their magnitude, and the distinction determines whether r=16 is defensible for 221 SFT pairs | [`pair_DAY_3/grounding_commit.md`](pair_DAY_3/grounding_commit.md) |
| 4 | Evaluation & statistics | Clopper-Pearson CI + Fisher's exact test on binary pass-rate comparisons at small N: a 3-failure → 0-failure improvement on 89 samples has p=0.24 and overlapping CIs — the directional claim was real but the statistical claim was missing | [`pair_DAY_4/grounding_commit.md`](pair_DAY_4/grounding_commit.md) |

**Day 1 (Efrate's explainer):** The prefill/decode split and prefix-cache invalidation rule closed the gap. I could not explain why my rubric-in-prompt design was defensible on cost; after the explainer I could name the exact condition: the rubric must sit byte-stable at the head of the prompt, and the 96% cache-hit rate makes prefill cost ~$0.022/call vs $0.142 cold — decode dominates at 92%. The grounding commit added the prefill/decode/cached split to every row in `cost_log.md` and added usage instrumentation to `scoring_evaluator.py`.

**Day 2 (Ramlla's explainer — not received):** The grounding commit documents a conditional edit because Ramlla submitted independently before writing my explainer (power outage at her location). I surfaced the right gap — the function-calling mechanism question is load-bearing for my retry logic — but the explainer never landed. The commit is an honest conditional stub, not a fabricated closure.

**Day 3 (Yohannes's explainer):** The B@A decomposition closed the rank question. Rank controls the dimensionality of the update subspace, not the magnitude of updates (magnitude = alpha/r separately). Aghajanyan 2020's ~200-dim intrinsic dimensionality argument made r=16 defensible for 221 pairs. The commit added a mechanistic comment to `train.py:L52` and a defended paragraph to `methodology.md §LoRA-config`.

**Day 4 (Zemzem's explainer):** The Clopper-Pearson + Fisher's exact mechanism closed the significance question. I now understand that a 3/89 vs 0/89 comparison has overlapping 95% CIs and p=0.24 — which is not "v0.3 failed the test" but "N=89 is too small to distinguish the true pass-rates." The commit added the CI column and p-value to the comparison table and named ~350 samples as the v0.4 evaluation target for adequate power.

---

## 2. The four gaps I researched and explained (writer side)

| Day | Partner's question (one line) | Sign-off |
|---|---|---|
| 1 | "What gets invalidated on a prefix-cache miss vs hit, and how does that change per-call cost and latency?" (Efrate) | closed |
| 2 | "Why does my Conversion Engine Draft stage regress to generic email templates despite rich enrichment data in the context?" (Ramlla) | partial (power outage — mechanism received over Slack, formal paragraph pending) |
| 3 | "What is the mechanistic difference between what updating q_proj/v_proj can change versus what updating the FFN layers would change, and why does this predict the regex_negative / regex_positive failure split?" (Yohannes) | closed |
| 4 | "What membership inference tests exist for base model pre-training contamination, what can they prove, and why can't n-gram overlap on held-out partitions answer the question?" (Zemzem) | pending |

**Day 1 (Efrate):** The surprise was how simple the invalidation rule is once stated precisely: byte-for-byte prefix match on the tokenized sequence, provider-side. I had assumed it was fuzzy. The fact that a single prepended timestamp at position 0 collapses hit rate to 0% — auditable via `usage.prompt_tokens_details.cached_tokens` in a 25-line probe — is a footgun that affects every long-prompt agent silently. Closed on first revision.

**Day 2 (Ramlla):** The mechanism I had to internalize was the constraint-satisfaction view of decoding: layered system instructions are not processed sequentially but simultaneously at every decoding step, and the decoder minimizes expected constraint-violation across all of them together, which mathematically produces low-variance template tokens. Layered on top, mid-prompt attention decay (Liu et al. 2023) makes enrichment data placed in the middle computationally invisible at decode time. The surprise: adding a sixth instruction ("be more personalized") makes the problem worse by increasing the constraint count. Partially closed — formal sign-off pending due to Ramlla's outage.

**Day 3 (Yohannes):** The mechanism was the routing/transformation cut. Q and V projections do information routing — deciding which tokens get attended to and what values flow forward. FFN layers do information transformation — composing token sequences via key-value memory (Geva 2021). These are categorically different computational jobs. The surprise was that Yohannes's rubric — `regex_negative` / `regex_positive` — was encoding this distinction without either of us realizing it: `regex_negative` measures routing success (suppression of banned phrases), `regex_positive` measures transformation success (generation of required hedged phrases). Q+V-only LoRA can learn the first but not the second. The failure pattern was mechanistically predicted by the configuration. Closed on first revision.

**Day 4 (Zemzem):** The mechanism was the partition-contamination / pre-training-contamination distinction. N-gram overlap tests a pipeline you control; MIA tests a training corpus you don't have. MIN-K% Prob (Shi 2023) is the most robust available signal: it uses minimum-probability tokens rather than average perplexity, which eliminates the stopword-dominance false-positive problem. The surprise: the "no MIA signal" result cannot prove absence — MIA power decreases for models that generalize well. The only fully conclusive method is temporal: tasks created after the model's training cutoff cannot have been memorized. Sign-off pending as of submission.

---

## 3. The most surprising thing I learned

The most counter-intuitive mechanism the week surfaced was from Day 3: the claim that Yohannes's rubric was already diagnosing the correct mechanistic failure before either of us understood the mechanism it was diagnosing. The `regex_negative` / `regex_positive` split in `held_out_traces.jsonl` had been producing a consistent pattern for weeks — all 3 failing tasks passing `regex_negative` and failing `regex_positive` — and both of us were reading it as noise. It was not noise. The rubric was, accidentally, a precision instrument for the routing/transformation distinction in the LoRA target-module choice. `regex_negative` tests whether the model suppressed a class of tokens it was instructed to suppress — a routing task. `regex_positive` tests whether the model generated a specific required phrase at the right position — a transformation task. Q+V LoRA can learn the first because it updates which values flow through the attention mechanism. It cannot learn the second because it never touches the FFN key-value memory where phrase composition happens.

What makes this surprising as a claim two years from now: it means the failure pattern in your eval rubric is diagnostic of the LoRA configuration problem, not independent of it. Before the explainer, I would have tried to fix the failures by adding more training data or increasing rank. After the explainer, the only correct fix is adding `gate_proj`, `up_proj`, and `down_proj` to `LORA_TARGETS`. The rubric was telling me this the entire time. I needed the mechanism to read it.

---

## 4. Trajectory across the week

Day 1's question was the right kind of question — it named a mechanism (prefill/decode split) rather than a topic area — but it took some sharpening on the morning call to focus on "through what mechanism does prefix caching change the prefill side without changing the decode side?" rather than the broader cost question. Day 2's question was strong: "constrained decoding vs unconstrained generation + post-hoc parse" is a precise mechanistic claim with a direct consequence for retry logic. Day 3's question was the best of the week: it named the B@A decomposition, quoted the exact LoraConfig block from `train.py:L52`, and named the specific failure evidence (3 residual SOC failures on `regex_positive`) that the question was addressing. Day 4 had a notable miss: the first-draft question (LoRA rank per module) was training mechanics, not evaluation and statistics — Zemzem corrected this immediately. The corrected question was strong and correctly grounded. The trajectory is not monotonically improving: Day 3 was the peak, and Day 4 showed a topic-fit error that Day 3 did not. However, the speed of correction (one Slack exchange, no delay) and the quality of the corrected question suggest the underlying skill is present — the error was category matching, not question quality.

The grounding commits show a cleaner trajectory: Day 1 was both wording and mechanism (two separate artifacts changed); Day 3 was mechanism only (a genuine understanding change, not a reword); Day 4 was both, with the most concrete power analysis number (350 samples for 80% power) of any commit in the week.

---

## 5. Compounding into Weeks 10 and 11

The four grounding commits are not four independent edits. They collectively shift the portfolio from one that asserts engineering choices toward one that defends them under interrogation. Before Week 12, `methodology.md` defended the rubric-in-prompt design with "the per-call cost is small enough to absorb on our $10 budget envelope" — a hand-wave. After Day 1's commit, it defends the same choice by naming the 96% cache-hit rate, the $0.022 amortized prefill cost, and the CI regression test that prevents silent invalidation. Before Week 12, `train.py:L52` said "accepted from Unsloth default — no mechanistic justification." After Day 3's commit, it says "ΔW = B@A; rank = update subspace dimensionality, not magnitude; r=16 safe for 221 pairs given ~200-dim LLM intrinsic dimensionality (Aghajanyan 2020)." Before Week 12, the v0.2 vs v0.3 comparison table was two point estimates with no uncertainty bounds. After Day 4's commit, it has CIs, a Fisher's exact p-value, and a power analysis.

The pattern across all four commits is the same: every change moves a claim from "I made this choice" to "I made this choice because of this specific mechanism, which you can verify here." A reviewer reading the portfolio end-to-end now encounters the same epistemic standard in every defended decision: named mechanism, named source, auditable probe. That coherence is what "compounding" names. The four edits are not additive patches — they are a single upgrade to the evidential standard the portfolio holds itself to.

---

## 6. Canonical list contribution

See [`canonical_list.md`](canonical_list.md) for the full annotated list. The single highest-signal item I am contributing to the cohort canon is the **MIN-K% Prob pattern** from Shi et al. 2023 — not because membership inference is exotic, but because the distinction it makes is one almost every eval builder misses: your held-out partition checks verify the pipeline you control; they say nothing about whether the base model saw your tasks during pre-training. The MIN-K% Prob probe is a 10-line Python function any FDE can run against their eval set and their base model to produce a probabilistic membership signal before making a benchmark validity claim. The pattern is narrow enough to be immediately useful and general enough to apply to any benchmark with any base model.

---

## 7. What I would do differently

Two things. First: check the cohort topic before drafting the Day 4 question. I drafted a training mechanics question (LoRA rank per module) without verifying it fit "evaluation and statistics." Zemzem caught it in one exchange, the correction was quick, but the initial miss was avoidable. A 30-second check against the daily topic announcement would have prevented it.

Second: Day 2 ran without an explainer because Ramlla's location had a power outage and she submitted independently. I documented the conditional commit honestly, but I never had a backup plan for getting an explainer from a different source (a paper, a cohort member, self-research). In a real FDE engagement, if a collaborator goes dark, you do not leave the knowledge gap open — you close it yourself and document what you used. The conditional stub is the honest record; it is not the right outcome.
