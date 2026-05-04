# Sources — Day 1

**Day:** 1
**Topic:** Inference-time mechanics
**Explainer author:** Atnabon Deressa
**Question this serves:** "What specifically gets invalidated on a prefix-cache miss versus a hit, and through what mechanism does that change my per-call latency and cost?"

---

## Canonical sources (minimum two; original papers > authoritative documentation > second-hand summaries)

### 1. DeepSeek-AI — *DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model*

- **Authors:** DeepSeek-AI (Liu et al.)
- **Year / venue:** 2024, arXiv preprint
- **Link:** <https://arxiv.org/abs/2405.04434>
- **What I drew from it:** Section 4's description of the server-side
  context-cache architecture — the KV-state reuse mechanism that became
  the industry pattern. This is the load-bearing reference for the
  explainer's "load-bearing mechanism" paragraph (what state is reused,
  what is not, and why prefill is the only phase that benefits).
- **Inspected directly?** Yes.

### 2. Anthropic — *Prompt caching* (developer documentation)

- **Authors:** Anthropic
- **Year / venue:** 2024–2026, official developer documentation
- **Link:** <https://docs.claude.com/en/docs/build-with-claude/prompt-caching>
- **What I drew from it:** The most explicit public description of the
  byte-for-byte tokenized-prefix invalidation rule, the discounted-rate
  pricing structure, and the 5-minute default TTL. The explainer's
  invalidation paragraph and the "where the cache lives" connect-the-
  dots paragraph rely on this directly.
- **Inspected directly?** Yes.

## Tool / pattern I ran hands-on

**Name:** OpenAI-compatible chat-completion API against `anthropic/claude-haiku-4.5` via OpenRouter
**Version:** `openai==1.x` Python SDK, OpenRouter passthrough, `cache_control: {"type": "ephemeral"}` set on system-prompt content block
**What I did:** Ran a 4-call probe — two calls with a 3,167-token stable system prompt (Pass A) and two calls with a per-call UTC timestamp prepended (Pass B). Logged `input_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`, and `output_tokens`. Observed that OpenRouter does not surface Anthropic's cache usage fields in the `/chat/completions` response object; the `input_tokens` count being identical across Pass A calls confirms the tokenization is stable as the mechanism predicts. The cache-hit signal requires the native Anthropic SDK or the OpenRouter billing dashboard. This is itself an FDE production finding documented in the results file.
**Where the artifact lives:** [`canonical/day1_prefix_cache_probe.py`](../canonical/day1_prefix_cache_probe.py), [`canonical/day1_prefix_cache_probe_results.md`](../canonical/day1_prefix_cache_probe_results.md)

## Attribution check

- [x] Every cited paper / tool / source above appears in the explainer's `Pointers` section with the same link.
- [x] No fabricated references.
- [x] No second-hand summary used as a load-bearing citation.
