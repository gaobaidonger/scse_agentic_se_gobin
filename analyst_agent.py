import json
import ollama


VALID_ACTIONS = {"FORWARD", "LEFT", "RIGHT", "STOP"}


def validate_requirements(requirements):
    """
    Validate the requirements returned by Qwen.
    """

    required_keys = {
        "goal",
        "allowed_actions",
        "safe_stop",
        "avoid_obstacles"
    }

    if not isinstance(requirements, dict):
        raise ValueError("Requirements must be a dictionary.")

    if set(requirements.keys()) != required_keys:
        raise ValueError(
            "Requirements must contain exactly these keys: "
            "goal, allowed_actions, safe_stop, avoid_obstacles"
        )

    if not isinstance(requirements["goal"], str):
        raise ValueError("goal must be a string.")

    if not isinstance(requirements["allowed_actions"], list):
        raise ValueError("allowed_actions must be a list.")

    if not isinstance(requirements["safe_stop"], bool):
        raise ValueError("safe_stop must be a boolean.")

    if not isinstance(requirements["avoid_obstacles"], bool):
        raise ValueError("avoid_obstacles must be a boolean.")

    for action in requirements["allowed_actions"]:
        if action not in VALID_ACTIONS:
            raise ValueError(
                f"Invalid action: {action}. "
                "Allowed actions are FORWARD, LEFT, RIGHT, STOP."
            )

    return requirements


def run_analyst(brief_text):
    """
    Send the project brief to Qwen and return validated requirements.
    """

    system_prompt = """
You are a software requirements analyst.

Your only task is to analyze the given robot navigation brief
and convert it into explicit software requirements.

Follow these rules strictly:

1. Return ONLY valid JSON.
2. Do not include markdown.
3. Do not include explanations.
4. Do not include code fences.
5. Do not output anything before or after the JSON object.
6. The JSON must contain exactly these four keys:
   - goal
   - allowed_actions
   - safe_stop
   - avoid_obstacles
7. goal must be a string.
8. allowed_actions must be a list.
9. The only valid navigation actions are:
   FORWARD
   LEFT
   RIGHT
   STOP
10. safe_stop must be a boolean.
11. avoid_obstacles must be a boolean.
12. Do not invent additional requirements.
13. Do not add additional keys.

The output must follow exactly this structure:

{
  "goal": "string",
  "allowed_actions": ["FORWARD", "LEFT", "RIGHT", "STOP"],
  "safe_stop": true,
  "avoid_obstacles": true
}
"""

    response = ollama.chat(
        model="qwen3:8b",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": brief_text
            }
        ],
        format="json",
        options={
            "temperature": 0
        }
    )

    json_text = response["message"]["content"]

    requirements = json.loads(json_text)

    validated_requirements = validate_requirements(requirements)

    return validated_requirements