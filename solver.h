#ifndef solver_h
#define solver_h

#pragma once
#include <vector>

namespace sudoku {

  // Define the Board struct
  struct Board {
    int rows;  // 1 indexed
    int cols;  // 1 indexed
    std::vector<std::vector<int> > board;
  };

  typedef struct Board Board_t;

  //create new board 
  Board_t newBoard(int row, int col);
  //REQUIRES o <= row || 0 <= col
  //REQUIRES row % 3 == 0 || col % 3 == 0  (Row and col form proper 3x3 grids)

  //create new board 
  void printBoard(const Board_t& board);

  // Check if value in given index is valid
  bool isValidValue(int row, int col, int input, const Board_t& board);

  // Solve the given Sudoku board and return the solution as a vector of vectors.
  Board_t solve(Board_t board);

  // Get the possible values for the cell at the given row and column index.
  int getPossibleValue(int row, int col, const Board_t& board);

}  


#endif /* solver_h */