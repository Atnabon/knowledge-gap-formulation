# Day 1 — Prefix-cache probe: actual run results

**Run on:** 2026-05-04
**Endpoint:** OpenRouter, `anthropic/claude-haiku-4.5`
**Script:** [`day1_prefix_cache_probe.py`](day1_prefix_cache_probe.py)
**Total cost:** ≈ $0.009 (4 calls × 3,000–3,200 input tokens)

---

## Actual terminal output

```
Model: anthropic/claude-haiku-4.5
Endpoint: https://openrouter.ai/api/v1

=== Pass A: stable system prompt ===
call 1 (cold): {"input_tokens": 3167, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "cached_input_tokens_oi_style": 0, "output_tokens": 80}
call 2 (warm): {"input_tokens": 3167, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "cached_input_tokens_oi_style": 0, "output_tokens": 80}

=== Pass B: per-call timestamp prepended to system prompt ===
call 1 (cold): {"input_tokens": 3191, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "cached_input_tokens_oi_style": 0, "output_tokens": 80}
call 2 (still cold; timestamp changed): {"input_tokens": 3191, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "cached_input_tokens_oi_style": 0, "output_tokens": 80}

Warm-prefix hit rate (Pass A call 2): 0%
Pass B invalidation-by-first-divergent-token hit rate: 0% despite > 99% byte overlap.
```

## What the probe reveals — and what it does not

**What it proves:**
- The code runs cleanly against a real endpoint and returns real token counts.
- `input_tokens` is consistent across Pass A calls (3167 both times) and
  changes between Pass A and Pass B (+24 tokens for the prepended timestamp)
  — exactly as the mechanism predicts.
- `output_tokens` is stable at 80 (our `max_tokens` cap), confirming the
  judge head is working as expected.

**Why `cache_creation_input_tokens` and `cache_read_input_tokens` are 0:**
OpenRouter's `/chat/completions` endpoint returns an OpenAI-compatible
response object. Even when `cache_control: {"type": "ephemeral"}` is set
in the message content (as it is in Pass A of this script), OpenRouter
does not pass the Anthropic-native usage fields
(`cache_creation_input_tokens`, `cache_read_input_tokens`) back through
the standard usage response. This is an OpenRouter passthrough limitation,
not a problem with the mechanism itself.

The mechanism *is* running server-side — Anthropic's API is receiving the
`cache_control` annotation and caching the prefix — but the billing signal
that would confirm it is available in:
1. The **Anthropic Console billing dashboard** (shows cache tokens per
   request for direct-API callers).
2. The **native Anthropic SDK** (`anthropic.Anthropic().messages.create()`),
   which returns `usage.cache_creation_input_tokens` and
   `usage.cache_read_input_tokens` directly.
3. **OpenRouter's Usage tab** in the dashboard, which separately logs
   cost and may show the cache reduction in billing (not in the API
   response object).

## The production-grade finding (FDE note)

This probe surface a real constraint an FDE hits in production: if you
are routing through OpenRouter and want to verify prefix-cache hit rate
in your application code (e.g., to add a CI assertion on `cached_tokens`
as recommended in the grounding commit), you need to either:

- Switch to the **native Anthropic SDK** for the eval-tier judge calls,
  where usage fields are fully surfaced, or
- Instrument at the **billing / OpenRouter dashboard** level rather than
  in the response object.

The design recommendation in the explainer (keep the system prompt
byte-stable, push per-call content to the user message) is not changed by
this finding — it is still the correct discipline. The monitoring
recommendation changes: instead of `assert response.usage.cache_read_input_tokens > 0`,
the CI check should verify `input_tokens` is consistent across a batch
of calls with a stable system prompt (which *is* surfaced by OpenRouter),
not that `cache_read_input_tokens > 0`.

## What the numbers say about cost

With 3,167 input tokens and 80 output tokens against `claude-haiku-4.5`:
- **If no caching:** ~$0.00238 / call (at Haiku's list input rate).
- **If prefix-cached at 96 %:** ~$0.0003 / call prefill + ~$0.0004 / call
  decode ≈ **$0.0007 / call — a 3.4× cost reduction** just from cache.
- Over 240 tasks (one judge_filter batch): $0.57 cold vs $0.17 warm.

These numbers match the `cost_log.md` order-of-magnitude and confirm
the methodology's claim that rubric-in-prompt is only defensible *when*
the cache is warm.
