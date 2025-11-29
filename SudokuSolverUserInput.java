import java.util.Scanner;

public class SudokuSolverUserInput {

    static final int SIZE = 9;

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int[][] board = new int[SIZE][SIZE];

        System.out.println("Enter Sudoku Puzzle (0 for empty cells):");
        
        // Taking Sudoku input from user
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                board[i][j] = sc.nextInt();
            }
        }

        System.out.println("\nSolving Sudoku...\n");

        if (solveSudoku(board)) {
            System.out.println("Sudoku Solved Successfully!\n");
            printBoard(board);
        } else {
            System.out.println("No Solution Exists for the Given Sudoku.");
        }

        sc.close();
    }

    // Sudoku solving using Backtracking
    public static boolean solveSudoku(int[][] board) {
        for (int row = 0; row < SIZE; row++) {
            for (int col = 0; col < SIZE; col++) {

                if (board[row][col] == 0) { // empty cell
                    for (int num = 1; num <= 9; num++) {

                        if (isSafe(board, row, col, num)) {
                            board[row][col] = num;

                            if (solveSudoku(board)) {
                                return true;
                            }

                            board[row][col] = 0; // backtrack
                        }
                    }
                    return false; 
                }
            }
        }
        return true; 
    }

    // Check if placing num at (row, col) is safe
    public static boolean isSafe(int[][] board, int row, int col, int num) {

        // Check row
        for (int x = 0; x < SIZE; x++) {
            if (board[row][x] == num) return false;
        }

        // Check column
        for (int x = 0; x < SIZE; x++) {
            if (board[x][col] == num) return false;
        }

        // Check 3×3 subgrid
        int startRow = row - row % 3;
        int startCol = col - col % 3;

        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (board[startRow + i][startCol + j] == num)
                    return false;
            }
        }

        return true; 
    }

    // Print Sudoku Board
    public static void printBoard(int[][] board) {
        for (int i = 0; i < SIZE; i++) {
            if (i % 3 == 0 && i != 0)
                System.out.println("---------------------");

            for (int j = 0; j < SIZE; j++) {
                if (j % 3 == 0 && j != 0)
                    System.out.print("| ");

                System.out.print(board[i][j] + " ");
            }
            System.out.println();
        }
    }
}
