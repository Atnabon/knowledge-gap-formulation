# Morning Call Summary — Day 3

**Date:** 2026-05-07
**Pair:** Atnabon Deressa ↔ Yohannes Dereje
**Duration:** Async (Slack DM thread, ~50 min effective interrogation across afternoon)
**Author:** Atnabon Deressa
**Confirmed by:** Yohannes Dereje

---

The call ran asynchronously over Slack — Yohannes flagged early in the
day that his battery was dying and proposed we exchange drafts in
writing, with mutual interrogation in the thread itself. His draft
question came in already well-grounded: he tied the q_proj/v_proj-only
LoRA config in `train.py:L37` directly to the 3 residual SOC failures
in `held_out_traces.jsonl`, where regex_negative passes (suppression
learned) but regex_positive fails (generative production not learned).
My push-back was on whether his draft was conflating two questions — a
*mechanism* question about what each projection matrix updates and a
*remediation* question about whether to add k_proj/o_proj/FFN — and
Yohannes confirmed he wanted the mechanism cut so the remediation drops
out of the answer rather than being asked separately. My draft was
softer: I asked vaguely "why r=16 and not r=8 or r=32?" Yohannes pushed
me to name what *kind* of capacity rank actually controls — subspace
dimensionality, update magnitude, or both — and to specify what edit in
`train.py` the answer would change. That interrogation reshaped my
question into the SVD-decomposition framing and tied it to the v0.2
expansion decision. By the end of the thread, both questions named a
mechanism, an artifact, and a measurable consequence; the two questions
are deliberately complementary — Yohannes asks *which weight matrices*
LoRA touches, I ask *how much expressive capacity per matrix* — together
covering the two main LoRA design knobs. No mid-day clarification slot
was requested; the async format meant sharpening happened in writing.
