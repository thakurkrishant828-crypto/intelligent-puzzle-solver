from collections import deque
import heapq
from itertools import count
from node_model import Node
from puzzle_board import GOAL_STATE, get_successors
from heuristics import HEURISTICS

MAX_EXPANSIONS = 250000


def solve_bfs(start, goal=GOAL_STATE):
    root = Node(start)
    frontier = deque([root])
    visited = {tuple(start)}
    expanded = generated = 0

    while frontier:
        current = frontier.popleft()
        if current.state == goal:
            return current.reconstruct_path(), expanded, generated
        expanded += 1
        if expanded > MAX_EXPANSIONS:
            raise RuntimeError("Search limit reached. Try A* with Manhattan Distance.")
        for action, nxt in get_successors(current.state):
            if nxt not in visited:
                visited.add(nxt)
                generated += 1
                frontier.append(Node(nxt, current, action, current.g + 1))
    return None, expanded, generated


def solve_dfs(start, goal=GOAL_STATE):
    root = Node(start)
    frontier = [root]
    visited = {tuple(start)}
    expanded = generated = 0

    while frontier:
        current = frontier.pop()
        if current.state == goal:
            return current.reconstruct_path(), expanded, generated
        expanded += 1
        if expanded > MAX_EXPANSIONS:
            raise RuntimeError("Search limit reached. Try a different algorithm.")
        # Reverse successor order so the displayed order is consistent with BFS.
        for action, nxt in reversed(get_successors(current.state)):
            if nxt not in visited:
                visited.add(nxt)
                generated += 1
                frontier.append(Node(nxt, current, action, current.g + 1))
    return None, expanded, generated


def solve_ucs(start, goal=GOAL_STATE):
    root = Node(start)
    serial = count()
    frontier = [(0, next(serial), root)]
    best_cost = {tuple(start): 0}
    expanded = generated = 0

    while frontier:
        cost, _, current = heapq.heappop(frontier)
        if cost != best_cost.get(current.state):
            continue
        if current.state == goal:
            return current.reconstruct_path(), expanded, generated
        expanded += 1
        if expanded > MAX_EXPANSIONS:
            raise RuntimeError("Search limit reached. Try A* with Manhattan Distance.")
        for action, nxt in get_successors(current.state):
            new_cost = current.g + 1
            if new_cost < best_cost.get(nxt, float("inf")):
                best_cost[nxt] = new_cost
                generated += 1
                child = Node(nxt, current, action, new_cost)
                heapq.heappush(frontier, (new_cost, next(serial), child))
    return None, expanded, generated


def solve_greedy(start, heuristic_name, goal=GOAL_STATE):
    heuristic = HEURISTICS[heuristic_name]
    root = Node(start, h=heuristic(start, goal))
    serial = count()
    frontier = [(root.h, next(serial), root)]
    visited = {tuple(start)}
    expanded = generated = 0

    while frontier:
        _, _, current = heapq.heappop(frontier)
        if current.state == goal:
            return current.reconstruct_path(), expanded, generated
        expanded += 1
        if expanded > MAX_EXPANSIONS:
            raise RuntimeError("Search limit reached. Try A* with Manhattan Distance.")
        for action, nxt in get_successors(current.state):
            if nxt not in visited:
                visited.add(nxt)
                generated += 1
                child = Node(nxt, current, action, current.g + 1,
                             heuristic(nxt, goal))
                heapq.heappush(frontier, (child.h, next(serial), child))
    return None, expanded, generated


def solve_astar(start, heuristic_name, goal=GOAL_STATE):
    heuristic = HEURISTICS[heuristic_name]
    root = Node(start, h=heuristic(start, goal))
    serial = count()
    frontier = [(root.f, root.h, next(serial), root)]
    best_cost = {tuple(start): 0}
    expanded = generated = 0

    while frontier:
        _, _, _, current = heapq.heappop(frontier)
        if current.g != best_cost.get(current.state):
            continue
        if current.state == goal:
            return current.reconstruct_path(), expanded, generated
        expanded += 1
        if expanded > MAX_EXPANSIONS:
            raise RuntimeError("Search limit reached. Try an easier starting board.")
        for action, nxt in get_successors(current.state):
            new_cost = current.g + 1
            if new_cost < best_cost.get(nxt, float("inf")):
                best_cost[nxt] = new_cost
                generated += 1
                child = Node(nxt, current, action, new_cost,
                             heuristic(nxt, goal))
                heapq.heappush(frontier,
                               (child.f, child.h, next(serial), child))
    return None, expanded, generated


def solve(start, algorithm, heuristic_name):
    if algorithm == "BFS":
        return solve_bfs(start)
    if algorithm == "DFS":
        return solve_dfs(start)
    if algorithm == "UCS":
        return solve_ucs(start)
    if algorithm == "GREEDY":
        return solve_greedy(start, heuristic_name)
    if algorithm == "ASTAR":
        return solve_astar(start, heuristic_name)
    raise ValueError("Unknown search algorithm.")
