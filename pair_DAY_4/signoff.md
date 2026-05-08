# Sign-off — Day 4

**Asker (signing off):** Atnabon Deressa
**Explainer (received from):** Zemzem Hibet
**Topic:** Statistical significance and confidence intervals on small binary-outcome eval sets
**Date:** 2026-05-08

---

## Judgement

- [x] **Closed** — gap is closed; I can now defend the mechanism unaided.
- [ ] **Partially closed**
- [ ] **Not closed**

## What I understand now that I did not before

My gap is closed because I now understand that claiming "v0.3 eliminates all
3 residual SOC failures" is a directional observation, not a statistical claim —
and I can now defend the difference precisely. Before this explainer I was
either tempted to write "p < 0.05" without checking whether that applied, or
to say nothing quantitative at all. I now understand that for binary pass-rate
comparisons on N=89, the right path is two things together: a **Clopper-Pearson
(exact binomial) 95% CI** on each proportion — not a t-interval, which requires
continuous outcomes — and **Fisher's exact test** on the 2×2 contingency table
rather than chi-squared, which becomes unreliable when expected cell counts fall
below 5, which they do here given only 3 failures in the v0.2 cell.

The specific numbers that closed the gap: v0.2 CI = [90.3%, 99.3%], v0.3 CI =
[95.9%, 100%], Fisher's exact p = 0.24 (one-sided). These overlap — so the
data do not exclude the possibility that the two versions have the same true
pass-rate, but they are also consistent with a real improvement. The correct
claim is: "v0.3 shows no observed failures on the 89-sample held-out set
(95% CI [95.9%, 100%]); Fisher's exact p = 0.24, consistent with sampling
variation at this N." That is a calibrated claim. It is not weaker than "v0.3
is better" — it is more useful to a reviewer who knows what to do with a CI.

The secondary thing this explainer corrected: I thought bootstrap resampling was
the modern preferred approach and exact binomial was old-fashioned. Zemzem's
explainer clarified that bootstrap resampling is appropriate for paired samples
or complex statistics with no closed-form distribution; for two independent
proportions with small N, the exact binomial is both simpler and more correct,
and a methodology reader does not need to know what bootstrapping is to verify
the claim.

## Residual gap

None. The grounding commit (adding the CI column and Fisher's exact p-value to
the v0.2 vs v0.3 comparison table in `methodology.md`) is the only edit this
gap requires.
