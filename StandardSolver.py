# StandardSolver.py

board = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]


# 1) Pick next empty square
# 2) Try all numbers for that empty square until you find one that works
# 3) Repeat 1 & 2 for all empty squares until there is no possible solution to one square
# 4) Backtrack

def print_board(inputBoard):
    # Prints board
    for i in range(len(inputBoard)):
        if i % 3 == 0 and i != 0:
            print("-----------------------")
        for j in range(len(inputBoard[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(inputBoard[i][j])
            else:
                print(str(inputBoard[i][j]) + " ", end="")


def find_empty(inputBoard):
    # Returns position of next empty square
    for i in range(len(inputBoard)):
        for j in range(len(inputBoard[i])):
            if inputBoard[i][j] == 0:
                return (i, j)  # Return (row, column)
    return None


def is_valid(inputBoard, num, row, column):
    # Return whether if inputBoard is valid or invalid
    main = num

    # Check Row
    for j in range(len(inputBoard[row])):
        if j != column and inputBoard[row][j] == main:
            return False

    # Check Column
    for i in range(len(inputBoard)):
        if i != row and inputBoard[i][column] == main:
            return False

    # Check Box
    boxX = column // 3
    boxY = row // 3

    for i in range(3):
        for j in range(3):
            if inputBoard[boxY * 3 + i][boxX * 3 + j] == main:
                if boxY * 3 + i != row or boxX * 3 + j != column:
                    return False
    return True


def solve_sudoku(inputBoard):
    # Recurssive funciton to solve Sodoku Board
    find = find_empty(inputBoard)
    if not find:
        return True
    else:
        row, column = find

    for k in range(1, 10):
        # Check if Board with value of i is valid
        if is_valid(inputBoard, k, row, column):
            # If the Board is valid, place the value k at that spot
            inputBoard[row][column] = k

            # Continue solving the next empty spaces
            if solve_sudoku(inputBoard):
                return True
            # Set the position back to 0 because there is an error in the future settings
            inputBoard[row][column] = 0
    return False


print_board(board)
solve_sudoku(board)
print("                                 ")
print_board(board)
