# Day 2 — Agent & tool-use internals (asker) / Long-context decoding mechanics (explainer)

**Status:** Submitted (async pair-day).
**Date:** 2026-05-06
**Pair:** Atnabon Deressa ↔ Ramlla Akmel
**My question (asker):** Function-calling at the token level — constrained decoding vs post-hoc parse — see [`question.md`](question.md).
**Partner's question (explainer):** Mode collapse + lost-in-the-middle decay in the Conversion Engine Draft stage — see [`explainer.md`](explainer.md).
**Honesty note:** This pair-day ran asynchronously over Slack rather than as live morning + evening calls (partner had a power outage and submitted independently before the formal sign-off step). See [`morning_call_summary.md`](morning_call_summary.md) and [`evening_call_summary.md`](evening_call_summary.md) for the actual record. Sign-off and grounding-commit are marked **pending** in their respective files until partner returns to confirm.

## Pre-staged candidate gaps (so Act II is real triage, not blank-page)

The brief says the asker's morning research is itself work — so these are
candidate gaps **already surfaced** from Week 10/11 artifacts. On Tuesday
morning I take the day's actual topic, intersect it with this list, pick
one, and let it survive (or fail) the four-property check.

| Topic | Subtopic | Candidate gap I have already surfaced from my work | Anchor artifact |
|---|---|---|---|
| Inference-time mechanics | KV cache + prefix caching | The Conversion Engine "Draft" stage builds an email per prospect with a long shared system prompt. I assert prompt-cache savings without knowing whether OpenRouter's prefix-cache is per-tenant, per-key, or per-route, or how invalidation lands when I edit the system prompt mid-batch. | [`conversion-engine/agent/draft.py`](../../conversion-engine/agent/draft.py) |
| Inference-time mechanics | Prefill vs decode cost split | I quote a per-task cost in `cost_log.md` as a single number. I do not know what fraction is prefill (one-shot, scales with input tokens) vs decode (per-output-token, scales with sampling), so I cannot defend the choice to put the rubric inside the prompt instead of a constrained-output schema. | [`sales-eval-bench/cost_log.md`](../../sales-eval-bench/cost_log.md) |
| Agent & tool-use internals | Function-calling at the token level | The HubSpot MCP integration in Conversion Engine assumes the model "chooses" a tool. I do not actually know whether function-calling is a constrained-decoding pass over a tool-name vocabulary or a structured output that the runtime parses. | [`conversion-engine/agent/`](../../conversion-engine/agent/) |
| Training & post-training | What LoRA actually adapts at rank 16 | I trained the Tenacious judge with `LoRA r = 16` and have no defense for that choice over r = 8 or r = 32 beyond "the recipe used it". | [`sales-eval-bench/training/`](../../sales-eval-bench/training/) |
| Production patterns | Structured output / constrained decoding | The ICP classifier uses a JSON-schema-constrained output. I cannot defend whether the constraint is enforced via logit masking, regex over decoded tokens, or repair-loop re-prompting. | [`conversion-engine/agent/classify.py`](../../conversion-engine/agent/classify.py) |

## Files in this folder

The eight deliverable files have been pre-populated from `_templates/`. Fill
in after the morning call (`question.md`, `morning_call_summary.md`),
during the day (`explainer.md`, `thread.md`, `sources.md`), and after the
evening call (`evening_call_summary.md`, `signoff.md`,
`grounding_commit.md`).
