# Canonical List — Atnabon Deressa's Week 12 contribution

**Trainee:** Atnabon Deressa
**Programme:** TRP1 / FDE — Week 12
**Audience:** other Forward-Deployed Engineers in the cohort and the wider community

> Annotated. Each entry says what the source actually claims, why it is
> load-bearing for FDE work, and which Week 10/11 artifact in my own
> portfolio it grounded. Items added across the week as gaps close.

---

## Papers (primary literature)

### DeepSeek-AI — *DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model* (2024)

- **Why it earns the canon slot:** Section 4 is the canonical public
  reference for the server-side context-cache architecture that became
  the industry pattern. Names the KV-state reuse mechanism precisely and
  is the load-bearing source for "what state is reused on a hit, what
  is recomputed on a miss".
- **Where I used it:** [Day 1 explainer](pair_DAY_1/explainer.md) and the
  [Day 1 grounding commit](pair_DAY_1/grounding_commit.md) on
  `sales-eval-bench/cost_log.md`.
- **Link:** <https://arxiv.org/abs/2405.04434>

### Anthropic — *Prompt caching* developer documentation (2024–2026)

- **Why it earns the canon slot:** the most explicit public description
  of the byte-for-byte tokenized-prefix invalidation rule, the discounted-
  rate pricing structure, and the cache TTL. Resolves the "narrow my
  prompt edit to the bottom" footgun that almost every long-prompt
  agent hits silently.
- **Where I used it:** [Day 1 explainer](pair_DAY_1/explainer.md).
- **Link:** <https://docs.claude.com/en/docs/build-with-claude/prompt-caching>

### _<paper from Day 2>_

_(Add as Day 2 lands.)_

### _<paper from Day 3>_

_(Add as Day 3 lands.)_

### _<paper from Day 4>_

_(Add as Day 4 lands.)_

### _<paper from Day 5>_

_(Add as Day 5 lands.)_

## Engineering tools / libraries (battle-tested in this week)

### Provider `usage` object inspection for prefill / decode / cached-input attribution

- **Why it earns the canon slot:** every OpenAI-compatible chat-completion
  endpoint exposes per-call token counts in `resp.usage`; pulling
  `prompt_tokens_details.cached_tokens` is the single highest-signal
  cost-attribution probe an FDE can run against a long-prompt system.
- **Pattern:** see [`pair_DAY_1/explainer.md`](pair_DAY_1/explainer.md) for
  the 25-line probe; ~ $0.001 per run.

### _<tool from Day 2>_

_(Add as Day 2 lands.)_

### _<tool from Day 3>_

_(Add as Day 3 lands.)_

### _<tool from Day 4>_

_(Add as Day 4 lands.)_

### _<tool from Day 5>_

_(Add as Day 5 lands.)_

## Engineering patterns (production-shaped)

### Per-call cost decomposition: `(uncached_in × $/in) + (cached_in × $/cached_in) + (out × $/out)`

- **What:** every cost-log row for a long-prompt agent should record the
  uncached-input / cached-input / output split and the resulting prefill /
  decode dollar split, not a single dollar amount.
- **Why it earns the canon slot:** without it, an FDE cannot tell whether
  a design decision (rubric-in-prompt, long system prompt, structured
  output) is defensible on cost. With it, the dependency on cache-hit
  rate is auditable from day one.
- **Reference implementation:** [`pair_DAY_1/grounding_commit.md`](pair_DAY_1/grounding_commit.md).

### _<pattern from Day 2>_

_(Add as Day 2 lands.)_

_(… and so on through Day 5.)_

---

## How to use this list

If you are an FDE who shipped a system in Weeks 10 or 11 and wrote a paragraph
you cannot fully defend, this list is a ranked surface of the canonical sources
that closed analogous gaps for me. The entries are deliberately narrow — each
one says **what the source proves**, not "interesting paper on X". The
narrower the claim, the more useful the citation.
