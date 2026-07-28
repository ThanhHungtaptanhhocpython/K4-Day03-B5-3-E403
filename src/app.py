"""
Core app for Lab 03 - milestone 2 baseline wiring.

Role 4 responsibility in this milestone: load test cases, connect
run_baseline_chatbot(), and run the baseline chatbot without tools.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

SRC_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SRC_DIR.parent
sys.path.append(str(SRC_DIR))

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Mốc 2 chỉ nối baseline prompt với LLM provider, không import hoặc gọi tool.
from prompts import CHATBOT_BASELINE_PROMPT
from providers import get_llm_provider

load_dotenv()


def load_test_cases() -> list[dict[str, Any]]:
    """Load Role 1 test cases from config/test_cases.json."""
    config_path = PROJECT_ROOT / "config" / "test_cases.json"
    with config_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError("config/test_cases.json must contain a list of test cases.")
    return data


def run_baseline_chatbot(user_query: str, provider) -> str:
    """
    Run the baseline chatbot with zero tool access.

    The baseline path only calls provider.generate() with CHATBOT_BASELINE_PROMPT.
    It does not import, inspect, or execute AVAILABLE_TOOLS.
    """
    return provider.generate(user_query, system_prompt=CHATBOT_BASELINE_PROMPT)


def run_baseline_suite(provider, test_cases: list[dict[str, Any]]) -> None:
    """Run baseline responses for every configured test case."""
    for test_case in test_cases:
        case_id = test_case.get("id", "?")
        category = test_case.get("category", "unknown")
        question = test_case.get("question", "")
        expected = test_case.get("expected_behavior", "")

        print(f"=== TEST CASE {case_id} ===")
        print(f"Category: {category}")
        print(f"Question: {question}")
        print("[Expected Behavior]")
        print(expected)
        print("[Baseline]")
        print(run_baseline_chatbot(question, provider))
        print()


def main() -> None:
    print("==================================================")
    print("LAB 03 - CHATBOT VS REACT AGENT")
    print("Moc 2: Baseline Chatbot")
    print("==================================================")

    provider = get_llm_provider()
    model_name = getattr(provider, "model_name", "Offline Mock Mode")
    print(f"Provider: {provider.__class__.__name__} (Model: {model_name})")

    test_cases = load_test_cases()
    print(f"Loaded {len(test_cases)} test cases from config/test_cases.json")
    print("Baseline mode: no tools are imported or executed.\n")

    run_baseline_suite(provider, test_cases)


if __name__ == "__main__":
    main()
