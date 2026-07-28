---
name: career-tool-engineer
description: Implement and maintain Role 2 tool contracts for the Day 3 Chatbot vs ReAct Agent lab when the selected topic is Chatbot Dinh Huong Su Nghiep / Career Guidance Chatbot. Use for editing src/tools.py, defining deterministic career guidance tools, documenting schemas, handling tool errors safely, and registering AVAILABLE_TOOLS for ReAct.
---

# Career Tool Engineer

## Scope

Act as Role 2 Tool Engineer for "Chatbot Dinh Huong Su Nghiep".

Own this file:

- `src/tools.py`

Read but do not casually edit:

- `config/test_cases.json` to align tool names with expected behavior.
- `src/prompts.py` to ensure prompt tool descriptions match the registry.
- `src/app.py` to confirm parser/executor expectations.

## Common Code Rules

Apply these rules when editing `src/tools.py`:

- Prefer clear, inspectable Python over clever abstractions.
- Keep the implementation deterministic and offline-friendly unless the user explicitly asks for a live API.
- Do not leave weather, flight, or unrelated demo tools in the final career guidance tool registry.
- Return strings from tools; use valid JSON strings when returning structured multi-field data.
- Handle invalid business inputs with `LOI:` or `CANH_BAO:` strings instead of uncaught exceptions.
- Keep side effects out of tools. Tools should read local sample data and return recommendations, not write files or call external services.
- Do not make absolute career claims such as guaranteed job, guaranteed salary, guaranteed admission, diagnosis, or `100% phu hop`.
- Keep `AVAILABLE_TOOLS`, prompt tool descriptions, app parser expectations, and test case expected behavior in sync.
- Do not commit `.env`, API keys, tokens, generated cache, or `__pycache__`.
## Tool Design Rules

Build deterministic, offline-friendly tools. The lab should run without live APIs unless the user explicitly adds one.

Each tool must:

- have a clear docstring with purpose, input schema, output schema, error behavior, side effects, and example;
- return a string, preferably compact JSON text for structured output;
- catch business-level errors by returning `LOI: ...` instead of raising uncaught exceptions;
- avoid making unsafe claims about guaranteed job outcomes, salary certainty, admission, medical or psychological diagnosis;
- be registered in `AVAILABLE_TOOLS` with the exact name the ReAct prompt will use.

Do not keep weather or flight tools unless the user asks to preserve demo examples. Replace them with career-domain tools.

## Recommended Tool Set

Use this minimum set for the career chatbot:

- `match_careers(interests: str, strengths: str = "", constraints: str = "") -> str`
  - Purpose: rank career options from user interests and strengths.
  - Output: JSON string with `careers`, each containing `name`, `fit_reason`, `watch_out`, and `confidence`.
- `get_career_profile(career_name: str) -> str`
  - Purpose: retrieve deterministic career profile data.
  - Output: JSON string with `career`, `tasks`, `skills`, `learning_paths`, `portfolio_ideas`, and `risk_notes`.
- `recommend_learning_path(target_career: str, current_skills: str, duration_weeks: int = 8) -> str`
  - Purpose: produce a bounded roadmap from current skills to target career.
  - Output: JSON string with `target_career`, `duration_weeks`, `skill_gaps`, `weekly_plan`, and `next_action`.

Optionally add:

- `compare_careers(career_a: str, career_b: str, user_priority: str = "") -> str`
- `assess_skill_gap(target_career: str, current_skills: str) -> str`

Keep the number of tools small enough that Role 3 can describe them clearly in the prompt.

## Data Model

Use a local dictionary for common career groups. Include enough data to support the 5 test cases:

- Data Analyst
- Software Engineer
- UX/UI Designer
- Digital Marketer
- AI Engineer
- Business Analyst
- Doctor or Healthcare role only as a guarded example with caution notes

Each career entry should include:

- `tasks`: 2-4 realistic tasks;
- `skills`: technical and soft skills;
- `good_for`: interests or strengths that fit;
- `watch_out`: constraints or mismatches;
- `learning_paths`: course or practice themes;
- `portfolio_ideas`: 1-3 beginner-friendly projects.

Use Vietnamese user-facing strings when returning results.

## Error Semantics

Return explicit errors for:

- empty or missing required input;
- unsupported career name;
- contradictory or unsafe request;
- invalid duration such as `0`, negative numbers, or very long plans.

Examples:

```text
LOI: Chua co du thong tin ve so thich hoac diem manh de goi y nghe nghiep.
LOI: Khong tim thay ho so nghe 'Phi cong vu tru' trong bo du lieu mau.
CANH_BAO: Dau vao co mau thuan; can hoi them truoc khi ket luan.
```

These strings are Observations for the agent. They should guide recovery, clarification, or safe fallback.

## Registration Contract

At the bottom of `src/tools.py`, maintain:

```python
AVAILABLE_TOOLS = {
    "match_careers": match_careers,
    "get_career_profile": get_career_profile,
    "recommend_learning_path": recommend_learning_path,
}
```

If adding another tool, update:

- the docstring;
- `AVAILABLE_TOOLS`;
- Role 3 prompt tool list;
- Role 1 expected behavior in test cases if that tool is part of a required scenario.

## Manual Checks

After editing, run or ask Role 4 to run:

```bash
python -m py_compile src/tools.py
python src/tools.py
```

If `src/tools.py` has no `__main__` block, test with a short Python call from the repo root. Verify:

- all registered functions are callable;
- malformed inputs return strings, not crashes;
- tool outputs include enough evidence for the final answer.

## Completion Checklist

Finish only when:

- `src/tools.py` no longer centers on weather/flights for this project.
- Tool names match `config/test_cases.json` and `src/prompts.py`.
- Every tool has a useful docstring and safe error return.
- `AVAILABLE_TOOLS` contains all intended tools and no stale domain tools.
- At least one tool supports one-step ReAct and one scenario supports two-step ReAct.
