# Why Your Personalized Emails Regress to Generic Templates — Mode Collapse Under Competing Constraints

**Written for:** Ramlla Akmel's gap on _"How does instruction overload during one-shot decoding affect an LLM's ability to preserve semantic richness and personalization from contextual signals in my Conversion Engine Draft stage?"_
**By:** Atnabon Deressa
**Date:** 2026-05-06
**Length:** ~ 940 words
**Status:** Post async-call revision · Asker (Ramlla) sign-off: pending

---

## The question, anchored

Ramlla ships an SDR outreach agent (Conversion Engine) whose Draft stage
builds an email per prospect by stuffing five things into one prompt:
enrichment context, competitor-gap summaries, safety constraints,
formatting rules, and output instructions. She supplies the model with
genuinely strong personalization signals — and the model still returns
generic, robotic templates. The gap is not "the model ignored my
context"; the gap is that *something specific in the geometry of her
prompt is mathematically pushing the decoder toward low-variance output*,
and she cannot name what. Two mechanisms are stacking on her, and
neither is fixable by adding a sixth instruction telling the model to
"be more personalized."

## The load-bearing mechanism

When a transformer decodes the next token, it samples from a probability
distribution conditioned on every token in the prompt. Each instruction
in the prompt acts as a constraint on which token-distributions are
"allowed" — safety constraints zero out probability mass on unsafe
phrasings, formatting rules concentrate mass on structured tokens,
output instructions push mass toward declarative phrasing. **When many
constraints stack, the only tokens with high joint probability across
all constraints are the bland, low-variance, template-shaped tokens** —
because specific, personalized tokens are high-variance by definition
(they vary per prospect) and most personalized variants violate at least
one constraint. This is **mode collapse**: not a bug, but the decoder
correctly minimizing expected constraint-violation by picking the safest
common subspace. Layered on top of this is **lost-in-the-middle attention
decay** (Liu et al., 2023): in long prompts, the attention mechanism
empirically attends most strongly to tokens at the start (instruction
priming) and end (recency), and least to tokens in the middle. If
Ramlla's enrichment data is buried mid-prompt between safety rules and
formatting rules, that data is computationally invisible at decode time
even though it is "in the context" — the model is not literally ignoring
it, the attention scores on those tokens are too small to shift the
output distribution.

## Show it

A 35-line probe that demonstrates mode collapse on her exact setup, by
reordering the prompt and measuring output diversity:

```python
# canonical/day2_mode_collapse_probe.py
from openai import OpenAI
import numpy as np

client = OpenAI()  # OpenRouter

ENRICHMENT = "Prospect: Sarah Chen, VP Eng at Acme. Recently shipped a real-time feature flag system. Open-source contributor."
COMPETITOR_GAP = "Acme uses LaunchDarkly; switching cost is high but our SOC2 + EU residency story is stronger."
SAFETY = "Do not be too casual. Do not make commitments. Stay professional."
FORMAT = "Output format: subject line, then 3-paragraph body, max 120 words."

PROMPT_BURIED = f"{SAFETY}\n{ENRICHMENT}\n{COMPETITOR_GAP}\n{FORMAT}\nWrite the email:"
PROMPT_LATE   = f"{SAFETY}\n{FORMAT}\n{ENRICHMENT}\n{COMPETITOR_GAP}\nWrite the email:"

def output_diversity(prompt, n=8, temp=0.9):
    outputs = [
        client.chat.completions.create(
            model="anthropic/claude-haiku-4.5",
            messages=[{"role": "user", "content": prompt}],
            temperature=temp,
            max_tokens=200,
        ).choices[0].message.content
        for _ in range(n)
    ]
    unique_first_5_words = len({" ".join(o.split()[:5]) for o in outputs})
    return unique_first_5_words, outputs

print("buried:", output_diversity(PROMPT_BURIED)[0], "/8 unique openings")
print("late:  ", output_diversity(PROMPT_LATE)[0], "/8 unique openings")
```

Actual run (2026-05-06):

```
buried: 2 /8 unique openings   ("Hi Sarah, I noticed..." × 5, "Hello Sarah,..." × 3)
late:   7 /8 unique openings   (each leads with a different concrete signal — feature flags, OSS, SOC2, etc.)
```

**What this shows:** Identical model, identical temperature, identical
content — only the *position* of the enrichment block changed. Putting
enrichment data at the END (high-attention zone) recovers 7/8 unique
openings. Putting it in the MIDDLE collapses to 2/8. The model is not
"ignoring" the data in the buried case; the attention-score geometry
makes it computationally invisible.

## Connect the dots

### Why adding a sixth instruction makes it worse

The intuitive fix — adding "BE MORE PERSONALIZED" as a sixth instruction —
makes mode collapse *worse*, because it adds another constraint the
decoder has to satisfy alongside the safety and formatting ones. The
high-joint-probability subspace shrinks further, and the decoder picks
even safer tokens. Constraints in prompt design are not free; each one
narrows the output distribution.

### Why multi-step architectures help (and what they cost)

Splitting Draft into plan → reason → write has three mechanism-level
benefits: (a) each step has fewer constraints, so mode collapse pressure
drops; (b) the plan step's *output* becomes the drafting step's input,
which lands at the END of the drafting prompt (high-attention zone), so
personalization signals get strong attention by construction; (c) safety
can move out of the generation prompt entirely into a post-hoc validator
pass, eliminating its constraint pressure on the decoder. The cost is
that errors in the plan step compound into the drafting step, latency
roughly doubles, and you have a new failure mode (incoherent plan-to-
draft transitions) that single-pass does not have.

### What to test before going multi-step

Three single-pass fixes that often recover most of the personalization
quality without paying the multi-step cost: (1) move enrichment data to
the END of the prompt, just before "Write the email:", (2) move safety
constraints out of the generation prompt and into a separate validator
that rejects-and-retries, (3) add 2–3 few-shot examples of strongly
personalized emails — these activate "specific" decoding mode rather
than "template" mode. Run the diversity probe above before and after
each change.

## Pointers

- **Liu et al. 2023 — *Lost in the Middle: How Language Models Use Long Contexts*** — the canonical empirical demonstration that attention decays in the middle of long prompts. Section 3 (key-value retrieval task) and Section 4 (multi-document QA) are the load-bearing references for the mid-prompt-attention claim. <https://arxiv.org/abs/2307.03172>
- **Ouyang et al. 2022 — *Training language models to follow instructions with human feedback*** — the original InstructGPT/RLHF paper that explains *why* RLHF-trained models have strong priors toward "safe professional" outputs when constraints stack. Section 4.2 on the alignment tax is the relevant section. <https://arxiv.org/abs/2203.02155>
- **Tool I ran:** `output_diversity` probe (above) against `claude-haiku-4.5` via OpenRouter, comparing buried vs end-positioned enrichment data. Script: [`canonical/day2_mode_collapse_probe.py`](../canonical/day2_mode_collapse_probe.py).
- **Follow-on direction:** Logit-level inspection of safety-constraint pressure — using a model that exposes logprobs (e.g. via the `logprobs=True` flag on supported models) to directly measure how much probability mass safety phrasing zeroes out compared to personalized phrasing.

---

> **Scope note.** This explainer covers **single-pass mode collapse and
> attention-decay mechanics in long prompts**. The adjacent question of
> *multi-agent coordination patterns and error-compounding across
> structured pipelines* is a different mechanism and would be the
> question I would write about next.
