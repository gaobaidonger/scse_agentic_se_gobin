import json
from pathlib import Path

from planner_agent import run_planner


BASE_DIR = Path(__file__).resolve().parent

REQUIREMENTS_FILE = BASE_DIR / "artifacts" / "requirements.json"
PLAN_FILE = BASE_DIR / "artifacts" / "plan.json"


def main():
    with open(REQUIREMENTS_FILE, "r", encoding="utf-8") as file:
        requirements = json.load(file)

    plan = run_planner(requirements)

    PLAN_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(PLAN_FILE, "w", encoding="utf-8") as file:
        json.dump(
            plan,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("Navigation plan generated successfully.")
    print(f"Saved to: {PLAN_FILE}")


if __name__ == "__main__":
    main()