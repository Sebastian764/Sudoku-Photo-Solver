#include "solver.h"
#include <iostream>
#include <array>
#include <bitset>

sudoku::Board_t sudoku::newBoard(int row, int col) 
{
  if (row <= 0 || col <= 0) {
    throw std::invalid_argument("Invalid row or column count");
  }

  if (row % 3 != 0 || col % 3 != 0 ) {
    throw std::invalid_argument("Row or column values do not form grid");
  }

  // 'std::vector<int>(col, -1)' creates a 1D vector of size col with all elements set to -1. 
  // 'board(row, ...)' creates a 2D vector of size row x col
  std::vector<std::vector<int>> board(row, std::vector<int>(col, 0));
  return {row, col, board};
}

void sudoku::printBoard(const sudoku::Board_t& board) 
{
  for (int i = 0; i < board.rows; i++) {
    for (int j = 0; j < board.cols; j++) {
      printf("%d ", board.board[i][j]);
    }
    printf("\n");
  }
}

bool sudoku::isValidValue(int row, int col, int input, const sudoku::Board_t& board)
{
  if (board.rows < row || board.cols < col) {
    throw std::invalid_argument("invalid row or col");
  }

  // check entire col 
  for (int i = 0; i < board.rows; i++) {
    if (board.board[row][i] == input) return false;
  }

  // check entire row
  for (int i = 0; i < board.cols; i++) {
    if (board.board[i][col] == input) return false;
  }

  //check entire block
  int blockRow = (row / 3) * 3;
  int blockCol = (col / 3) * 3;
  
  for (int i = blockRow; i < blockRow + 3; i++) {
    for (int j = blockCol; j < blockCol + 3; j++) {
      if (board.board[i][j] == input) return false;
    }
  }

  return true;
}

std::bitset<10> getCandidates(const std::vector<std::vector<int>>& board, int row, int col) {
    std::bitset<10> candidates;
    candidates.set();  // Initialize all bits to 1

    // Check row
    for (int c = 0; c < 9; ++c) {
        candidates.reset(board[row][c]);
    }

    // Check column
    for (int r = 0; r < 9; ++r) {
        candidates.reset(board[r][col]);
    }

    // Check 3x3 box
    int startRow = (row / 3) * 3;
    int startCol = (col / 3) * 3;
    for (int r = startRow; r < startRow + 3; ++r) {
        for (int c = startCol; c < startCol + 3; ++c) {
            candidates.reset(board[r][c]);
        }
    }

    return candidates;
}

bool solveHelper(sudoku::Board_t& board, int row, int col) 
{
  // Check if we have reached the end of the board
  if (row == board.rows) {
    return true;
  }

  // Calculate the next row and column
  int nextRow, nextCol;
  if (col == board.cols - 1) {
    nextRow = row + 1;
    nextCol = 0;
  } else {
    nextRow = row;
    nextCol = col + 1;
  }

  // Check if this cell is already filled
  if (board.board[row][col] != 0) {
    return solveHelper(board, nextRow, nextCol);
  }


      //   std::bitset<10> candidates = getCandidates(board.board, row, col);

      // for (int num = 1; num <= 9; ++num) {
      //   if (candidates[num]) {
      //     board.board[row][col] = num;

      //     if (solveHelper(board, nextRow, nextCol)) {
      //       return true;  // Found a valid solution
      //     }

      //     board.board[row][col] = 0;  // Backtrack
      //   }
      // }

  // Try every possible value in this cell
  for (int i = 9; 1 <= i; i--) {
    if (isValidValue(row, col, i, board)) {
      board.board[row][col] = i;
      if (solveHelper(board, nextRow, nextCol)) {
        return true;
      }
      // backtrack by returning cell to 0
      board.board[row][col] = 0;
    }
  }

  // If no valid value was found, backtrack
  return false;
}

sudoku::Board_t sudoku::solve(sudoku::Board_t board) 
{
  // if (!isValidBoard(board)) {
  //   throw std::invalid_argument("invalid board");
  // }

  solveHelper(board, 0, 0);
  return board;
}

int sudoku::getPossibleValue(int row, int col, const sudoku::Board_t& board) 
{
  sudoku::Board_t solution =  board;
  if (solveHelper(solution, 0, 0)) {
    return solution.board[row][col];
  } else {
    return 0;
  }
}
