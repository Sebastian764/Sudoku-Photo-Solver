var numSelected = null;
var tileSelected = null;

let board = [];  // Initialize board to an empty array

document.getElementById("solve").addEventListener("click", solveBoard);
document.getElementById("clear").addEventListener("click", clearBoard);

function updateTiles() {
    for (let r = 0; r < 9; r++) {
        for (let c = 0; c < 9; c++) {
            let tileId = r.toString() + "0" + c.toString();
            let tile = document.getElementById(tileId);
            tile.innerText = board[r][c] !== 0 ? board[r][c] : "";
            tile.classList.remove("tile-start");
            if (board[r][c] !== 0) {
                tile.classList.add("tile-start");
            }
        }
    }
}

function solveBoard() {
    fetch('/solve', { method: 'POST' })
        .then(() => {
            return fetch('/get_board');
        })
        .then(response => response.json())
        .then(data => {
            board = data.board;
            updateTiles();  // Update the tiles only
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

function clearBoard() {
    fetch('/clear', { method: 'POST' })
        .then(() => {
            return fetch('/get_board');
        })
        .then(response => response.json())
        .then(data => {
            board = data.board;
            updateTiles();  // Update the tiles only
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

// Add this function to send updated board to the server
function updateServerBoard() {
    fetch('/update_board', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ board: board }),
    });
}

window.onload = function() {
    fetchBoard();
}

function fetchBoard() {
    fetch('/get_board')
        .then(response => response.json())
        .then(data => {
            board = data.board;  // Now board will be a 9x9 array of integers
            setGame();  // Render the updated board
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}


function setGame() {
    // Digits 
    for (let i = 1; i <= 9; i++) {
        //<div id="1" class="number">1</div>
        let number = document.createElement("div");
        number.id = i
        number.innerText = i;
        number.addEventListener("click", selectNumber);
        number.classList.add("number");
        document.getElementById("digits").appendChild(number);
    }

    // Board 9x9
    for (let r = 0; r < 9; r++) {
        for (let c = 0; c < 9; c++) {
            let tile = document.createElement("div");
            tile.id = r.toString() + "0" + c.toString();
            if (board[r][c] != 0) {
                tile.innerText = board[r][c]; // this matches orginial to display board
                tile.classList.add("tile-start");
            }
            if (r == 2 || r == 5) {
                tile.classList.add("horizontal-line");
            }
            if (c == 2 || c == 5) {
                tile.classList.add("vertical-line");
            }
            tile.addEventListener("click", selectTile);
            tile.classList.add("tile");
            document.getElementById("board").append(tile);
        }
    }
}

//select button numbers
function selectNumber(){
    if (numSelected != null) {
        numSelected.classList.remove("number-selected");
    }
    numSelected = this;
    numSelected.classList.add("number-selected");
}

function selectTile() {
    if (numSelected) {
        this.innerText = numSelected.id;
        let r = parseInt(this.id.charAt(0));
        let c = parseInt(this.id.charAt(2));
        board[r][c] = parseInt(numSelected.id);
        updateServerBoard();
    }
}
