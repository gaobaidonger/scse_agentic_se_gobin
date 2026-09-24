import json
import os

from analyst_agent import run_analyst


def main():
    # Read the project brief
    with open("brief.txt", "r", encoding="utf-8") as file:
        brief_text = file.read()

    requirements = run_analyst(brief_text)

    os.makedirs("artifacts", exist_ok=True)

    output_path = "artifacts/requirements.json"

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(
            requirements,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("Requirements generated successfully.")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()