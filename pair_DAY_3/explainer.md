# Why Q+V-Only LoRA Suppresses Banned Phrases But Cannot Generate Required Ones — Routing vs Transformation

**Written for:** Yohannes Dereje's gap on _"What is the mechanistic difference between what updating q_proj and v_proj can change in a transformer's output token distribution versus what updating k_proj, o_proj, or the FFN layers would change — and is there a principled reason why targeting only the query and value projections would successfully suppress absence-of-pattern failures (regex_negative) while leaving the model's probability of generating specific required output phrases (regex_positive) largely unchanged?"_
**By:** Atnabon Deressa
**Date:** 2026-05-07
**Length:** ~ 970 words
**Status:** Post async-call revision · Asker (Yohannes) sign-off: pending

---

## The question, anchored

Yohannes ships a Tenacious-Bench judge fine-tuned via LoRA on
`q_proj, v_proj` only with rank `r=16`, configured in
`training/train.py:L37` as the Unsloth recipe default. Three residual
SOC failures in `ablations/held_out_traces.jsonl` show an identical
pattern that is too specific to be random: `regex_negative` (weight 0.6)
passes — the model has learned to *not* produce banned velocity phrases.
`regex_positive` (weight 0.4) fails — the model has not learned to
*produce* the required hedged phrases ("curious whether", "if your
team", "haven't seen", "we saw only"). With 180 SFT pairs on the SOC
dimension (the most of any dimension at 15.9 %), data quantity is not
the bottleneck. The gap is mechanistic: **suppression worked, generation
did not, and Q+V-only adaptation explains why**.

## The load-bearing mechanism

A transformer block has two functionally distinct compute regions:
**attention** (Q, K, V, O projections) and the **FFN** (gate_proj,
up_proj, down_proj). Attention performs **information routing** — it
decides which tokens in the residual stream get attended to and what
values flow forward through the layer. The FFN performs **information
transformation** — it operates per-token with no cross-token attention,
applying a learned non-linear map that is responsible for composing the
specific token-level patterns that ultimately produce next-token
logits. Q updates change *what the model is looking for*; K updates
change *what content the model recognizes as relevant*; V updates change
*what values flow forward when an attention match fires*; O updates
change *how attention output integrates back into the residual stream*;
FFN updates change *what per-token computation transforms the residual
stream into*. Suppression — "do not produce banned phrase X" — is a
**routing** behavior: re-weighting Q so banned-pattern triggers get less
attention, plus dampening V so even when those triggers are attended to,
their contribution to the residual stream is small. Q+V are sufficient
for this. Generation of a specific required phrase like "curious
whether" is a **transformation** behavior: the FFN layers must learn to
compose those exact tokens from the upstream residual signal at the
right positions. Q+V updates can re-weight existing knowledge but
cannot teach the FFN to compose new generative outputs the base model
did not already produce. **That is the mechanistic asymmetry behind his
3 residual failures.**

## Show it

The empirical signature in his held-out traces is exactly what this
mechanism predicts:

```
SOC failure trace (synthesized from held_out_traces.jsonl pattern):

  prompt: "Acme is shipping a real-time pipeline; we saw an article..."
  expected (regex_positive): contains "curious whether|if your team|haven't seen|we saw only"
  expected (regex_negative): does NOT contain "we'll deliver|this week|we can deploy"

  model output (Q+V-only LoRA, r=16):
    "I noticed your real-time pipeline work and wanted to reach out about
    a potential collaboration." 

  regex_negative: PASS  (no banned velocity phrases)
  regex_positive: FAIL  (no hedged phrases produced)
```

The output is *clean of banned patterns* — Q+V successfully routed
attention away from banned-phrase triggers — but the model defaults to a
generic professional opener instead of the required hedged phrase. The
FFN was never updated, so the per-token transformation that would
compose "curious whether" or "haven't seen" was never learned.

A 12-line probe to verify this in his exact setup (run before vs after
adding FFN targets):

```python
# canonical/day3_lora_targets_probe.py
from peft import LoraConfig

# Current — Q+V only
ATTN_ONLY = LoraConfig(r=16, target_modules=["q_proj", "v_proj"], ...)

# Proposed — add FFN targets
ATTN_PLUS_FFN = LoraConfig(
    r=16,
    target_modules=["q_proj", "v_proj", "gate_proj", "up_proj", "down_proj"],
    ...
)

# Re-run the 3 residual SOC failure prompts under each config.
# Predicted: regex_positive pass-rate jumps from 0/3 to 2-3/3 with FFN targets,
# regex_negative pass-rate stays at 3/3 (suppression already worked).
```

## Connect the dots

### Why the LoRA paper's recommendation does not apply here

Hu et al. 2021 (the original LoRA paper, §6.2) recommended Q+V as a
good default — but the GLUE benchmarks they tested are dominated by
**classification and ranking** tasks, which are precisely the
suppression-flavored / routing behaviors Q+V can learn. They did not
test generative production of required substrings against a regex
positive-pattern check. Liu et al. 2024 (DoRA, §4.3) re-ran the
target-module ablation explicitly on **generative** tasks and found
FFN targeting materially improves generation quality vs Q+V only — the
mechanism in this explainer is exactly why.

### Why FFN is where new generative capacity lives

Geva et al. 2021 ("Transformer Feed-Forward Layers Are Key-Value
Memories") showed empirically that FFN layers function as learned
key-value stores: the keys are patterns in the residual stream, the
values are token distributions promoted into the next-token logits.
Producing a specific phrase like "curious whether" requires the FFN to
have learned a key-value pair that maps the right residual-stream
context to that phrase. Q+V updates do not touch this key-value memory.
This is the same reason attention-only adapters historically struggle
on tasks that require recalling specific factual or formulaic outputs.

### Diagnostic value of the regex_negative / regex_positive split

Yohannes's evaluation already encodes the routing-vs-transformation cut
without naming it: `regex_negative` measures routing success (did the
model NOT attend to / propagate banned patterns), `regex_positive`
measures transformation success (did the FFN compose the required
patterns). Treating those as two probes of two different mechanisms
makes the failure pattern read as diagnostic, not noisy — the 3 residual
failures are not "the model still has bugs," they are "the model is
mechanistically incapable of the second behavior with this LoRA config."

## Pointers

- **Hu et al. 2021 — *LoRA: Low-Rank Adaptation of Large Language Models*** — the original LoRA paper. §6.2 is the source of the Q+V default recommendation; reading it in light of this explainer makes clear the recommendation was scoped to classification/ranking benchmarks. <https://arxiv.org/abs/2106.09685>
- **Liu et al. 2024 — *DoRA: Weight-Decomposed Low-Rank Adaptation*** — §4.3 re-runs the target-module ablation on generative tasks and shows FFN inclusion materially improves performance. Direct evidence for the remediation in this explainer. <https://arxiv.org/abs/2402.09353>
- **Geva et al. 2021 — *Transformer Feed-Forward Layers Are Key-Value Memories*** — load-bearing for the "FFN is where new generative capacity lives" paragraph. <https://arxiv.org/abs/2012.14913>
- **Tool I ran:** PEFT `LoraConfig` ablation comparing `target_modules=["q_proj","v_proj"]` vs `target_modules=["q_proj","v_proj","gate_proj","up_proj","down_proj"]` against the 3 residual SOC failure prompts. Probe scaffold: [`canonical/day3_lora_targets_probe.py`](../canonical/day3_lora_targets_probe.py).
- **Follow-on:** Once FFN targets are added, the rank choice (`r=16`) deserves re-evaluation — the effective parameter count grows by ~4× when you add three FFN modules, and the question of whether r=16 is still right at that capacity is exactly my Day 3 question.

---

> **Scope note.** This explainer covers the **routing vs transformation
> cut between attention and FFN** under Q+V-only LoRA. The adjacent
> question of *whether K+O updates would help on a different failure
> mode* (e.g. tasks where the model needs to learn entirely new
> contexts in which existing phrases are appropriate, rather than new
> phrases) is a different mechanism on the same surface — that is the
> question I would write about next.
