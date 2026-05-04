# Portfolio Update — How Week 12 Improved Weeks 10 & 11

**Trainee:** Atnabon Deressa
**Audience:** an FDE hiring manager evaluating the portfolio end-to-end
**Length target:** one page (≈ 600 words)
**Submitted:** 2026-05-10 (Sat 21:00 UTC)

> _Filled in across Saturday, after all five grounding commits have landed.
> Below is the load-bearing structure plus the prompts I will answer for
> each section._

---

## Headline

_(One sentence. The shift. Example shape: "After Week 12 my Week 10
Conversion Engine and Week 11 Tenacious-Bench portfolio defend the
engineering choices they make under questioning — five wording or
mechanism fixes against five real gaps, each grounded in primary sources
and verifiable code.")_

## The five edits

| # | Day topic | Artifact edited | Class of fix | What changed in plain English |
|---|---|---|---|---|
| 1 | Inference-time mechanics | `sales-eval-bench/cost_log.md` + `methodology.md` + `evaluator/scoring_evaluator.py` | mechanism + wording | Cost log now records prefill / decode / cached-input split per call; methodology's defence of rubric-in-prompt cites measured cache-hit rate; evaluator captures `usage.prompt_tokens_details.cached_tokens` so future audits never re-derive the split. |
| 2 | _<topic>_ | _<artifact>_ | _<wording / mechanism / both>_ | _<one line>_ |
| 3 | _<topic>_ | _<artifact>_ | _<…>_ | _<…>_ |
| 4 | _<topic>_ | _<artifact>_ | _<…>_ | _<…>_ |
| 5 | _<topic>_ | _<artifact>_ | _<…>_ | _<…>_ |

## What this collectively means for the portfolio

_(One paragraph, ≈ 150 words. Not "five independent fixes." A coherent
shift. Examples of the shape this should take:_

> "The five edits move the portfolio from one that quotes calibrated
> numbers to one that exposes the diagnostics underneath those numbers.
> Every quoted statistic in the audit memo now has a defended construct
> definition and a measured uncertainty; every engineering choice in the
> agent code now has a one-paragraph rationale grounded in a canonical
> source. The portfolio reads as if it were written by someone who can
> defend each line, because by Saturday it is."_

## What an interviewer can do with this

- **Open `audit_memo.md` and ask "why κ?"** — the memo answers in one paragraph with the length-stratified table, names the slope, and points to the canonical source for paired-bootstrap CIs.
- **Open `methodology.md` and ask "why SimPO over DPO?"** — _(Day 3 grounding commit if SimPO/DPO came up; otherwise replace.)_
- **Open `cost_log.md` and ask "why is decode the dominant cost here?"** — _(Day 2/3 grounding commit on prefill-vs-decode if it came up.)_
- _(... one bullet per closed gap.)_

Each of these now resolves in &lt; 60 seconds with a defensible answer.

## Public artifacts

- **5 blog posts:** see [`artifacts/blog_links.md`](artifacts/blog_links.md).
- **5 tweet threads:** see [`artifacts/thread_links.md`](artifacts/thread_links.md).
- **Tutor pre-publication review:** all five passed — see `artifacts/tutor_signoff.md` for the chain.

## What the next FDE engagement will look like

_(One paragraph, ≈ 100 words. The compounding the brief names by name.
Concretely: which class of question do I now spot inside an existing
codebase that I could not have spotted before this week, and what is the
five-minute audit I would run on a new client codebase as a result?)_

---

> The trajectory across Weeks 10, 11, and 12 is the cumulative diagnostic.
> A trainee who shipped a system in Week 10, built a benchmark and trained
> an adapter in Week 11, and can explain what they did with depth and
> teach others in Week 12 has the FDE-grade portfolio the program is
> designed to produce.
