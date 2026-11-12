
"""Flask application for the Intelligent Puzzle Solver."""

import os
import sys
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

# Project folder paths
BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BACKEND_DIR.parent
FRONTEND_DIR = PROJECT_DIR / "frontend"

# Make backend modules available to Python and WSGI hosts
backend_path = str(BACKEND_DIR)
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from puzzle_board import (
    validate_state,
    is_solvable,
    count_inversions
)
from profiler import run_profile

app = Flask(
    __name__,
    static_folder=str(FRONTEND_DIR),
    static_url_path=""
)

ALLOWED_ALGORITHMS = {
    "BFS", "DFS", "UCS", "GREEDY", "ASTAR"
}

ALLOWED_HEURISTICS = {
    "misplaced", "manhattan", "linear_conflict"
}


@app.get("/")
def home():
    """Serve the frontend."""
    index_file = FRONTEND_DIR / "index.html"

    if not index_file.is_file():
        app.logger.error("Frontend index.html not found")
        return jsonify({
            "error": "Frontend files are missing."
        }), 500

    return send_from_directory(
        str(FRONTEND_DIR),
        "index.html"
    )


@app.get("/api/health")
def health():
    """Check whether the API is running."""
    return jsonify({
        "status": "ok",
        "message": "Puzzle Solver API is running"
    })


@app.post("/api/solve")
def solve_puzzle():
    """Validate and solve the submitted puzzle."""

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body must be valid JSON."
        }), 400

    state = data.get("board")
    algorithm = str(
        data.get("algorithm", "ASTAR")
    ).strip().upper()

    heuristic = str(
        data.get("heuristic", "manhattan")
    ).strip().lower()

    valid, message = validate_state(state)

    if not valid:
        return jsonify({"error": message}), 400

    if algorithm not in ALLOWED_ALGORITHMS:
        return jsonify({
            "error": "Invalid algorithm selected."
        }), 400

    if heuristic not in ALLOWED_HEURISTICS:
        return jsonify({
            "error": "Invalid heuristic selected."
        }), 400

    board = tuple(state)
    inversions = count_inversions(board)

    if not is_solvable(board):
        return jsonify({
            "error": "This board is not solvable.",
            "inversions": inversions
        }), 400

    try:
        result = run_profile(
            board,
            algorithm,
            heuristic
        )

        return jsonify({
            "algorithm": algorithm,
            "heuristic": heuristic,
            "initial_board": list(board),
            "inversions": inversions,
            **result
        })

    except RuntimeError as error:
        return jsonify({
            "error": str(error)
        }), 422

    except Exception:
        app.logger.exception(
            "Unexpected error while solving puzzle"
        )

        return jsonify({
            "error": (
                "The solver encountered an unexpected error. "
                "Check the server logs."
            )
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
