"""Core app for Lab 03: baseline chatbot and guarded ReAct loop."""

from __future__ import annotations

import json
import os
import re
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

# Role 4 tích hợp prompt, provider, test cases và tool registry.
from prompts import CHATBOT_BASELINE_PROMPT, MAX_ITERATIONS, REACT_SYSTEM_PROMPT
from providers import get_llm_provider
from tools import AVAILABLE_TOOLS

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
    It does not inspect or execute AVAILABLE_TOOLS.
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


WRITE_TOOLS = {
    "save_user_profile",
    "generate_cv",
    "generate_career_roadmap",
    "save_conversation_memory",
}

ACTION_PATTERN = re.compile(r"(?m)^Action:\s*([A-Za-z_][A-Za-z0-9_]*)\s*$")
ACTION_INPUT_PATTERN = re.compile(r"(?m)^Action Input:\s*(\{.*\})\s*$")


def parse_agent_response(response: str) -> tuple[str, dict[str, Any]] | None:
    """Parse exactly one tool call emitted in the required ReAct format."""
    action_match = ACTION_PATTERN.search(response)
    input_match = ACTION_INPUT_PATTERN.search(response)
    if not action_match or not input_match:
        return None

    try:
        arguments = json.loads(input_match.group(1))
    except json.JSONDecodeError:
        return None

    if not isinstance(arguments, dict):
        return None
    return action_match.group(1), arguments


def execute_registered_tool(
    tool_name: str,
    arguments: dict[str, Any],
    confirmed_actions: set[str],
) -> dict[str, Any]:
    """Execute a registered tool and convert every failure into Observation."""
    if tool_name not in AVAILABLE_TOOLS:
        return {"ok": False, "error": f"Tool không được đăng ký: {tool_name}"}

    if tool_name in WRITE_TOOLS and tool_name not in confirmed_actions:
        return {
            "ok": False,
            "confirmation_required": True,
            "error": (
                f"Cần người dùng xác nhận rõ ràng trước khi gọi {tool_name}."
            ),
        }

    try:
        result = AVAILABLE_TOOLS[tool_name](**arguments)
        return {"ok": True, "result": result}
    except NotImplementedError:
        return {
            "ok": False,
            "error": f"Tool {tool_name} mới có spec và chưa được implement.",
        }
    except TypeError as exc:
        return {"ok": False, "error": f"Tham số tool không hợp lệ: {exc}"}
    except Exception as exc:
        return {"ok": False, "error": f"Tool thất bại an toàn: {exc}"}


def run_react_agent(
    user_query: str,
    provider,
    confirmed_actions: set[str] | None = None,
) -> str:
    """Run a guarded Thought -> Action -> Observation loop."""
    confirmed = confirmed_actions or set()
    trace = [f"Question: {user_query}"]
    previous_actions: set[tuple[str, str]] = set()

    for step in range(1, MAX_ITERATIONS + 1):
        prompt = "\n".join(trace)
        response = provider.generate(prompt, system_prompt=REACT_SYSTEM_PROMPT)
        print(f"[ReAct step {step}/{MAX_ITERATIONS}]\n{response}")
        trace.append(response)

        if "Final Answer:" in response:
            return response.split("Final Answer:", 1)[1].strip()

        parsed = parse_agent_response(response)
        if parsed is None:
            return "Không thể tiếp tục an toàn vì Action hoặc Action Input không hợp lệ."

        tool_name, arguments = parsed
        action_key = (tool_name, json.dumps(arguments, ensure_ascii=False, sort_keys=True))
        if action_key in previous_actions:
            return "Đã dừng an toàn vì Agent lặp lại cùng một Action và tham số."
        previous_actions.add(action_key)

        observation = execute_registered_tool(tool_name, arguments, confirmed)
        observation_text = json.dumps(observation, ensure_ascii=False, default=str)
        print(f"Observation: {observation_text}\n")
        trace.append(f"Observation: {observation_text}")

    return f"Đã dừng an toàn sau {MAX_ITERATIONS} vòng lặp mà chưa có Final Answer."


def run_react_suite(provider, test_cases: list[dict[str, Any]]) -> None:
    """Run ReAct Agent for every configured test case."""
    for test_case in test_cases:
        print(f"=== REACT TEST CASE {test_case.get('id', '?')} ===")
        print(run_react_agent(test_case.get("question", ""), provider))
        print()


def main() -> None:
    print("==================================================")
    print("LAB 03 - CHATBOT VS REACT AGENT")
    print("Moc 3: ReAct Agent Loop & Safeguards")
    print("==================================================")

    provider = get_llm_provider()
    model_name = getattr(provider, "model_name", "Offline Mock Mode")
    print(f"Provider: {provider.__class__.__name__} (Model: {model_name})")

    test_cases = load_test_cases()
    print(f"Loaded {len(test_cases)} test cases from config/test_cases.json")
    mode = os.getenv("APP_MODE", "compare").lower().strip()
    print(f"App mode: {mode}\n")

    if mode in {"baseline", "compare"}:
        run_baseline_suite(provider, test_cases)
    if mode in {"react", "compare"}:
        run_react_suite(provider, test_cases)
    if mode not in {"baseline", "react", "compare"}:
        raise ValueError("APP_MODE must be baseline, react, or compare.")


if __name__ == "__main__":
    main()
