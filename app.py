from flask import Flask, render_template, request, redirect, url_for, jsonify
import numpy as np
# import cv2
from ImageProcessor import ImageProcessor
from ImageConverter import imagesToGrid
import ctypes
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

SUDOKU_BOARD = [[0 for _ in range(9)] for _ in range(9)]
ERROR_MESSAGE = None

def wrapperProcess(image_path):
    try:
        boardExtractor = ImageProcessor(image_path)
        boardExtractor.preprocess_image()
        boardExtractor.detect_and_crop_grid()
        boardcells = boardExtractor.create_image_grid()
        grid = imagesToGrid(boardcells)
        return grid
    except Exception as e:
        return str(e)

def wrapperSolve(grid):
    lib = ctypes.CDLL('/Users/pc/Documents/Sudoku/Integrated/sudoku_solver.so')
    lib.solve.argtypes = [np.ctypeslib.ndpointer(dtype=np.int32, ndim=2, flags='C_CONTIGUOUS')]
    lib.solve.restype = None
    npArray = np.array(grid, dtype=np.int32)
    lib.solve(npArray)
    return npArray.tolist()

@app.route("/", methods=["GET", "POST"])
def index():
    global SUDOKU_BOARD, ERROR_MESSAGE
    return render_template("index.html", sudoku_board=SUDOKU_BOARD, error_message=ERROR_MESSAGE)

@app.route("/upload", methods=["POST"])
def upload():
    global SUDOKU_BOARD, ERROR_MESSAGE
    if "image" in request.files:
        image = request.files["image"]
        if image.filename != "":
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image.filename))
            image.save(image_path)
            SUDOKU_BOARD = wrapperProcess(image_path)
            if isinstance(SUDOKU_BOARD, str):
                ERROR_MESSAGE = SUDOKU_BOARD  # An error occurred
                SUDOKU_BOARD = None
            else:
                ERROR_MESSAGE = None  # Clear any previous error messages
    return redirect(url_for("index"))

@app.route("/solve", methods=["POST"])
def solve():
    global SUDOKU_BOARD, ERROR_MESSAGE

    unsolved_board = SUDOKU_BOARD
    solved_board = wrapperSolve(SUDOKU_BOARD)
    if unsolved_board == solved_board:
        ERROR_MESSAGE = "Board is unsolvable"
    else:
        ERROR_MESSAGE = "Board successfully solved"
        SUDOKU_BOARD = solved_board
    return redirect(url_for("index"))

@app.route("/clear", methods=["POST"])
def clear():
    global SUDOKU_BOARD, ERROR_MESSAGE
    SUDOKU_BOARD = [[0 for _ in range(9)] for _ in range(9)]
    return redirect(url_for("index"))


@app.route("/get_board", methods=["GET"])
def get_board():
    global SUDOKU_BOARD
    # print(SUDOKU_BOARD)
    # Convert np.int64 to native Python int
    board_to_send = [[int(cell) for cell in row] for row in SUDOKU_BOARD]
    return jsonify({"board": board_to_send})

@app.route("/update_board", methods=["POST"])
def update_board():
    global SUDOKU_BOARD
    new_board = request.get_json()["board"]
    SUDOKU_BOARD = new_board
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True)