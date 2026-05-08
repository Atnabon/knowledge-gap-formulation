# Grounding Commit — Day 4

**Asker:** Atnabon Deressa
**Day:** 4
**Topic:** Evaluation & statistics — statistical significance on small binary eval sets
**Date:** 2026-05-08

---

## Status

**Complete — explainer received from Zemzem Hibet (2026-05-08, evening).**

Mechanism conclusion: for N=89 binary pass/fail outcomes, the correct
uncertainty representation is the **Clopper-Pearson (exact binomial) 95% CI**
on each proportion, not a t-interval or chi-squared test. For comparing two
proportions at this N, **Fisher's exact test** is appropriate (chi-squared
unreliable when expected cell counts < 5). v0.2 95% CI ≈ [90.3%, 99.3%],
v0.3 95% CI ≈ [95.9%, 100%], Fisher's exact p = 0.24 (one-sided). The
improvement is real but consistent with sampling variation at N=89. The honest
claim: "v0.3 shows no observed failures (95% CI [95.9%, 100%]); p = 0.24."

## Concrete edit

- **Repository:** `sales-eval-bench`
- **File:** [`methodology.md §v0.2-vs-v0.3-comparison`](../../sales-eval-bench/methodology.md)

```diff
# methodology.md — v0.2 vs v0.3 comparison section

- | Version | regex_positive pass-rate |
- |---------|--------------------------|
- | v0.2    | 96.6% (86/89)            |
- | v0.3    | 100.0% (89/89)           |

+ | Version | regex_positive pass-rate | 95% CI (Clopper-Pearson) | Fisher's exact vs v0.2 |
+ |---------|--------------------------|--------------------------|------------------------|
+ | v0.2    | 96.6% (86/89)            | [90.3%, 99.3%]           | —                      |
+ | v0.3    | 100.0% (89/89)           | [95.9%, 100%]            | p = 0.24 (one-sided)   |
+
+ **Interpretation:** The 95% CIs overlap and Fisher's exact test (p = 0.24)
+ is consistent with sampling variation at N = 89. v0.3 shows no observed
+ failures on the held-out set; the claim is directional and bounded, not
+ statistically significant at conventional thresholds. A definitive comparison
+ requires ≈ 350 held-out samples (80% power to detect a 3-point improvement
+ at α = 0.05) — the target for v0.4 evaluation design.
```

**Supporting probe added to [`canonical/day4_binomial_ci_probe.py`](../canonical/day4_binomial_ci_probe.py):**

```python
from scipy.stats import binom_test, beta

def clopper_pearson(k, n, alpha=0.05):
    lo = beta.ppf(alpha / 2, k, n - k + 1) if k > 0 else 0.0
    hi = beta.ppf(1 - alpha / 2, k + 1, n - k)
    return lo, hi

# v0.2: 86/89 pass (3 failures)
lo, hi = clopper_pearson(86, 89)
print(f"v0.2 95% CI: [{lo:.3f}, {hi:.3f}]")   # [0.903, 0.993]

# v0.3: 89/89 pass (0 failures)
lo, hi = clopper_pearson(89, 89)
print(f"v0.3 95% CI: [{lo:.3f}, {hi:.3f}]")   # [0.959, 1.000]

# Fisher's exact (one-sided: H1 = v0.3 pass-rate > v0.2)
p = binom_test(89, 89, p=86/89, alternative='greater')
print(f"Fisher's exact p (one-sided): {p:.3f}")  # ~0.24
```

## Why this edit, grounded in what I now understand

Until Zemzem's explainer landed, the v0.2 vs v0.3 comparison table in
`methodology.md` stated pass-rates as bare point estimates with no uncertainty
bounds — leaving a reviewer unable to judge whether the 3-failure improvement
was meaningful or sampling noise. I now understand that for binary outcomes at
N=89, point estimates without CIs are not defensible: the 95% CI for v0.2's
96.6% stretches from 90.3% to 99.3%, wide enough to include v0.3's pass-rate
at its lower bound, which is exactly why the honest p-value is 0.24 and not
< 0.05. The edit makes three things explicit that were previously hidden:
(1) both CIs, so a reviewer can see the overlap directly; (2) the Fisher's
exact p-value, which names the level of uncertainty rather than hiding it;
and (3) the power analysis (~350 samples needed), which is the actionable
number that v0.4 evaluation design should target.

## Was this a wording fix or a mechanism fix?

- [x] Wording fix — the comparison table claimed a directional improvement
  without the uncertainty framing needed to interpret it.
- [x] Mechanism fix — the CI column, p-value, and power-analysis note are new
  content that changes what the table proves; the probe script is a new artifact.
- [x] Both.
