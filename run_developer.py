import json
from pathlib import Path

from developer_agent import run_developer


BASE_DIR = Path(__file__).resolve().parent

PLAN_FILE = BASE_DIR / "artifacts" / "plan.json"
OUTPUT_FILE = BASE_DIR / "generated" / "navigation_logic.py"


def main():
    with open(PLAN_FILE, "r", encoding="utf-8") as file:
        plan = json.load(file)

    print(
        "Currently, Ollama (qwen3:8b) is being invoked "
        "to generate the code...",
        flush=True
    )

    code = run_developer(plan)

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write(code)
        file.write("\n")

    print("Navigation code generated successfully.")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()