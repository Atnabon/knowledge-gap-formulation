# Sources — Day 4

**Day:** 4
**Topic:** Evaluation & statistics — benchmark contamination and membership inference
**Explainer author:** Atnabon Deressa
**Question this serves:** Zemzem Hibet's gap on what membership inference tests exist for base model pre-training contamination and why n-gram overlap on held-out partitions is a fundamentally different problem.

---

## Canonical sources

### 1. Detecting Pretraining Data from Large Language Models (MIN-K% Prob)

- **Authors:** Weijia Shi, Anirudh Ajith, Mengzhou Xia, Yangsibo Huang, Daogao Liu, Terra Blevins, Danqi Chen, Luke Zettlemoyer
- **Year / venue:** 2023 — arXiv:2310.16789 / ICLR 2024
- **Link:** https://arxiv.org/abs/2310.16789
- **What I drew from it:** The MIN-K% Prob method (Section 3) — using the average log-probability of the k% lowest-probability tokens as a membership signal, and why it outperforms average perplexity by being less sensitive to high-frequency stopwords dominating the signal.
- **Inspected directly?** Yes

### 2. Extracting Training Data from Large Language Models

- **Authors:** Nicholas Carlini, Florian Tramèr, Eric Wallace, Matthew Jagielski, Ariel Herbert-Voss, Katherine Lee, Adam Roberts, Tom Brown, Dawn Song, Úlfar Erlingsson, Alina Oprea, Colin Raffel
- **Year / venue:** 2021 — USENIX Security Symposium 2021
- **Link:** https://arxiv.org/abs/2012.07805
- **What I drew from it:** The perplexity threshold MIA baseline (Section 3) and the fundamental observation that training members receive lower perplexity from the model — the foundational insight underlying all perplexity-based MIA methods.
- **Inspected directly?** Yes

### 3. Privacy Risk in Machine Learning: Analyzing the Connection to Overfitting

- **Authors:** Samuel Yeom, Irene Giacomelli, Matt Fredrikson, Somesh Jha
- **Year / venue:** 2018 — IEEE Computer Security Foundations Symposium (CSF)
- **Link:** https://arxiv.org/abs/1709.01604
- **What I drew from it:** The original formalization of perplexity (loss)-based membership inference: if a model's loss on a sample is below the average training loss, classify as member. Provides the theoretical grounding for why perplexity correlates with membership.
- **Inspected directly?** Yes

## Tool / pattern I ran hands-on

**Name:** Python / PyTorch — MIN-K% Prob sketch
**Version:** torch 2.x
**What I did:** Wrote a minimal MIN-K% Prob function demonstrating how to extract per-token log probabilities from a causal LM and average the k% lowest as the membership signal. Not run against Qwen-2.5 directly — the sketch is illustrative of the method.
**Where the artifact lives:** Inline in `explainer.md §Show it`

## Attribution check

- [x] Every cited paper / tool / source above appears in the explainer's `Pointers` section with the same link.
- [x] No fabricated references.
- [x] No second-hand summary used as a load-bearing citation.
