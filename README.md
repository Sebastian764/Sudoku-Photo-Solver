# Sudoku Photo Solver

## Introduction

Sudoku Photo Solver is a web application that allows users to upload an image of a Sudoku board and have it solved automatically. The project integrates multiple technologies including Python (Flask, OpenCV, Numpy, Tensorflow, ctypes), JavaScript, and HTML to create a seamless user experience. It uses advanced image processing and a C library to solve Sudoku boards.
### Demo:
![ezgif-4-a2257c9d2d](https://github.com/Sebastian764/Sudoku-Photo-Solver/assets/120810193/f931b3fb-aa2a-4c76-aa7d-2ff21e0246fc)


## Features
* Image Upload: Upload a photo of a Sudoku board.
* Image Processing: Extracts Sudoku grid and numbers using OpenCV and Numpy, then converts handwritten digits using Tensorflow.
* Sudoku Solver: Uses a custom C library to solve the extracted Sudoku board (Note that the code was originally written in C++, it was modified to C and slightly simplified when it was converted into 'sudoku_solver.so').
* Interactive UI: Allows users to manually edit, solve, and clear the Sudoku board.

## Prerequisites
* Python 3.11.3
* Flask
* OpenCV for Python (cv2)
* numpy
* Tensorflow
* ctypes

## How to Run
1. Clone this repository
2. Navigate to the project directory and install required packages
3. Run the command below:
```
python app.py
```
4. Go to http://127.0.0.1:5000


# Sudoku Solver Library

# Image Processor Library

## preprocess_image()
This function is responsible for preprocessing an image. It applies a Gaussian Blur to remove noise, inverts the image, and fill in any “cracks” in the image. 

## detect_and_crop_grid()
This function is responsible for identifying the Sudoku grid in an input image and cropping it to a 252x252 square image that focuses solely on the grid. The steps are as follows:
1. **Image Pre-processing:** Grayscale conversion and Gaussian blur application.
2. **Edge Detection:** Uses Canny edge detection to find edges in the image.
3. **Finding Contours:** Identifies the largest contour in the image, assuming it to be the Sudoku grid.
4. **Perspective Transformation:** Calculates four lines that approximate the outer boundary of the grid, finds their intersection points, and uses these points to warp the perspective, thereby correcting any skewness.

## create_image_grid()
1. **Adaptive Thresholding:** Applies to make the grid lines prominent.

This function further divides the 252x252 square image into 81 smaller 28x28 squares (each representing a cell in the Sudoku grid). It applies additional pre-processing via postProcessCell() to each cell to remove any noise and center the number.

  ## postProcessCell() (Helper function for create_image_grid()
  This function takes in a 28x28 cell image and performs:
  1. **Flood Filling:** To remove outermost white pixels.
  2. **Bounding Box Detection:** To identify the region where the number is located.
  3. **Content Centering:** Centers the number within the cell.

# Image Converter Library
It only has one function,imagesToGrid(). The function takes in a 9x9 array, with each slot containing a 28x28 image. It will comapre every cell to a certain threshold, and if it is below the threshold, it will assign that value to 0. Otherwise, the image will be passed on to the either the Convolutional Neural Network.





