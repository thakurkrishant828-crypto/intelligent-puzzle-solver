const GOAL = [1, 2, 3, 4, 5, 6, 7, 8, 0];
let board = [...GOAL];
let solution = [];
let currentStep = 0;

const boardElement = document.getElementById("board");
const playbackBoard = document.getElementById("playbackBoard");
const message = document.getElementById("message");
const results = document.getElementById("results");
const algorithmSelect = document.getElementById("algorithm");
const heuristicSelect = document.getElementById("heuristic");

function renderBoard(element, state, clickable = false) {
  element.innerHTML = "";
  state.forEach((value, index) => {
    const tile = document.createElement("button");
    tile.className = value === 0 ? "tile empty" : "tile";
    tile.textContent = value === 0 ? "" : value;
    tile.setAttribute("aria-label", value === 0 ? "Empty space" : `Tile ${value}`);
    tile.disabled = value === 0 || !clickable;
    if (clickable && value !== 0) {
      tile.addEventListener("click", () => moveTile(index));
    }
    element.appendChild(tile);
  });
}

function moveTile(index) {
  const blank = board.indexOf(0);
  const row = Math.floor(index / 3);
  const col = index % 3;
  const blankRow = Math.floor(blank / 3);
  const blankCol = blank % 3;
  if (Math.abs(row - blankRow) + Math.abs(col - blankCol) !== 1) return;
  [board[index], board[blank]] = [board[blank], board[index]];
  clearResults();
  renderBoard(boardElement, board, true);
}

function clearResults() {
  results.classList.add("hidden");
  message.textContent = "";
  solution = [];
  currentStep = 0;
}

function shuffleBoard() {
  board = [...GOAL];
  let previousBlank = -1;
  for (let i = 0; i < 35; i++) {
    const blank = board.indexOf(0);
    const row = Math.floor(blank / 3);
    const col = blank % 3;
    const options = [];
    if (row > 0) options.push(blank - 3);
    if (row < 2) options.push(blank + 3);
    if (col > 0) options.push(blank - 1);
    if (col < 2) options.push(blank + 1);
    const filtered = options.filter(x => x !== previousBlank);
    const next = filtered[Math.floor(Math.random() * filtered.length)];
    previousBlank = blank;
    [board[blank], board[next]] = [board[next], board[blank]];
  }
  clearResults();
  renderBoard(boardElement, board, true);
}

function showStep() {
  if (!solution.length) return;
  const item = solution[currentStep];
  renderBoard(playbackBoard, item.state, false);
  document.getElementById("stepLabel").textContent =
    `Step ${currentStep} of ${solution.length - 1}`;
  document.getElementById("moveLabel").textContent =
    item.move || "Initial state";
  document.getElementById("prevBtn").disabled = currentStep === 0;
  document.getElementById("nextBtn").disabled =
    currentStep === solution.length - 1;
}

async function solvePuzzle() {
  message.textContent = "";
  const solveButton = document.getElementById("solveBtn");
  solveButton.disabled = true;
  solveButton.textContent = "Solving...";

  try {
    const response = await fetch("/api/solve", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        board,
        algorithm: algorithmSelect.value,
        heuristic: heuristicSelect.value
      })
    });

    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Unable to solve puzzle.");

    solution = data.path;
    currentStep = 0;

    document.getElementById("movesMetric").textContent = data.moves;
    document.getElementById("expandedMetric").textContent = data.expanded;
    document.getElementById("generatedMetric").textContent = data.generated;
    document.getElementById("timeMetric").textContent = data.time_seconds;
    document.getElementById("memoryMetric").textContent = `${data.peak_memory_kb} KB`;
    document.getElementById("pathInfo").textContent =
      `${data.algorithm} · ${data.heuristic.replaceAll("_", " ")} · ${data.inversions} inversions`;

    results.classList.remove("hidden");
    showStep();
    results.scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (error) {
    message.textContent = error.message;
  } finally {
    solveButton.disabled = false;
    solveButton.innerHTML = 'Solve puzzle <span>→</span>';
  }
}

document.getElementById("shuffleBtn").addEventListener("click", shuffleBoard);
document.getElementById("resetBtn").addEventListener("click", () => {
  board = [...GOAL];
  clearResults();
  renderBoard(boardElement, board, true);
});
document.getElementById("solveBtn").addEventListener("click", solvePuzzle);
document.getElementById("prevBtn").addEventListener("click", () => {
  if (currentStep > 0) currentStep--;
  showStep();
});
document.getElementById("nextBtn").addEventListener("click", () => {
  if (currentStep < solution.length - 1) currentStep++;
  showStep();
});
algorithmSelect.addEventListener("change", () => {
  heuristicSelect.disabled = !["ASTAR", "GREEDY"].includes(algorithmSelect.value);
});

renderBoard(boardElement, board, true);
renderBoard(playbackBoard, GOAL, false);
document.getElementById("prevBtn").disabled = true;
document.getElementById("nextBtn").disabled = true;
heuristicSelect.disabled = false;
