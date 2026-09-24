import json
from pathlib import Path

from developer_agent import run_developer


BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = (
    BASE_DIR / "artifacts" / "plan.json"
)

OUTPUT_FILE = (
    BASE_DIR / "generated" / "navigation_logic.py"
)


def test_developer_agent():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        plan = json.load(file)

    code = run_developer(plan)

    assert "def decide_next_move" in code

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write(code)
        file.write("\n")

    print("\nDeveloper output:")
    print(code)


if __name__ == "__main__":
    test_developer_agent()