import json
from pathlib import Path

from analyst_agent import run_analyst


BASE_DIR = Path(__file__).resolve().parent
BRIEF_FILE = BASE_DIR / "brief.txt"
OUTPUT_FILE = BASE_DIR / "artifacts" / "requirements.json"


def test_analyst_agent():
    with open(BRIEF_FILE, "r", encoding="utf-8") as file:
        brief = file.read()

    requirements = run_analyst(brief)

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            requirements,
            file,
            indent=4,
            ensure_ascii=False
        )

    assert isinstance(requirements, dict)
    assert "goal" in requirements
    assert "allowed_actions" in requirements
    assert "safe_stop" in requirements
    assert "avoid_obstacles" in requirements

    print("\nAnalyst output:")
    print(json.dumps(requirements, indent=4))


if __name__ == "__main__":
    test_analyst_agent()