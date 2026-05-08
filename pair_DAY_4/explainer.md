# What Membership Inference Actually Tests — and Why N-gram Overlap on Held-Out Partitions Is a Different Problem

**Written for:** Zemzem Hibet's gap on benchmark contamination and base model pre-training data
**By:** Atnabon Deressa
**Date:** 2026-05-08
**Length target:** 600–1,000 words
**Status:** First draft (sent via Slack) · Asker sign-off: pending

---

## The question, anchored

Zemzem's eval bench passes three contamination checks — n-gram overlap,
embedding similarity, and time-shift verification — confirming that held-out
tasks did not leak into the fine-tuning partition. But when a client asks "how
do you know Qwen didn't see these tasks during pre-training?", she has no
answer. The gap is: what tests exist for base model pre-training contamination,
what can they actually prove, and why can't the held-out partition checks answer
this question?

## The load-bearing mechanism

The three checks Zemzem already has all verify the same thing: *your held-out
tasks did not leak into your fine-tuning data or evaluation loop*. You control
both sides — you have the fine-tuning corpus and the held-out set, so you can
directly measure overlap. This is a **data pipeline integrity problem**, and her
checks solve it correctly. Pre-training contamination is a fundamentally
different problem: you are now asking whether Qwen-2.5 — trained on ~3 trillion
tokens of filtered Common Crawl, GitHub, books, and code — saw these exact
benchmark tasks during its original training. You do not have access to that
corpus. You cannot run n-gram overlap against a dataset you don't have. The
methodology does not transfer because the data you need to check is not yours
to inspect.

Membership Inference Attack (MIA) is the family of techniques for this second
problem. The key statistical insight: if a model was trained on a sample, it
will typically assign that sample **lower perplexity** (higher probability) than
a held-out non-member sample with similar surface properties. MIA exploits this
signal.

## Show it

Four concrete MIA methods, in order of robustness:

**1. Perplexity threshold (Yeom et al. 2018, Carlini et al. 2021)**
Flag a sample as a potential training member if `perplexity(sample) < threshold`.
Crude and high false-positive rate — base models have low perplexity on any
in-distribution text, whether or not they saw it during training.

**2. MIN-K% Prob (Shi et al. 2023)**
Instead of average perplexity, look at the *k%* of tokens with the lowest
individual probability in the sequence. Members tend to have higher minimum-token
probabilities than non-members because the model has "seen" even the surprising
tokens. More robust than average perplexity because it is less sensitive to
high-probability stopwords dominating the average.

```python
# MIN-K% Prob sketch (k=20)
import torch

def min_k_prob(model, tokenizer, text, k=0.2):
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits
    log_probs = torch.log_softmax(logits[0, :-1], dim=-1)
    token_log_probs = log_probs.gather(1, inputs.input_ids[0, 1:].unsqueeze(1)).squeeze()
    n_tokens = len(token_log_probs)
    n_min = max(1, int(n_tokens * k))
    min_k_avg = token_log_probs.topk(n_min, largest=False).values.mean().item()
    return min_k_avg  # more negative = less likely = safer (non-member)
```

**3. Likelihood ratio attack**
Compare `log P_base(sample) / log P_ref(sample)` where `P_ref` is a reference
model trained on known non-contaminated data. Ratio > 1 suggests the base model
assigns disproportionately high probability — a membership signal. Requires a
clean reference model of comparable capability.

**4. Canary / watermark test**
Insert synthetic benchmark tasks with unique phrasings that did not exist on the
internet before a known date. If the model has memorized them, they were in
pre-training. This is the only fully conclusive test, and it requires designing
tasks *after* the model's training cutoff.

## Connect the dots

### What MIA can actually prove — and cannot

MIA gives probabilistic evidence, not certainty. The false positive rate is
significant: a model can have low perplexity on a task simply because the
task's domain matches its training distribution, even if the exact task was
never seen. "MIA flagged this task" means "this task is plausibly in-distribution
for Qwen's training corpus" — not "Qwen memorized this exact task." The claim
MIA cannot support is the negative: "Qwen definitely did not see this task."
Absence of MIA signal is not evidence of absence. Statistical power of MIA
decreases for models that generalize well, because they assign similar
perplexity to members and non-members alike.

### Time-shift verification as the strongest available signal

If Zemzem's benchmark tasks were phrased or created after Qwen-2.5's training
cutoff (roughly 2024-Q3 for the Qwen-2.5 family), temporal verification is
stronger than any perplexity-based MIA. A task that did not exist during
training cannot have been memorized. This is worth checking in the datasheet
alongside the MIA methods.

### The honest framing for the datasheet

Zemzem's current three checks protect the evaluation pipeline she controls. The
honest addition to `datasheet.md §contamination` is:

> "MIA for base model pre-training contamination was not performed. Tasks are
> phrased in domain-specific sales-conversation language unlikely to appear
> verbatim in web-scale pre-training corpora. Temporal verification: all tasks
> were authored in [date] — after Qwen-2.5's training cutoff of [cutoff date].
> Residual pre-training contamination risk is acknowledged as non-eliminable
> without access to the training corpus."

That framing is more defensible than silence, and it honestly bounds what the
checks prove.

## Pointers

- **MIN-K% Prob — Shi et al. 2023:** "Detecting Pretraining Data from Large Language Models" — arXiv:2310.16789
- **Perplexity-based MIA — Carlini et al. 2021:** "Extracting Training Data from Large Language Models" — USENIX Security 2021
- **Yeom et al. 2018:** "Privacy Risk in Machine Learning: Analyzing the Connection to Overfitting" — CSF 2018
- **Follow-on direction:** Watson et al. 2022, "Importance of Difficulty Calibration in Membership Inference Attacks" — NeurIPS 2022 — explains why MIA power varies by task difficulty

---

> **Scope note.** I focused on perplexity-based MIA and MIN-K% Prob because
> these are runnable without a reference model. The likelihood ratio attack and
> canary/watermark approach would be the next two sections in a fuller treatment.
> I did not cover differential privacy guarantees or audit-log-based provenance
> methods, which are out of scope for the datasheet question.
