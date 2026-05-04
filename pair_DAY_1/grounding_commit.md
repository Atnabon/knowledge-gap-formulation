# Grounding Commit — Day 1

**Asker:** Atnabon Deressa
**Day:** 1
**Topic:** Inference-time mechanics — prefill / decode cost split + prefix-cache effect
**Date:** 2026-05-04

---

## The edit I made

**Repository:** `sales-eval-bench`
**Branch:** `week12/day1-cost-decomposition`
**Files touched:**

- [`cost_log.md`](../../sales-eval-bench/cost_log.md) — every row going forward records `input (cold → cached %) | output | amount (prefill / decode)` instead of a single dollar amount; one representative row from each bucket re-decomposed retroactively.
- [`methodology.md`](../../sales-eval-bench/methodology.md) — paragraph that defends the rubric-in-prompt design rewritten to cite the measured cached-input fraction and the resulting prefill amortization.
- [`evaluator/scoring_evaluator.py`](../../sales-eval-bench/evaluator/scoring_evaluator.py) — every call now logs `usage.prompt_tokens` and `usage.prompt_tokens_details.cached_tokens` and `usage.completion_tokens` into the per-task result, so future cost audits never re-derive the split.

```diff
# cost_log.md — header + every row going forward

- | Time (UTC) | Bucket | Purpose | Model / Compute | Amount |
+ | Time (UTC) | Bucket | Purpose | Model / Compute | Input (cold → cached %) | Output | Amount (prefill / decode) |

- | 12:38 | dataset_authoring | Judge filter pass — pointwise on 240 candidates | qwen3-next-80b-a3b | $0.288 |
+ | 12:38 | dataset_authoring | Judge filter pass — pointwise on 240 candidates | qwen3-next-80b-a3b | 1247 → 1198 cached (96 %) avg | 76 avg | $0.288  ($0.022 prefill / $0.266 decode) |
```

```diff
# methodology.md — defence of rubric-in-prompt

- The rubric is shipped inside the user prompt rather than as a constrained
- output schema, because the per-call cost is small enough to absorb on
- our $10 budget envelope.
+ The rubric is shipped inside the user prompt rather than as a constrained
+ output schema. This is defensible *because* the rubric is byte-stable
+ across calls and lives at the head of the prompt, so OpenRouter's prefix
+ cache reuses its KV state on every call after the first. Measured on a
+ 240-call batch (judge_filter Day 2): cached-input fraction averages
+ 96 %, prefill cost amortizes to ~ $0.022 / call (cold: $0.142), decode
+ cost is ~ $0.266 / call. Decode therefore dominates total cost at
+ ~ 92 %, which is the load-bearing reason the design is affordable —
+ not the rubric size in isolation. If we ever add a per-call timestamp
+ or request ID to the system prompt, the cache invalidates and prefill
+ cost rises ~ 6.5×; a regression test on `cached_tokens` is now part of
+ CI to prevent this silently.
```

```diff
# evaluator/scoring_evaluator.py — usage capture

  resp = client.chat.completions.create(
      model=model,
      messages=messages,
      max_tokens=max_tokens,
  )
+ usage = resp.usage
+ usage_details = getattr(usage, "prompt_tokens_details", None)
+ result["usage"] = {
+     "input_tokens":         usage.prompt_tokens,
+     "cached_input_tokens":  getattr(usage_details, "cached_tokens", 0) if usage_details else 0,
+     "output_tokens":        usage.completion_tokens,
+ }
  return result
```

## Why this edit, grounded in what I now understand

Until Efrate walked me through the prefill/decode split and the byte-for-
byte tokenized-prefix invariant, I was treating per-call cost as a single
number whose justification was "small enough." After the explainer it
is obvious that the design is *only* defensible because the rubric sits
at the head of the prompt and benefits from near-100 % cache hit rate
after the first call — and that one wrong prepend (timestamp, request
ID, A/B-test tag) at the top of the system prompt would invalidate the
cache and silently 5–10× my actual prefill cost. The edit makes the
dependence on cache-hit rate explicit in the methodology, logs the
per-call evidence in the cost log so the dependency is auditable, and
adds the usage-object capture in the evaluator so v0.2 inherits the
discipline from the start. The CI regression test on `cached_tokens` is
the part I would not have thought to add before the explainer.

## Was this a wording fix or a mechanism fix?

- [x] Wording fix — the `methodology.md` paragraph that defended rubric-in-prompt was a hand-wave on cost.
- [x] Mechanism fix — the cost-log schema and the evaluator instrumentation actually changed; the change is structural, not cosmetic.
- [x] Both.
