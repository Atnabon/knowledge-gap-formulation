# Tweet thread — Day 2

**Platform:** X (mirror to LinkedIn)
**Length:** 6 tweets
**Standalone test:** A reader who never clicks through still leaves with the mechanism (mode collapse under stacked constraints + lost-in-the-middle attention decay; fix is prompt geometry, not adding instructions).
**Status:** Post async-call draft

---

**1/** Most engineers shipping LLM agents have hit this: you stuff enrichment data, safety rules, formatting constraints, and output instructions into one prompt — and the model returns a generic template. Adding "be more personalized" makes it *worse*. Here is why. 🧵

**2/** The mechanism is **mode collapse under competing constraints**. Each instruction in your prompt zeroes out probability mass on tokens that violate it. When many constraints stack, the only tokens with high *joint* probability across all of them are the bland, low-variance, template-shaped ones. Personalized tokens are high-variance by definition — and most personalized variants violate at least one constraint.

**3/** Stacked on top: **lost-in-the-middle attention decay** (Liu et al. 2023). Long prompts under-attend the middle. If your enrichment data is buried between safety rules and formatting rules, it is computationally invisible at decode time even though it is "in the context."

**4/** Probe it on your own setup — same model, same temperature, only the *position* of the enrichment block changes:

```
buried (mid-prompt): 2 /8 unique openings  ("Hi Sarah, I noticed..." × 5)
late (end-of-prompt): 7 /8 unique openings (each leads with a different concrete signal)
```

The model is not "ignoring" the data in the buried case; attention-score geometry makes it invisible.

**5/** Three single-pass fixes before going multi-step:
- Move enrichment data to the END of the prompt, right before "Write:"
- Move safety constraints to a post-hoc validator, not the generation prompt
- Add 2–3 few-shot examples of strongly personalized outputs

Each one shrinks the constraint stack. Each one moves personalization into a high-attention position.

**6/** Going multi-step (plan → reason → write) helps because each step has fewer constraints and personalization signals land at high-attention positions by construction. But you pay: latency ~ 2×, error compounding, harder coherence. Try the geometry fixes first. Full write-up: <link to blog post>
