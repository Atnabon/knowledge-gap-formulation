# Tweet thread — Day 4

**Platform:** X / LinkedIn
**Length:** 5 tweets
**Standalone test:** A reader who never clicks through still gets a coherent, correct compressed explanation.
**Post-revision status:** draft (pre evening-call revision)

---

**1/** Your LLM eval bench passes n-gram overlap, embedding similarity, and time-shift checks. Someone asks: "how do you know the base model didn't see these tasks during pre-training?" You have no answer. Here's the distinction that explains why your checks can't answer that question — and what can.

**2/** Your held-out partition checks verify one thing: your tasks didn't leak into your fine-tuning data. You control both sides, so you can measure overlap directly. Base model contamination is different — you're asking if Qwen saw your tasks in its 3-trillion-token pre-training corpus. You don't have that corpus. N-gram overlap requires data you can't inspect.

**3/** Membership Inference Attacks (MIA) are the right tool. The core insight: if a model trained on a sample, it assigns that sample lower perplexity than a comparable non-member. MIN-K% Prob (Shi et al. 2023) makes this robust: instead of average perplexity, use the average log-prob of the k% *lowest*-probability tokens — less sensitive to stopwords dominating the signal.

```python
# sketch: MIN-K% Prob (k=20%)
token_log_probs = get_per_token_log_probs(model, text)
n_min = max(1, int(len(token_log_probs) * 0.2))
score = token_log_probs.topk(n_min, largest=False).values.mean()
# more negative = less likely = safer (non-member signal)
```

**4/** What MIA cannot prove: "this sample was definitely not in training." Low MIA signal means the model generalizes well — not that it never saw the data. The honest framing: MIA gives probabilistic evidence with real false-positive rates. The strongest available signal is temporal: tasks created *after* the model's training cutoff cannot have been memorized.

**5/** Practical fix: add one paragraph to your datasheet. State (a) that held-out partition checks verify pipeline integrity, not pre-training exposure, (b) whether you ran MIN-K% Prob and what the distribution looked like, and (c) the temporal gap between task creation date and the model's training cutoff. That bounds what your contamination checks actually prove — which is more defensible than silence.
