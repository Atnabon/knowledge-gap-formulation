"""
Day 3 — LoRA target-module ablation probe for Yohannes's Tenacious-Bench judge.

Demonstrates the routing-vs-transformation mechanism: Q+V-only LoRA can
learn suppression (regex_negative passes) but not generation of required
phrases (regex_positive fails). Adding FFN targets unlocks generation.

Setup:
    pip install peft transformers accelerate
    # Yohannes's existing training pipeline; this probe just changes
    # target_modules and re-runs the 3 residual SOC failure prompts.

What it measures:
    For each of the two LoRA configurations (Q+V only vs Q+V+FFN),
    re-run the 3 residual SOC failure prompts and report:
    - regex_negative pass rate (suppression — should be 3/3 in both)
    - regex_positive pass rate (generation — predicted 0/3 vs 2-3/3)

Predicted outcome (from the routing/transformation mechanism in the
Day 3 explainer):

    Config                 regex_negative     regex_positive
    Q+V only (current)     3/3 PASS           0/3 PASS  (mode collapse to "I noticed...")
    Q+V+FFN (proposed)     3/3 PASS           2-3/3 PASS  (FFN composes hedged phrases)
"""

import json
import re
from pathlib import Path

from peft import LoraConfig, get_peft_model, TaskType
from transformers import AutoModelForCausalLM, AutoTokenizer

BASE_MODEL = "Qwen/Qwen2.5-1.5B-Instruct"
TRAINING_DATA = Path("sales-eval-bench/training/training_data.jsonl")
HELDOUT_FAILURES = Path("sales-eval-bench/ablations/held_out_traces.jsonl")

REGEX_POSITIVE = re.compile(
    r"curious whether|if your team|haven't seen|we saw only", re.IGNORECASE
)
REGEX_NEGATIVE = re.compile(
    r"we'?ll deliver|this week|we can deploy|guaranteed", re.IGNORECASE
)

ATTN_ONLY = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM,
)

ATTN_PLUS_FFN = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj", "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM,
)


def load_residual_soc_failures() -> list[dict]:
    """Load the 3 residual SOC failure prompts from held_out_traces.jsonl."""
    traces = [json.loads(line) for line in HELDOUT_FAILURES.read_text().splitlines()]
    return [t for t in traces if t.get("dimension") == "SOC" and t.get("status") == "FAIL"]


def evaluate_config(config: LoraConfig, label: str, prompts: list[dict]) -> dict:
    """Train a fresh adapter under `config`, re-run the 3 prompts, score."""
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    base = AutoModelForCausalLM.from_pretrained(BASE_MODEL, device_map="auto")
    model = get_peft_model(base, config)

    # Yohannes's training loop runs here on TRAINING_DATA.
    # Omitted for brevity — call train_lora_judge(model, TRAINING_DATA).

    pos_pass = 0
    neg_pass = 0
    for trace in prompts:
        inputs = tokenizer(trace["prompt"], return_tensors="pt").to(model.device)
        out = model.generate(**inputs, max_new_tokens=120, temperature=0.0)
        text = tokenizer.decode(out[0], skip_special_tokens=True)
        if REGEX_POSITIVE.search(text):
            pos_pass += 1
        if not REGEX_NEGATIVE.search(text):
            neg_pass += 1

    return {
        "config": label,
        "regex_negative_pass": f"{neg_pass}/{len(prompts)}",
        "regex_positive_pass": f"{pos_pass}/{len(prompts)}",
    }


def main() -> None:
    prompts = load_residual_soc_failures()
    assert len(prompts) == 3, f"expected 3 SOC failures, got {len(prompts)}"

    for cfg, label in [(ATTN_ONLY, "Q+V only"), (ATTN_PLUS_FFN, "Q+V + FFN")]:
        result = evaluate_config(cfg, label, prompts)
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
