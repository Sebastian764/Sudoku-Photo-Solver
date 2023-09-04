from ImageProcessor import ImageProcessor
from ImageConverter import imagesToGrid
import ctypes
import numpy as np
import cv2

# cv2.imread()
boardExtractor = ImageProcessor('/Users/pc/Documents/Sudoku/image_processor/boards/sudoku4.png')
boardExtractor.preprocess_image()
boardExtractor.detect_and_crop_grid()

boardcells = boardExtractor.create_image_grid()

# boardConverter = ImageConverter()

example = imagesToGrid(boardcells)

print(example)
# Load the shared library/DLL
lib = ctypes.CDLL('./Integrated/sudoku_solver.so')

# Define the argument and return types for the function
lib.solve.argtypes = [np.ctypeslib.ndpointer(dtype=np.int32, ndim=2, flags='C_CONTIGUOUS')]
lib.solve.restype = None

# Create a sample board
def converter(board):
    return np.array((board), dtype=np.int32)

# example = [	
#                 [ 0,0,0,  0,0,0,  0,0,0 ],
#                 [ 0,0,0,  0,0,3,  0,8,5 ],
#                 [ 0,0,1,  0,2,0,  0,0,0 ],

#                 [ 0,0,0,  5,0,7,  0,0,0 ],
#                 [ 0,0,4,  0,0,0,  1,0,0 ],
#                 [ 0,9,0,  0,0,0,  0,0,0 ],

#                 [ 5,0,0,  0,0,0,  0,7,3 ],
#                 [ 0,0,2,  0,1,0,  0,0,0 ],
#                 [ 0,0,0,  0,4,0,  0,0,9 ]
# 								];
board = converter(example)
# board = np.zeros((9, 9), dtype=np.int32)


# Call the function
lib.solve(board)

# Print the solution
print(board)

  

