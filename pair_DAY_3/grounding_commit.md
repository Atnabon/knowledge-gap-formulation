# Grounding Commit — Day 3

**Asker:** Atnabon Deressa
**Day:** 3
**Topic:** Training & post-training — LoRA rank vs adapter expressivity
**Date:** 2026-05-07

---

## Status

**Pending — explainer not yet received from partner.**

The canonical pair-day flow expects:
1. I (asker) ship a sharpened question (`question.md`) on LoRA rank.
2. Yohannes (explainer) writes the explainer for my rank question.
3. After his explainer lands, I make the concrete edit to
   `sales-eval-bench/training/train.py:L52` and
   `sales-eval-bench/methodology.md §LoRA-config`.

Yohannes's battery and connectivity were unreliable through the
afternoon (see `evening_call_summary.md`); he received my question and
acknowledged it but had not delivered an explainer for it at submission
time.

## Edits I will make once the explainer lands

The two plausible mechanism conclusions and the edits each one
implies:

**If the explainer confirms rank `r` controls the dimensionality of
the adapter's update subspace (the SVD-decomposition view) and r=16 is
right because 221 SFT pairs cannot saturate a higher-rank subspace:**

- **Repository:** `sales-eval-bench`
- **File:** `training/train.py:L52` and `methodology.md §LoRA-config`
- **Edit:** Replace the inline `# accepted from Unsloth default`
  comment with a one-line mechanistic defense citing the SVD view; add
  a paragraph to `methodology.md` defending r=16 on a 221-pair task and
  explicitly committing to re-evaluate at v0.2 (~600 pairs).

**If the explainer confirms r=16 is over- or under-parameterized and
the right choice is r=8 or r=32:**

- **Repository:** `sales-eval-bench`
- **File:** `training/train.py:L52`
- **Edit:** Change `r=16` to the recommended rank, retrain on the
  existing 221 pairs, regenerate
  `ablations/held_out_traces.jsonl`, and update
  `methodology.md §LoRA-config` to document the rank change and the
  empirical evidence.

```diff
# train.py:L52 — pending edit (rank value will be set by the explainer's mechanism conclusion)

  peft_config = LoraConfig(
-     r=16,                # accepted from Unsloth default — no mechanistic justification
-     lora_alpha=32,       # effective scaling alpha/r = 2 — also unjustified
+     r=<R>,               # SVD-rank of adapter update subspace; defended in methodology §LoRA-config
+     lora_alpha=<2*R>,    # alpha/r = 2 keeps effective scaling stable across rank changes
      target_modules=["q_proj", "v_proj"],
      lora_dropout=0.05,
      bias="none",
      task_type="CAUSAL_LM",
  )
```

## Honesty note

The rubric's "Grounding Commit" line item rewards a real edit grounded
in the partner's explainer. Because the partner's explainer did not
land in time, I am documenting the *conditional* edit I will make in
each of the two possible mechanism outcomes, rather than fabricating a
commit. This file will be updated with the actual diff and the
explainer-grounded reasoning when Yohannes's explainer is delivered.

## Was this a wording fix or a mechanism fix?

- [ ] Wording fix
- [ ] Mechanism fix
- [ ] Both
- [x] **Pending** — see status note above.
