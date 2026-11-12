# Intelligent Puzzle Solver – CSE276

An educational 8-Puzzle solver with an HTML/CSS/JavaScript frontend and Python Flask backend.

## Features
- Interactive 3×3 puzzle board
- BFS, DFS, UCS, Greedy Best-First Search and A*
- Misplaced Tiles, Manhattan Distance and Linear Conflict heuristics
- Solvability validation using inversion parity
- Solution playback, move count, expanded/generated nodes, runtime and peak memory
- No database or external frontend framework required

## Requirements
- Python 3.8+
- pip

## Run locally

### Windows
```powershell
cd backend
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### macOS / Linux
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## API
- `GET /api/health` – backend health check
- `POST /api/solve` – solve a board

Example request:
```json
{
  "board": [1, 2, 3, 4, 0, 6, 7, 5, 8],
  "algorithm": "ASTAR",
  "heuristic": "manhattan"
}
```

Allowed algorithms: `BFS`, `DFS`, `UCS`, `GREEDY`, `ASTAR`.

Allowed heuristics: `misplaced`, `manhattan`, `linear_conflict`.

## Project structure
```text
intelligent-puzzle-solver/
├── backend/
│   ├── app.py
│   ├── heuristics.py
│   ├── node_model.py
│   ├── profiler.py
│   ├── puzzle_board.py
│   ├── search_engines.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
└── README.md
```

## Notes
- The blank tile is represented by `0`.
- Goal state: `[1, 2, 3, 4, 5, 6, 7, 8, 0]`.
- For a 3×3 puzzle, an even inversion count is solvable.
- BFS and UCS find shortest paths for equal move costs. A* with Manhattan Distance is the recommended option for this demo.
- DFS is not guaranteed to return an optimal path.
- A search expansion limit is included to avoid very long browser requests on difficult inputs.
