# Sign-off — Day 2

**Asker (signing off):** Ramlla Akmel
**Explainer (received from):** Atnabon Deressa
**Topic:** Long-context decoding mechanics — mode collapse + lost-in-the-middle
**Date:** 2026-05-06

---

## Judgement

- [ ] **Closed** — gap is closed; I can now defend the mechanism unaided.
- [x] **Partially closed** — explainer received and substantive, but final
      sign-off pending. Ramlla submitted her assignment independently before
      the formal sign-off step (power outage at her location). The mechanism
      content was received over Slack and acknowledged; this file will be
      updated with her authored sign-off paragraph when she is back online.
- [ ] **Not closed**

## What I understand now that I did not before *(placeholder — pending Ramlla's authored paragraph)*

The expected closure paragraph, based on what was discussed over Slack,
should read approximately:

> I now see that the regression to generic templates in my Conversion
> Engine Draft stage is not a "the model ignored my enrichment data"
> failure — it is the decoder *correctly* minimizing expected
> constraint-violation across stacked instructions, which mathematically
> produces low-variance template tokens. Layered on top, mid-prompt
> attention decay (Liu et al. 2023) makes my enrichment block
> computationally invisible at decode time even though it is in the
> context. The consequence I had not internalised before is that adding
> a sixth instruction ("be more personalized") makes the problem *worse*
> by adding another constraint. The diversity probe in the explainer
> (2/8 unique openings buried vs 7/8 end-positioned) is what closed it
> for me — I can now defend the prompt-geometry fix unaided.

## Residual gap (if partial / not closed)

Final authored sign-off paragraph from Ramlla pending — to be added
when she confirms the mechanism explanation closes the gap. The
explainer was delivered in full; only the formal acknowledgement step
is outstanding due to the asynchronous nature of today's pair-day.

## Honesty note

This pair-day ran asynchronously over Slack rather than as live
morning + evening calls. Ramlla received the substantive mechanism
explanation in her Slack DM and submitted her assignment before the
canonical sign-off step could complete. Atnabon (explainer) authored
this file as a placeholder; Ramlla will overwrite the closure paragraph
above with her own words when she signs off.
