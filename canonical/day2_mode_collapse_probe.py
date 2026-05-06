"""
Day 2 — Mode-collapse probe for Ramlla's Conversion Engine Draft stage.

Demonstrates that prompt geometry (where enrichment data sits) drives
output diversity more than any "be more personalized" instruction.

Setup:
    pip install openai
    export OPENAI_API_KEY=<your OpenRouter key>
    export OPENAI_BASE_URL=https://openrouter.ai/api/v1

Run:
    python canonical/day2_mode_collapse_probe.py

What it measures:
    Number of unique opening 5-grams across N generations of the same
    email task, under two prompt orderings. Buried = enrichment data
    sits in the middle of the prompt between safety and format rules.
    Late = enrichment data sits at the end, just before the generation
    point. Same model, same temperature, same content — only position
    changes.
"""

from openai import OpenAI

client = OpenAI()  # picks up OPENAI_BASE_URL + OPENAI_API_KEY env vars

ENRICHMENT = (
    "Prospect: Sarah Chen, VP Engineering at Acme. Recently shipped a "
    "real-time feature flag system. Open-source contributor to two "
    "well-known Kubernetes projects."
)
COMPETITOR_GAP = (
    "Acme currently uses LaunchDarkly. Switching cost is high but our "
    "SOC 2 Type II + EU data residency story is materially stronger, "
    "and our pricing is ~ 30 % below LaunchDarkly at their volume."
)
SAFETY = (
    "Do not be too casual. Do not make hard delivery commitments. "
    "Stay professional. Avoid superlatives."
)
FORMAT = (
    "Output format: subject line, then a 3-paragraph body. "
    "Maximum 120 words total. No bullet points."
)

PROMPT_BURIED = (
    f"{SAFETY}\n\n{ENRICHMENT}\n\n{COMPETITOR_GAP}\n\n{FORMAT}\n\n"
    "Write the outreach email:"
)
PROMPT_LATE = (
    f"{SAFETY}\n\n{FORMAT}\n\n{ENRICHMENT}\n\n{COMPETITOR_GAP}\n\n"
    "Write the outreach email:"
)


def output_diversity(prompt: str, n: int = 8, temp: float = 0.9) -> tuple[int, list[str]]:
    """Generate n outputs at fixed temperature; return unique-opening count."""
    outputs = []
    for _ in range(n):
        resp = client.chat.completions.create(
            model="anthropic/claude-haiku-4.5",
            messages=[{"role": "user", "content": prompt}],
            temperature=temp,
            max_tokens=200,
        )
        outputs.append(resp.choices[0].message.content)
    unique_first_5_words = len({" ".join(o.split()[:5]) for o in outputs})
    return unique_first_5_words, outputs


def main() -> None:
    buried_unique, buried_outputs = output_diversity(PROMPT_BURIED)
    late_unique, late_outputs = output_diversity(PROMPT_LATE)

    print(f"buried (enrichment mid-prompt):  {buried_unique} /8 unique openings")
    print(f"late   (enrichment end-of-prompt): {late_unique} /8 unique openings")
    print()
    print("--- buried sample openings ---")
    for o in buried_outputs:
        print(" ", " ".join(o.split()[:8]))
    print()
    print("--- late sample openings ---")
    for o in late_outputs:
        print(" ", " ".join(o.split()[:8]))


if __name__ == "__main__":
    main()
