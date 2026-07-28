"""
Core app for Lab 03 - milestone 2 baseline wiring.

Role 4 responsibility in this milestone: load test cases, connect
run_baseline_chatbot(), and run the baseline chatbot without tools.
"""

from __future__ import annotations

import json
import os
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

# Import các thành phần từ file của Role 2, Role 3 & Multi-Provider Adapter
from tools import AVAILABLE_TOOLS
from prompts import CHATBOT_BASELINE_PROMPT, MAX_ITERATIONS

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
    
def execute_registered_tool(tool_name: str, args: dict):
    """Chỉ thực thi tool có trong AVAILABLE_TOOLS, không tự tạo tool mới."""
    if tool_name not in AVAILABLE_TOOLS:
        return f"LỖI: Tool '{tool_name}' không tồn tại trong AVAILABLE_TOOLS."

    try:
        return AVAILABLE_TOOLS[tool_name](**args)
    except NotImplementedError:
        return f"LỖI: Tool '{tool_name}' mới có SPEC và chưa được implement."
    except TypeError as exc:
        return f"LỖI: Tham số không hợp lệ cho tool '{tool_name}': {exc}"
    except Exception as exc:
        return f"LỖI: Tool '{tool_name}' thất bại an toàn: {exc}"


def run_react_agent(user_query: str, provider):
    """
    Dựng vòng lặp ReAct Agent (Thought -> Action -> Observation) có Guardrails.
    """
    print(f"\n🤖 [REACT AGENT] Câu hỏi: {user_query}")
    step = 0
    conversation = user_query
    
    while step < MAX_ITERATIONS:
        step += 1
        print(f"\n--- 🔄 Vòng lặp ReAct (Step {step}/{MAX_ITERATIONS}) ---")
        
        # Dự án hiện chỉ có một system prompt dùng chung cho cả hai luồng.
        response = provider.generate(
            conversation,
            system_prompt=CHATBOT_BASELINE_PROMPT,
        )
        print(f"🤖 Model response:\n{response}")

        if "Final Answer:" in response:
            break

        # Baseline provider có thể không sinh Action. Khi đó dừng an toàn.
        action_line = next(
            (line.strip() for line in response.splitlines()
             if line.strip().startswith("Action:")),
            None,
        )
        if not action_line:
            print("🛡️ SAFE FALLBACK: Không phát hiện Action hợp lệ, dừng agent.")
            break

        # App chỉ thực thi action đã được parser/adapter cung cấp.
        # Chưa tự suy đoán tham số từ câu trả lời của model.
        print(f"🛡️ SAFE FALLBACK: Chưa có parser Action an toàn: {action_line}")
        break

    else:
        print(f"🛡️ GUARDRAIL TRIGGERED: Đã đạt giới hạn tối đa {MAX_ITERATIONS} bước.")
    


if __name__ == "__main__":
    main()
