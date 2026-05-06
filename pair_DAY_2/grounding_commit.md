# Grounding Commit — Day 2

**Asker:** Atnabon Deressa
**Day:** 2
**Topic:** Agent & tool-use internals — function-calling at the token level
**Date:** 2026-05-06

---

## Status

**Pending — explainer not yet received from partner.**

The canonical pair-day flow expects:
1. I (asker) ship a sharpened question (`question.md`).
2. Ramlla (explainer) writes the explainer for my question.
3. After her explainer lands, I make the concrete edit to my own
   portfolio code that the explainer enables.

Ramlla submitted her own assignment before writing an explainer for my
function-calling question (her location had a power outage and she
could not wait — see `evening_call_summary.md`). I therefore have no
explainer to ground a concrete edit against yet.

## Edits I will make once the explainer lands

If Ramlla's explainer confirms function-calling is **constrained
decoding (logit masking over a tool-name vocabulary)**, I will:

- **Repository:** `conversion-engine`
- **File:** `agent/tool_router.py:L42-78`
- **Edit:** Remove the inline tool-list from the system prompt (it is
  redundant when the runtime enforces tool selection via logit masking)
  and tighten the `KeyError` retry-logic comment to reflect that
  hallucinated tool names are *impossible* at the decoder, so any
  observed `KeyError` is a runtime parse bug not a model failure.

If Ramlla's explainer confirms function-calling is **unconstrained
generation + post-hoc parse**, I will:

- **Repository:** `conversion-engine`
- **File:** `agent/tool_router.py:L42-78`
- **Edit:** Replace the bare `KeyError` catch with a typed
  `HallucinatedToolError`, add an upstream tool-name validator before
  the parse step, and add a unit test that asserts the validator
  rejects a known-hallucinated tool name (e.g.
  `update_contract_property` instead of the real `update_contact_property`).

```diff
# tool_router.py — pending edit (one of the two above, depending on explainer)

  try:
      tool_name = response.tool_calls[0].function.name
      return TOOL_REGISTRY[tool_name](**args)
- except KeyError:
-     # treat as parse error — retry once
-     return retry_with_clarification(prompt, attempt=attempt+1)
+ except KeyError as e:
+     # If function-calling is constrained decoding, this branch is
+     # unreachable and indicates a runtime bug, not a model failure.
+     # If function-calling is post-hoc parse, this is a hallucinated
+     # tool name and should not retry — it should fail loudly.
+     raise HallucinatedToolError(tool_name) from e
```

## Honesty note

The rubric's "Grounding Commit" line item rewards a real edit grounded
in the partner's explainer. Because the partner's explainer did not
land in time, I am documenting the *conditional* edit I will make in
each of the two possible mechanism outcomes, rather than fabricating a
commit. This file will be updated with the actual diff and the
explainer-grounded reasoning when Ramlla's explainer is delivered.

## Was this a wording fix or a mechanism fix?

- [ ] Wording fix
- [ ] Mechanism fix
- [ ] Both
- [x] **Pending** — see status note above.
