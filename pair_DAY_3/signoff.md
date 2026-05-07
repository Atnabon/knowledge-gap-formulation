# Sign-off — Day 3

**Asker (signing off):** Yohannes Dereje
**Explainer (received from):** Atnabon Deressa
**Topic:** Routing vs transformation under Q+V-only LoRA
**Date:** 2026-05-07

---

## Judgement

- [ ] **Closed** — gap is closed; I can now defend the mechanism unaided.
- [x] **Partially closed** — explainer received and substantive, but final
      authored sign-off pending. Yohannes acknowledged the mechanism cut
      (routing vs transformation) over Slack but had not yet confirmed in
      writing at the time of submission. This file will be overwritten with
      his authored closure paragraph when he confirms.
- [ ] **Not closed**

## What I understand now that I did not before *(placeholder — pending Yohannes's authored paragraph)*

The expected closure paragraph, based on what was discussed over Slack,
should read approximately:

> I now see that my 3 residual SOC failures in
> `ablations/held_out_traces.jsonl` are not a data-quantity problem and
> not random — they are mechanistically diagnostic of Q+V-only LoRA's
> capacity limit. Q+V control information *routing* (which tokens get
> attended to and what values flow forward), which is sufficient for
> suppression — that is why regex_negative passes. FFN layers control
> information *transformation* (per-token computation that composes the
> next-token output), and producing required phrases like "curious
> whether" requires the FFN to learn a key-value memory mapping
> (Geva et al. 2021) from the residual context to that phrase. Q+V
> updates cannot teach the FFN this; it is mechanistically incapable.
> The consequence I had not internalised before today is that my
> regex_negative / regex_positive evaluation split is already encoding
> the routing / transformation cut without naming it — the 3 residual
> failures are not "the model still has bugs", they are "this LoRA
> config cannot learn this behavior class." The remediation is target-
> set expansion (add `gate_proj`, `up_proj`, `down_proj`), not more SFT
> pairs.

## Residual gap (if partial / not closed)

The residual gap I would carry into a follow-up day: **once FFN targets
are added, does the rank choice (`r=16`) need to scale with the larger
adapter parameter count, or does rank-vs-target-modules decouple in
practice?** That follow-up is exactly Atnabon's Day 3 question on rank —
the two questions are deliberately complementary.

## Honesty note

This pair-day ran asynchronously over Slack rather than as live morning
+ evening calls. The substantive mechanism content was delivered to
Yohannes in writing in the Slack thread. Atnabon (explainer) authored
this file as a placeholder; Yohannes will overwrite the closure
paragraph above with his own words when he signs off.
