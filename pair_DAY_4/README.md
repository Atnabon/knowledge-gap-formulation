# Day 4 — Evaluation & statistics

**Date:** 2026-05-08 (Fri)
**Pair:** Atnabon Deressa ↔ Zemzem Hibet
**Status:** Complete (async pair-day).

## Pre-staged candidate gaps (so Act II is real triage, not blank-page)

| Topic | Subtopic | Candidate gap I have already surfaced from my work | Anchor artifact |
|---|---|---|---|
| Agent & tool-use internals | Multi-turn agent planning failure modes | The Conversion Engine pipeline is `enrich → classify → draft → deliver`. The planner is implicit (orchestrator code, not the model). I do not know what the failure modes look like when I let the model own the planning step instead. | [`conversion-engine/agent/`](../../conversion-engine/agent/) |
| Agent & tool-use internals | Reasoning-trace vs final-output tokens | I send Claude Sonnet 4.6's full output (including thinking) to my evaluator without separating reasoning-trace tokens from the final answer. | [`sales-eval-bench/evaluator/scoring_evaluator.py`](../../sales-eval-bench/evaluator/scoring_evaluator.py) |
| Production patterns | Observability spans for agent systems | The Conversion Engine wires Langfuse but I do not have a defensible answer for which spans should capture *what* — and what the typical missing span is when an FDE retros an agent failure. | [`conversion-engine/`](../../conversion-engine/) |
| Production patterns | Rate limiting & backpressure under bursty load | The deliver-stage hits Resend, Africa's Talking, HubSpot MCP, and Cal.com. I have no defended backpressure model. | [`conversion-engine/agent/deliver.py`](../../conversion-engine/agent/deliver.py) |
| Multimodal & embedding | Positional encoding (RoPE / ALiBi) and long context | The eval-tier Claude judge takes a long task + candidate + rubric and is sensitive to position-of-rubric. I cannot defend my choice of rubric placement (system vs user, top vs bottom). | [`sales-eval-bench/evaluator/`](../../sales-eval-bench/evaluator/) |

## Files in this folder

Templates pre-populated from `_templates/`. Fill in across the day per the brief.
