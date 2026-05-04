# Morning Call Summary — Day 1

**Date:** 2026-05-04
**Pair:** Atnabon Deressa ↔ Efrate
**Topic:** Inference-time mechanics
**Duration:** 28 minutes
**Author:** Atnabon Deressa
**Confirmed by:** Efrate

---

Atnabon's draft asked broadly "why is the rubric-in-prompt design defensible
on cost?", which Efrate flagged as conflating two questions: a *mechanism*
question about how providers bill prefill vs decode and a *consequence*
question about the architectural choice. We split it: the mechanism
question is what Efrate will answer; the architectural defence follows
once the mechanism is in hand. Efrate's draft asked "what is KV cache,"
which Atnabon pushed on as too broad — narrowed to "what specifically
gets *invalidated* on a prefix-cache miss vs hit, at the level a
Forward-Deployed Engineer needs to design around." Both final questions
now name a mechanism, an artifact in the asker's portfolio, and a
measurable outcome; no second mid-day call requested.
