# Knowledge Gap Formulation for Compounding — Week 12

**TRP1 / FDE Programme — Week 12**
**Trainee:** Atnabon Deressa
**Week of:** 2026-05-04 → 2026-05-10
**Final submission:** Saturday 2026-05-10, 21:00 UTC

---

## What this week is

Weeks 0–11 made me ship systems. Week 12 makes me **understand** them. The
deliverable is pedagogical: each day I find one real gap in my understanding
of an engineering or scientific mechanism that underlies the systems I built,
my partner finds another, we sharpen each other's questions on a morning call,
research and write each other's explainers during the day, critique on an
evening call, and ship a blog post + tweet thread under our own identity.

Each closed gap pays back into a concrete edit to my **Week 10 Conversion
Engine** or **Week 11 Sales-Eval-Bench** portfolio.

By Saturday 21:00 UTC:

- 5 sharpened questions I asked
- 5 explainer blog posts I wrote for partners (600–1,000 words each)
- 5 tweet threads I shipped (4–6 tweets each)
- 5 grounding commits to Weeks 10/11 work
- `synthesis.md` (1,500 words) covering all 10 gaps closed
- `canonical_list.md` of papers, tools, patterns I now stand behind
- `portfolio_update.md` written for an FDE hiring manager

## Grounding portfolio (Weeks 10 + 11)

These are the artifacts every gap-closure edit must trace back to.

| Week | Project | Path | Load-bearing artifacts |
|---|---|---|---|
| 10 | Conversion Engine | [`../conversion-engine/`](../conversion-engine/) | Tone-preservation classifier, bench-gated commitments, ICP classifier with abstain, τ²-Bench retail evaluator |
| 11 | Tenacious-Bench v0.1 | [`../sales-eval-bench/`](../sales-eval-bench/) | `evaluator/scoring_evaluator.py`, SimPO-trained Qwen2.5-1.5B LoRA judge, datasheet, methodology, ablations |

Older weeks remain in scope as secondary grounding when a topic touches them:
[`../oracle-forge/`](../oracle-forge/) (Weeks 8–9, DAB benchmark),
[`../trp1-chimera/`](../trp1-chimera/), [`../The-Ledger/`](../The-Ledger/),
[`../Legacy-Code-Cartographer /`](../Legacy-Code-Cartographer%20/),
[`../automaton-auditor/`](../automaton-auditor/), [`../Roo-Code/`](../Roo-Code/).

## Repo layout

```
knowledge-gap-formulation/
├── README.md                       (this file)
├── _templates/                     (templates for the daily deliverable set)
│   ├── question.md
│   ├── morning_call_summary.md
│   ├── explainer.md
│   ├── thread.md
│   ├── evening_call_summary.md
│   ├── signoff.md
│   ├── grounding_commit.md
│   └── sources.md
├── pair_DAY_1/                     (Mon — Inference-time mechanics, paired with Efrate)
├── pair_DAY_2/                     (Tue — TBD by cohort vote)
├── pair_DAY_3/                     (Wed — TBD by cohort vote)
├── pair_DAY_4/                     (Thu — TBD by cohort vote)
├── pair_DAY_5/                     (Fri — TBD by cohort vote)
├── artifacts/                      (published blog + thread links, screenshots)
├── canonical/                      (raw notes, downloaded papers, code experiments)
├── synthesis.md                    (1,500-word week synthesis, populated Sat)
├── canonical_list.md               (annotated reading list, populated Sat)
└── portfolio_update.md             (one-page hiring-manager summary, populated Sat)
```

## Daily deliverable set (per `pair_DAY_N/`)

Each day folder contains the full eight-file set the brief mandates, in this
order of production:

1. `question.md` — my final sharpened question, with the named connection to a Week 10/11 artifact.
2. `morning_call_summary.md` — 3–5 sentences on what was ambiguous and how the question sharpened.
3. `explainer.md` — the 600–1,000 word post I wrote for **my partner's** question, post evening-call revision.
4. `thread.md` — 4–6 tweet thread, post-revision.
5. `evening_call_summary.md` — 3–5 sentences on the asker's feedback and what I revised.
6. `signoff.md` — my partner's gap-closure judgement on the explainer they received from me (closed / partial / not closed).
7. `grounding_commit.md` — pointer to the actual edit I made to my Week 10/11 work after my partner's explainer landed.
8. `sources.md` — two canonical sources cited, plus the tool/pattern I ran hands-on.

## The four-property rubric (peer + tutor vote)

Every question I commit must clear all four:

| Property | Pass condition |
|---|---|
| Diagnostic | Names a specific gap whose closure changes how I do FDE work — not Wikipedia-shaped. |
| Grounded in cohort work | Names a specific Week 10/11 artifact whose quality depends on understanding this. |
| Generalizable | Closing the gap helps many FDE engagements, not only mine. |
| Resolvable in one explainer | A thoughtful colleague can write 600–1,000 words that closes it. |

## Public-artifact quality bar

Before any blog or thread ships under my identity:

- [ ] Two canonical sources cited with links (papers > authoritative docs > second-hand summaries).
- [ ] Code or concrete demo a reader can run / inspect / verify.
- [ ] Tutor pre-publication review passed (clear or single-revision).
- [ ] Tweet thread reads standalone without clicking through.
- [ ] Asker sign-off received on the post-revision version.
- [ ] Attribution clean — every source credited, nothing fabricated.

## Topic spine (illustrative, cohort votes the actual slate)

- **Multimodal & embedding mechanics** — vision tokens, late vs early fusion, cosine-similarity geometry, RoPE/ALiBi.
- **Inference-time mechanics** — sub-800 ms voice latency, KV cache, speculative decoding, attention sinks, prefill vs decode cost.
- **Agent & tool-use internals** — function-calling at the token level, MCP capability surface, multi-turn planning failures, reasoning-trace vs final-output tokens.
- **Training & post-training mechanics** — what LoRA adapts, DPO vs SimPO vs ORPO gradients, reward-model overoptimization, instruction-following vs reasoning data.
- **Evaluation & statistics** — pass^k vs pass^1, paired bootstrap CIs, LLM-as-a-judge biases, contamination tests.
- **Production patterns** — rate limiting & backpressure, structured output / constrained decoding, prompt caching, agent observability spans.

## Daily loop (five acts, mirrors Weeks 10–11)

- **Act I — Topic & pair (morning).** Cohort vote from previous evening sets topic. Pairing published.
- **Act II — Question & morning call (morning).** Independent gap triage → 30-min real-time call → final question committed.
- **Act III — Research & drafting (midday + afternoon).** Two canonical sources, one hands-on tool/pattern, draft `explainer.md` + `thread.md`.
- **Act IV — Evening call & sign-off (late afternoon).** 45-min call → revise → asker signs off → grounding commit lands.
- **Act V — Vote & present (evening + next morning).** Questions vote, topic vote, top-three present next morning.

## Final-submission checklist (Sat 21:00 UTC)

- [ ] Five complete `pair_DAY_N/` folders.
- [ ] `synthesis.md` covers all 10 gaps (5 asked + 5 researched), surprising thing learned, canonical list contribution.
- [ ] `canonical_list.md` annotated.
- [ ] `portfolio_update.md` one page, written for an FDE hiring manager.
- [ ] Five blog post URLs in `artifacts/blog_links.md`.
- [ ] Five tweet thread URLs in `artifacts/thread_links.md`.
- [ ] All grounding commits pushed to the relevant Week 10 / Week 11 repo.

---

> Find the gap. Sharpen the question. Teach what you just learned. Edit what you already shipped.
# knowledge-gap-formulation
