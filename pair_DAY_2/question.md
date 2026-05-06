# Question — Day 2

**Topic:** Agent & tool-use internals
**Subtopic:** Function-calling at the token level
**Asker:** Atnabon Deressa
**Partner (explainer):** Ramlla Akmel
**Date:** 2026-05-06
**Status:** Final (post async-call)

---

## My sharpened question

> When my Conversion Engine routes a prospect's reply to the HubSpot MCP
> integration and the LLM "decides" to call `update_contact_property`, what
> is *mechanically* happening at the decoder — is the model performing a
> constrained-decoding pass over a tool-name vocabulary (logit masking at
> the tool-selection step), or is it generating an unconstrained JSON object
> that my runtime then parses and routes? The two have very different
> failure modes, and my retry logic currently treats them as equivalent.

## Why this is the gap I picked (asker's triage)

I read [`conversion-engine/agent/`](../../conversion-engine/agent/) as a
hostile reviewer this morning and surfaced four candidate gaps. (1) "Why
DeepSeek vs Qwen for the Draft stage?" — discarded; price-shopping
question I can already defend. (2) "How do I count tool-call tokens for
billing?" — discarded; OpenRouter's usage object answers it. (3) "Why
does my agent sometimes call a non-existent tool?" — kept as a candidate
but it is symptomatic, not mechanistic. (4) **"Is function-calling
constrained decoding or post-hoc parsing?"** — this is the one. My
production retry logic assumes "tool-not-found" errors are runtime parse
bugs (which is only true if function-calling is constrained decoding).
If it's actually unconstrained generation + parse, then the model can
hallucinate tool names that pass JSON schema validation but fail my
router, and my retry logic is catching the wrong failure mode.

## Connection to a specific Week 10 or 11 artifact

**Artifact:** [`conversion-engine/agent/tool_router.py:L42-78`](../../conversion-engine/agent/tool_router.py)
**Current claim/choice in that artifact:**

> ```python
> # tool_router.py — current retry logic
> try:
>     tool_name = response.tool_calls[0].function.name
>     return TOOL_REGISTRY[tool_name](**args)
> except KeyError:
>     # treat as parse error — retry once
>     return retry_with_clarification(prompt, attempt=attempt+1)
> ```
>
> (The `KeyError` branch assumes the model "tried" to call something that
> doesn't exist. Whether this is mechanically possible depends on whether
> the provider implements function-calling as constrained decoding.)

**What closing this gap will let me change:**

After Ramlla's explainer lands I will (a) replace the bare `KeyError`
catch with a typed `HallucinatedToolError` if function-calling turns out
to be unconstrained, (b) add an upstream tool-name validator before the
parse step, and (c) rewrite the agent's prompt to include the tool list
inline only if the provider does *not* enforce it via logit masking. If
the provider does enforce constrained decoding, the redundant inline
list is dead bytes inflating my prefill cost on every call.

## Four-property self-check

- [x] **Diagnostic** — names a specific mechanism (constrained decoding via logit masking vs structured output + post-hoc parse), not "how does function calling work" in general.
- [x] **Grounded in cohort work** — names `tool_router.py:L42-78` and quotes the retry logic that depends on the answer.
- [x] **Generalizable** — every FDE shipping an agent with tool-use through OpenAI-compatible APIs faces this; the same diagnostic applies to MCP, HubSpot connectors, and any function-calling integration.
- [x] **Resolvable** — 600–1,000 words can cover the two implementations, the failure-mode difference, and a probe to tell which one a provider uses.
