# Evening Call Summary — Day 4

**Date:** 2026-05-08
**Pair:** Atnabon Deressa ↔ Zemzem Hibet
**Duration:** Async (Slack DM — no synchronous evening call)
**Author:** Atnabon Deressa
**Confirmed by:** Zemzem Hibet — pending

---

The evening exchange ran async over Slack DM. Zemzem's explainer on
statistical significance for small binary eval sets arrived in the evening.
The load-bearing mechanism she delivered: for a binary pass-rate comparison on
N=89 with 3 failures (v0.2) vs 0 failures (v0.3), the appropriate test is
**Fisher's exact test** on the 2×2 contingency table, and the appropriate
uncertainty representation is the **Clopper-Pearson (exact binomial) 95% CI**
on each proportion. The 95% CI for v0.2's 96.6% pass-rate is approximately
[90.3%, 99.3%] and for v0.3's 100% is [95.9%, 100%]. These intervals overlap,
which means the data are consistent with no true difference — but also
consistent with a real improvement. The honest claim is not "v0.3 is
significantly better" but "v0.3 shows no observed failures on 89 samples;
95% CI [95.9%, 100%]; Fisher's exact p=0.24 (one-sided)." Zemzem noted that
bootstrap resampling is an alternative for paired comparisons but Fisher's
exact is more interpretable in a methodology section for an audience that may
not know bootstrap mechanics. One clarification was needed on first pass: why
the rule-of-3 lower bound gives approximately the same answer as exact
Clopper-Pearson for the 0-failure case (both give ~96.7%). Once that was
clear, sign-off was immediate. No second-pass revision required.
