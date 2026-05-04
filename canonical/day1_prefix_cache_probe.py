"""Day 1 probe — prefill / decode / cached-input attribution against an
OpenAI-compatible chat-completion endpoint.

Goal: directly verify the byte-for-byte tokenized-prefix invariant the
Day 1 explainer claims, by inspecting `usage.prompt_tokens_details.cached_tokens`
across consecutive calls with (a) a stable system prompt and (b) a
per-call-timestamped system prompt.

Run:
    OPENROUTER_API_KEY=... python day1_prefix_cache_probe.py

Cost: ≈ $0.001 total (3 calls against qwen3-next-80b-a3b at OpenRouter dev rates).

Captured output for the Day 1 submission lives in
`day1_prefix_cache_probe_results.md`.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import sys
from typing import Any

try:
    from openai import OpenAI
except ImportError:
    sys.exit(
        "openai SDK not installed. `pip install openai` (>= 1.0) and re-run."
    )


MODEL = "anthropic/claude-haiku-4.5"

# Static rubric prefix — stand-in for sales-eval-bench/tenacious_bench_v0.1
# rubric, sized to ~ 1,200 tokens to match the production system prompt.
STATIC_RUBRIC = (
    "You are a careful sales-email evaluator. Score the candidate email "
    "1 to 5 against five style markers (warmth, specificity, signal-grounding, "
    "ASK-not-ASSERT, brevity). Return a single JSON object with keys "
    "`score`, `markers`, and `notes`. Be strict; do not award benefit of "
    "the doubt. Banned phrases include 'we hope', 'we believe', 'we think' "
    "(soft hedges), and any claim that is not directly grounded in the "
    "candidate's stated signal. Banned structures include opening with the "
    "candidate's name in isolation, more than two sentences before the "
    "first concrete observation, and any closing line longer than fifteen "
    "words. Calibration: a 5/5 email is one a senior partner at a "
    "boutique consultancy would send unedited; a 3/5 is competent but "
    "generic; a 1/5 contains banned phrases or fabricated signal. "
    + "Reference style notes follow. "
    "Each email must be evaluated strictly against the style guide. "
    "Do not award partial credit for effort. "
    "The score must be justified by specific markers, not general impression. "
    "Warmth: does the opening demonstrate knowledge of the recipient? "
    "Specificity: are claims grounded in named signals from the brief? "
    "Signal-grounding: is every assertion traceable to a fact in the brief? "
    "ASK-not-ASSERT: are uncertain claims framed as questions? "
    "Brevity: is the email under 200 words with no filler sentences? \n" * 25
)


def call(
    client: OpenAI,
    system_prompt: str,
    user_message: str,
    max_tokens: int = 80,
) -> dict[str, Any]:
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": system_prompt,
                        "cache_control": {"type": "ephemeral"},  # Anthropic prefix cache
                    }
                ],
            },
            {"role": "user", "content": user_message},
        ],
        max_tokens=max_tokens,
    )
    u = resp.usage
    # OpenAI-style field
    details = getattr(u, "prompt_tokens_details", None)
    cached_oi = getattr(details, "cached_tokens", 0) if details else 0
    # Anthropic-style fields (passed through by OpenRouter)
    cache_creation = getattr(u, "cache_creation_input_tokens", 0) or 0
    cache_read = getattr(u, "cache_read_input_tokens", 0) or 0
    return {
        "input_tokens": u.prompt_tokens,
        "cache_creation_input_tokens": cache_creation,
        "cache_read_input_tokens": cache_read,
        "cached_input_tokens_oi_style": cached_oi,
        "output_tokens": u.completion_tokens,
    }


def main() -> int:
    api_key = os.environ.get("OPENROUTER_API_KEY") or os.environ.get(
        "OPENAI_API_KEY"
    )
    if not api_key:
        sys.exit(
            "Set OPENROUTER_API_KEY (or OPENAI_API_KEY) in your environment."
        )

    base_url = os.environ.get(
        "OPENAI_BASE_URL", "https://openrouter.ai/api/v1"
    )
    client = OpenAI(api_key=api_key, base_url=base_url)

    print(f"Model: {MODEL}")
    print(f"Endpoint: {base_url}\n")

    # Pass A — two calls with the same static system prompt.
    # Expect call 1: cached_input_tokens == 0 (cold).
    # Expect call 2: cached_input_tokens > 0 (warm; prefix matched).
    print("=== Pass A: stable system prompt ===")
    a1 = call(client, STATIC_RUBRIC, "Hi Sarah, just following up on our call ...")
    print("call 1 (cold):", json.dumps(a1))
    a2 = call(client, STATIC_RUBRIC, "Hi Marcus, congrats on the Series B ...")
    print("call 2 (warm):", json.dumps(a2))

    # Pass B — same payload but with a per-call timestamp PREPENDED to the
    # system prompt (before the cache_control block).
    # The first divergent token sits at byte 0, so the cache should
    # invalidate completely even though 99 %+ of the bytes are identical.
    # Expect: cache_creation_input_tokens > 0, cache_read_input_tokens == 0.
    print("\n=== Pass B: per-call timestamp prepended to system prompt ===")
    ts1 = f"# generated {dt.datetime.now(dt.timezone.utc).isoformat()}Z\n" + STATIC_RUBRIC
    b1 = call(client, ts1, "Hi Sarah, just following up on our call ...")
    print("call 1 (cold):", json.dumps(b1))
    ts2 = f"# generated {dt.datetime.now(dt.timezone.utc).isoformat()}Z\n" + STATIC_RUBRIC
    b2 = call(client, ts2, "Hi Marcus, congrats on the Series B ...")
    print("call 2 (still cold; timestamp changed):", json.dumps(b2))

    # Reporting — works for both Anthropic-style and OpenAI-style fields.
    a2_cache_read = a2.get("cache_read_input_tokens", 0) or a2.get("cached_input_tokens_oi_style", 0)
    b2_cache_read = b2.get("cache_read_input_tokens", 0) or b2.get("cached_input_tokens_oi_style", 0)
    warm_hit_rate = a2_cache_read / a2["input_tokens"] if a2["input_tokens"] else 0.0
    b2_hit_rate   = b2_cache_read / b2["input_tokens"] if b2["input_tokens"] else 0.0
    print(f"\nWarm-prefix hit rate (Pass A call 2): {warm_hit_rate:.0%}")
    print(
        "Pass B invalidation-by-first-divergent-token hit rate: "
        f"{b2_hit_rate:.0%} despite > 99% byte overlap."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
