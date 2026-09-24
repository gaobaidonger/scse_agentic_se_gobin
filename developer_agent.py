import ast
import ollama


def validate_code(code):
    if not isinstance(code, str):
        raise ValueError("Generated code must be a string.")

    if not code.strip():
        raise ValueError("Generated code must not be empty.")

    try:
        tree = ast.parse(code)
    except SyntaxError as error:
        raise ValueError(
            f"Generated code is not valid Python: {error}"
        )

    functions = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
    ]

    if not functions:
        raise ValueError(
            "Generated code must contain at least one function."
        )

    decide_functions = [
        node for node in functions
        if node.name == "decide_next_move"
    ]

    if not decide_functions:
        raise ValueError(
            "Generated code must contain decide_next_move(state)."
        )

    decide_function = decide_functions[0]

    if len(decide_function.args.args) != 1:
        raise ValueError(
            "decide_next_move must take exactly one parameter: state."
        )

    if decide_function.args.args[0].arg != "state":
        raise ValueError(
            "The parameter of decide_next_move must be named state."
        )

    return code


def run_developer(plan):
    system_prompt = """
You are a Developer Agent.

Your task is to convert a validated robot navigation plan
into working Python code.

Follow these rules strictly:

1. Return ONLY Python source code.
2. Do not include markdown.
3. Do not include code fences.
4. Do not include explanations before or after the code.
5. The generated code MUST contain this public function:

   decide_next_move(state)

6. Other helper functions may exist, but external programs
   must only need to call decide_next_move(state).

7. state is a dictionary with these boolean keys:

   goal_ahead
   goal_on_left
   goal_on_right
   front_blocked
   left_blocked
   right_blocked

8. decide_next_move(state) must return only one of:

   FORWARD
   LEFT
   RIGHT
   STOP

9. The robot must never move into a blocked direction.

10. If the direction toward the goal is unblocked,
    prefer that direction.

11. If the goal direction is blocked, choose another
    safe unblocked direction.

12. If every movement direction is blocked, return STOP.

13. When choosing an alternative safe direction,
    use this priority order:

    FORWARD
    LEFT
    RIGHT

14. Do not use external packages.

15. The generated output must be valid executable Python code.
"""

    response = ollama.Client(timeout=120).chat(
        model="qwen3:8b",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": str(plan)
            }
        ],
        think=False,
        options={
            "temperature": 0,
            "num_predict": 1024
        }
    )

    code = response["message"]["content"].strip()

    if code.startswith("```python"):
        code = code[len("```python"):]

    if code.startswith("```"):
        code = code[3:]

    if code.endswith("```"):
        code = code[:-3]

    code = code.strip()

    return validate_code(code)