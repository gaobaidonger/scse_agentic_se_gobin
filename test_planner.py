import json
from pathlib import Path

from planner_agent import run_planner


BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = (
    BASE_DIR / "artifacts" / "requirements.json"
)

OUTPUT_FILE = (
    BASE_DIR / "artifacts" / "plan.json"
)


def test_planner_agent():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        requirements = json.load(file)

    plan = run_planner(requirements)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            plan,
            file,
            indent=4,
            ensure_ascii=False
        )

    assert isinstance(plan, dict)
    assert "strategy" in plan
    assert "decisions" in plan
    assert "stop_condition" in plan

    print("\nPlanner output:")
    print(json.dumps(plan, indent=4))


if __name__ == "__main__":
    test_planner_agent()