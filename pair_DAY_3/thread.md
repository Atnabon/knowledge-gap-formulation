# Tweet thread — Day 3

**Platform:** X (mirror to LinkedIn)
**Length:** 6 tweets
**Standalone test:** A reader who never clicks through still leaves with the mechanism (Q+V LoRA = routing; FFN LoRA = transformation; suppression and generation are not the same problem and Q+V cannot solve both).
**Status:** Post async-call draft

---

**1/** Most LoRA recipes ship with `target_modules=["q_proj","v_proj"]` as the default. If your fine-tune successfully *suppresses* a banned pattern but cannot *generate* a required pattern, that is not a data bug — it is a target-module bug. Here is the mechanism. 🧵

**2/** A transformer block has two compute regions: **attention** (Q/K/V/O) and **FFN**. Attention does **information routing** — it decides which tokens get attended to and what values flow forward. The FFN does **information transformation** — per-token computation that composes the actual next-token output.

**3/** **Suppression is a routing problem.** Q updates change what the model looks for; V updates change what flows forward when an attention match fires. Q+V are sufficient to learn "down-weight banned-pattern triggers and dampen their contribution to the residual stream." regex_negative passes.

**4/** **Generation is a transformation problem.** Producing a specific required phrase like "curious whether" needs the FFN to learn a key-value mapping (Geva et al. 2021) from residual context to that exact phrase. Q+V cannot teach the FFN this. The Q+V-only adapter is mechanistically incapable. regex_positive fails.

**5/** Hu et al. 2021 (original LoRA) recommended Q+V as a default — but their benchmarks were classification/ranking, the routing-flavored tasks. Liu et al. 2024 (DoRA, §4.3) re-ran the ablation on generative tasks and showed FFN targeting materially helps. The default recommendation was scoped, not universal.

**6/** Practical fix for any LoRA fine-tune where suppression works but generation fails: add `gate_proj`, `up_proj`, `down_proj` to target_modules. Keep your existing rank first; re-evaluate rank only if FFN-targeted training plateaus. Full write-up: <link to blog post>
