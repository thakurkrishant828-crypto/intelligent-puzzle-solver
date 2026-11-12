from flask import Flask, jsonify, request, send_from_directory
from pathlib import Path
from puzzle_board import GOAL_STATE, validate_state, is_solvable, count_inversions
from profiler import run_profile

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="")


@app.get("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "message": "Puzzle Solver API is running"})


@app.post("/api/solve")
def solve_puzzle():
    data = request.get_json(silent=True) or {}
    state = data.get("board")
    algorithm = str(data.get("algorithm", "ASTAR")).upper()
    heuristic = str(data.get("heuristic", "manhattan")).lower()

    valid, message = validate_state(state)
    if not valid:
        return jsonify({"error": message}), 400

    if algorithm not in {"BFS", "DFS", "UCS", "GREEDY", "ASTAR"}:
        return jsonify({"error": "Invalid algorithm selected."}), 400

    if heuristic not in {"misplaced", "manhattan", "linear_conflict"}:
        return jsonify({"error": "Invalid heuristic selected."}), 400

    state = tuple(state)
    if not is_solvable(state):
        return jsonify({
            "error": "This board is not solvable.",
            "inversions": count_inversions(state)
        }), 400

    try:
        result = run_profile(state, algorithm, heuristic)
        return jsonify({
            "algorithm": algorithm,
            "heuristic": heuristic,
            "initial_board": list(state),
            "inversions": count_inversions(state),
            **result
        })
    except RuntimeError as error:
        return jsonify({"error": str(error)}), 422
    except Exception as error:
        app.logger.exception("Solver failed")
        return jsonify({"error": "Solver error: " + str(error)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
