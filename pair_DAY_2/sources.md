# Sources — Day 2

**Day:** 2
**Topic:** Agent & tool-use internals (paired) / Long-context decoding mechanics (Ramlla's gap)
**Explainer author:** Atnabon Deressa
**Question this serves:** Ramlla's gap — "How does instruction overload during one-shot decoding affect an LLM's ability to preserve semantic richness and personalization from contextual signals in my Conversion Engine Draft stage?"

---

## Canonical sources (minimum two; original papers > authoritative documentation > second-hand summaries)

### 1. Liu et al. — *Lost in the Middle: How Language Models Use Long Contexts*

- **Authors:** Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, Percy Liang
- **Year / venue:** 2023, arXiv preprint (subsequently TACL 2024)
- **Link:** <https://arxiv.org/abs/2307.03172>
- **What I drew from it:** Section 3 (key-value retrieval task) and
  Section 4 (multi-document QA) — the empirical demonstration that
  attention to mid-prompt tokens is systematically lower than attention
  to start-of-prompt and end-of-prompt tokens, and that this degrades
  task performance proportionally to how deep the relevant token is
  buried. This is the load-bearing reference for the explainer's
  "lost-in-the-middle attention decay" paragraph and for the diversity
  probe interpretation (why end-positioned enrichment recovers 7/8
  unique openings vs 2/8 for mid-positioned).
- **Inspected directly?** Yes.

### 2. Ouyang et al. — *Training language models to follow instructions with human feedback*

- **Authors:** Long Ouyang, Jeff Wu, Xu Jiang, Diogo Almeida, Carroll L. Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, John Schulman, Jacob Hilton, Fraser Kelton, Luke Miller, Maddie Simens, Amanda Askell, Peter Welinder, Paul Christiano, Jan Leike, Ryan Lowe
- **Year / venue:** 2022, NeurIPS 2022 (InstructGPT paper)
- **Link:** <https://arxiv.org/abs/2203.02155>
- **What I drew from it:** Section 4.2 — the documented "alignment tax"
  showing that RLHF-trained models acquire strong priors toward safe,
  professional, low-variance outputs because that is what got rewarded
  in human preference training. This is the load-bearing reference for
  the explainer's claim that adding a sixth instruction telling the
  model to "be more personalized" makes mode collapse *worse*, because
  the RLHF prior is already biased toward the safe-template subspace
  before any user instruction is added.
- **Inspected directly?** Yes.

## Tool / pattern I ran hands-on

**Name:** OpenAI-compatible chat-completion API against `anthropic/claude-haiku-4.5` via OpenRouter
**Version:** `openai==1.x` Python SDK, OpenRouter passthrough
**What I did:** Ran an 8-call diversity probe with two prompt orderings — `PROMPT_BURIED` (enrichment data positioned mid-prompt between safety and format rules) and `PROMPT_LATE` (enrichment data positioned at the end, just before the generation point). Measured unique opening 5-grams across the 8 generations per condition. The buried condition produced 2/8 unique openings (mode collapse to "Hi Sarah, I noticed..."). The end-positioned condition produced 7/8 unique openings, each leading with a different concrete signal from the enrichment block.
**Where the artifact lives:** [`canonical/day2_mode_collapse_probe.py`](../canonical/day2_mode_collapse_probe.py)

## Attribution check

- [x] Every cited paper / tool / source above appears in the explainer's `Pointers` section with the same link.
- [x] No fabricated references.
- [x] No second-hand summary used as a load-bearing citation.
