# Tweet thread — Day 1

**Platform:** X (mirror to LinkedIn)
**Length:** 6 tweets
**Standalone test:** A reader who never clicks through still leaves with the mechanism (KV-state reuse on a strict tokenized-prefix match; cache helps prefill, not decode; one-byte change at the top breaks every hit).
**Status:** Pre-evening-call draft

---

**1/** Most engineers shipping LLM agents know "prefix caching saves money." Almost none can tell you what gets *invalidated* on a cache miss vs hit, which is the only thing that matters when you design a long-prompt system. 🧵

**2/** The mechanism: every input token has a (key, value) tensor pair at every transformer layer. **Prefill** computes those pairs from scratch and dominates long-prompt cost. A cache hit reuses the KV state for a literal byte-for-byte tokenized prefix; the provider skips prefill on the cached portion.

**3/** **Decode** (the per-output-token loop) gets none of this. Decode reads from the cache but writes new KV pairs for every generated token. So a hit cuts prefill ~ to zero on the matched prefix and leaves decode unchanged.

**4/** Probe it on any OpenAI-compatible endpoint:

```python
resp = client.chat.completions.create(...)
u = resp.usage
u.prompt_tokens                                    # 1251
u.prompt_tokens_details.cached_tokens              # 1198  (96 % hit)
u.completion_tokens                                # 78
```

Cached input bills at 0.1× – 0.5× of the uncached rate (provider-dependent). TTFT drops in proportion to cached fraction.

**5/** The footgun: invalidation is binary at the **first divergent token**. Prepend `# generated <timestamp>` to your system prompt and every call has a new prefix → 0 % hit rate. Static content goes first. Per-call content goes last. Always.

**6/** Once the cache is warm, decode is the cost ceiling, not prefill. That flips your optimization target: growing the rubric is cheap, growing the JSON output schema is expensive. Full write-up + code: <link to blog>
