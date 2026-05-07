# Question — Day 3

**Topic:** Training & post-training
**Subtopic:** LoRA rank vs adapter expressivity
**Asker:** Atnabon Deressa
**Partner (explainer):** Yohannes Dereje
**Date:** 2026-05-07
**Status:** Final (post async-call)

---

## My sharpened question

> In [`sales-eval-bench/training/train.py:L52`](../../sales-eval-bench/training/train.py),
> I configured LoRA with `r=16, lora_alpha=32` to fine-tune my Tenacious-Bench
> judge on 221 SFT preference pairs, accepted as the Unsloth recipe default
> with no mechanistic justification. What does increasing rank from r=8 → r=16
> → r=32 actually change in the adapter's update space — specifically, does
> rank control the **dimensionality of the subspace** the adapter can move
> the base weights through, the **magnitude** of those moves, or both — and
> is there a principled reason r=16 was right for a 221-pair preference task
> versus being over- or under-parameterized?

## Why this is the gap I picked (asker's triage)

I read [`training/train.py`](../../sales-eval-bench/training/train.py) and
[`methodology.md`](../../sales-eval-bench/methodology.md) §LoRA-config as
a hostile reviewer this morning and surfaced four candidate gaps. (1)
"Why Unsloth vs PEFT directly?" — discarded; tooling question I can already
defend. (2) "Why `lora_alpha=32`?" — kept as a candidate but it is paired
with rank (the effective scaling is `alpha/r`), so it folds into the rank
question. (3) "Why 221 SFT pairs and not more?" — discarded; data-quantity
is empirical, not mechanistic. (4) **"Why `r=16` and not `r=8` or `r=32`?"** —
this is the one. The choice is load-bearing: under-rank means the adapter
cannot represent the behavior the SFT pairs are teaching; over-rank means
I am training noise into the residual stream and inflating both adapter
size and inference latency. I copied `r=16` from the Unsloth recipe with
no mechanistic defense, and I cannot tell whether v0.2's expansion to ~600
preference pairs warrants raising rank, keeping it, or lowering it.

## Connection to a specific Week 10 or 11 artifact

**Artifact:** [`sales-eval-bench/training/train.py:L52`](../../sales-eval-bench/training/train.py)
**Current claim/choice in that artifact:**

> ```python
> # train.py:L52 — LoRA config (current)
> peft_config = LoraConfig(
>     r=16,                # accepted from Unsloth default — no mechanistic justification
>     lora_alpha=32,       # effective scaling alpha/r = 2 — also unjustified
>     target_modules=["q_proj", "v_proj"],
>     lora_dropout=0.05,
>     bias="none",
>     task_type="CAUSAL_LM",
> )
> ```

**What closing this gap will let me change:**

After Yohannes's explainer lands I will (a) replace the inline `# accepted
from Unsloth default` comment with a one-line mechanistic defense citing
the SVD-decomposition view of LoRA and the rank-vs-task-complexity scaling
argument, (b) add a paragraph to `methodology.md §LoRA-config` defending
the `r=16` and `alpha/r=2` choices on the 221-pair task, and (c) decide
whether to bump rank to r=32 for the v0.2 expansion to ~600 pairs or keep
r=16 with broader target modules (which Yohannes's question is exploring).

## Four-property self-check

- [x] **Diagnostic** — names a specific mechanism (rank as the dimensionality of the adapter's update subspace via the `B @ A` decomposition), not "what is LoRA?" in general.
- [x] **Grounded in cohort work** — names `train.py:L52`, quotes the actual `LoraConfig` block, and ties to the methodology section that depends on it.
- [x] **Generalizable** — every FDE training a LoRA adapter faces the rank choice; the SVD-decomposition view applies to any LoRA on any backbone.
- [x] **Resolvable** — 600–1,000 words can cover the `B@A` low-rank decomposition, the SVD intuition for what rank `r` represents, and the rank-vs-task-complexity scaling argument with a concrete probe.
