from generated.navigation_logic import decide_next_move


VALID_ACTIONS = {
    "FORWARD",
    "LEFT",
    "RIGHT",
    "STOP"
}


def expected_move(state):
    safe_actions = []

    if not state["front_blocked"]:
        safe_actions.append("FORWARD")

    if not state["left_blocked"]:
        safe_actions.append("LEFT")

    if not state["right_blocked"]:
        safe_actions.append("RIGHT")

    if not safe_actions:
        return "STOP"

    if state["goal_ahead"] and "FORWARD" in safe_actions:
        return "FORWARD"

    if state["goal_on_left"] and "LEFT" in safe_actions:
        return "LEFT"

    if state["goal_on_right"] and "RIGHT" in safe_actions:
        return "RIGHT"

    return safe_actions[0]


def create_test_cases():
    cases = []

    goals = [
        ("goal_ahead", "FORWARD"),
        ("goal_on_left", "LEFT"),
        ("goal_on_right", "RIGHT")
    ]

    for goal_key, _ in goals:

        for front_blocked in [False, True]:
            for left_blocked in [False, True]:
                for right_blocked in [False, True]:

                    state = {
                        "goal_ahead": False,
                        "goal_on_left": False,
                        "goal_on_right": False,
                        "front_blocked": front_blocked,
                        "left_blocked": left_blocked,
                        "right_blocked": right_blocked
                    }

                    state[goal_key] = True

                    cases.append(
                        (
                            state,
                            expected_move(state)
                        )
                    )

    return cases


def test_all_navigation_states():
    test_cases = create_test_cases()

    assert len(test_cases) == 24

    for number, (state, expected) in enumerate(
        test_cases,
        start=1
    ):
        result = decide_next_move(state)

        assert result in VALID_ACTIONS, (
            f"Test {number}: invalid action {result}"
        )

        assert result == expected, (
            f"Test {number} failed.\n"
            f"State: {state}\n"
            f"Expected: {expected}\n"
            f"Got: {result}"
        )

        print(
            f"Test {number:02d}: "
            f"expected={expected}, "
            f"got={result} -> PASSED"
        )


if __name__ == "__main__":
    test_all_navigation_states()

    print("\nAll navigation tests passed.")