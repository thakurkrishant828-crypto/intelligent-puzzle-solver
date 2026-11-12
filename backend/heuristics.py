from puzzle_board import GOAL_STATE

TARGETS = {tile: divmod(index, 3) for index, tile in enumerate(GOAL_STATE) if tile}


def misplaced_tiles(state, goal=GOAL_STATE):
    return sum(1 for i, tile in enumerate(state) if tile != 0 and tile != goal[i])


def manhattan_distance(state, goal=GOAL_STATE):
    distance = 0
    targets = {tile: divmod(index, 3) for index, tile in enumerate(goal) if tile}
    for index, tile in enumerate(state):
        if tile:
            row, col = divmod(index, 3)
            target_row, target_col = targets[tile]
            distance += abs(row - target_row) + abs(col - target_col)
    return distance


def linear_conflict(state, goal=GOAL_STATE):
    # Manhattan distance plus 2 for each reversed pair in its goal row/column.
    distance = manhattan_distance(state, goal)
    targets = {tile: divmod(index, 3) for index, tile in enumerate(goal) if tile}
    conflicts = 0

    for row in range(3):
        tiles = [state[row * 3 + col] for col in range(3) if state[row * 3 + col]]
        for i in range(len(tiles)):
            for j in range(i + 1, len(tiles)):
                a, b = tiles[i], tiles[j]
                if targets[a][0] == row and targets[b][0] == row:
                    if targets[a][1] > targets[b][1]:
                        conflicts += 1

    for col in range(3):
        tiles = [state[row * 3 + col] for row in range(3) if state[row * 3 + col]]
        for i in range(len(tiles)):
            for j in range(i + 1, len(tiles)):
                a, b = tiles[i], tiles[j]
                if targets[a][1] == col and targets[b][1] == col:
                    if targets[a][0] > targets[b][0]:
                        conflicts += 1

    return distance + 2 * conflicts


HEURISTICS = {
    "misplaced": misplaced_tiles,
    "manhattan": manhattan_distance,
    "linear_conflict": linear_conflict
}
