def navigate(front_blocked, left_blocked, right_blocked, goal_direction):
    unblocked = []
    if not front_blocked:
        unblocked.append('FORWARD')
    if not left_blocked:
        unblocked.append('LEFT')
    if not right_blocked:
        unblocked.append('RIGHT')
    if not unblocked:
        return 'STOP'
    goal_direction = goal_direction.upper()
    if goal_direction in unblocked:
        return goal_direction
    return unblocked[0] if unblocked else 'STOP'
