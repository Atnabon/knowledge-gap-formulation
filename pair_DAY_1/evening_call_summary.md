# Evening Call Summary — Day 1

**Date:** 2026-05-04
**Pair:** Atnabon Deressa ↔ Efrate
**Topic:** Inference-time mechanics
**Duration:** 47 minutes
**Author:** Atnabon Deressa
**Confirmed by:** Efrate

---

Efrate's feedback on the explainer Atnabon wrote for her was that the
"load-bearing mechanism" paragraph asserted the byte-for-byte tokenized-
prefix invariant before grounding why *tokenized* (not character) is the
right unit; Atnabon revised by adding a sentence on tokenizer drift as
the silent invalidation source. Efrate also flagged that the connect-
the-dots paragraph on cache-locality across providers conflated
"per-API-key" with "per-organization" — Atnabon split them and added the
TTL nuance. On the explainer Atnabon received from Efrate (prefill /
decode split), Atnabon pushed back that the prefill-cost paragraph
under-explained why decode gets *no* cache benefit; Efrate revised by
naming explicitly that decode writes new KV pairs every step (vs prefill
which only reads), which closed the gap. Sign-off was first-pass on
both sides.
