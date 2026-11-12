GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)


def validate_state(state):
    if not isinstance(state, (list, tuple)) or len(state) != 9:
        return False, "Board must contain exactly 9 numbers."
    if any(type(x) is not int for x in state):
        return False, "Every tile must be an integer."
    if set(state) != set(range(9)):
        return False, "Board must contain each number from 0 to 8 exactly once."
    return True, ""


def count_inversions(state):
    values = [x for x in state if x != 0]
    return sum(
        1 for i in range(len(values))
        for j in range(i + 1, len(values))
        if values[i] > values[j]
    )


def is_solvable(state):
    # For a 3x3 board, an even inversion count is solvable.
    return count_inversions(state) % 2 == 0


def get_successors(state):
    result = []
    blank = state.index(0)
    row, col = divmod(blank, 3)
    moves = []

    if row > 0:
        moves.append(("UP", blank - 3))
    if row < 2:
        moves.append(("DOWN", blank + 3))
    if col > 0:
        moves.append(("LEFT", blank - 1))
    if col < 2:
        moves.append(("RIGHT", blank + 1))

    for action, target in moves:
        board = list(state)
        board[blank], board[target] = board[target], board[blank]
        result.append((action, tuple(board)))
    return result
