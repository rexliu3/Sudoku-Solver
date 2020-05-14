# MainGUI.py
import time
from random import randint

import pygame

from MainSolver import is_valid, solve_sudoku, find_empty

pygame.init()
pygame.font.init()


class Grid:
    def format_board(preboard):
        main = [[], [], [], [], [], [], [], [], []]
        for i in range(0, 9):
            for j in range(0, 9):
                main[i].append(int(preboard[i][0][j]))
        return main

    def generate_board(sub):
        arr = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        x = 0
        while x < 17:
            rowNum = randint(0, 8)
            columnNum = randint(0, 8)
            num = randint(1,9)
            if arr[rowNum][columnNum] == 0 and is_valid(arr, num, rowNum, columnNum):
                arr[rowNum][columnNum] = num
                x += 1
        return arr

    pre_board = [
        ["000004050"],
        ["250000079"],
        ["000029300"],
        ["026900008"],
        ["090000010"],
        ["100007920"],
        ["009280000"],
        ["680000031"],
        ["070400000"]

    ]

    #board = format_board(pre_board)
    board = generate_board(0)

    def __init__(self, rows, columns, width, height):
        self.rows = rows
        self.columns = columns
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(columns)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.columns)] for i in range(self.rows)]

    def place(self, value):
        row, column = self.selected
        if self.cubes[row][column].value == 0:
            self.cubes[row][column].set_value(value)
            self.update_model()

            if is_valid(self.model, value, row, column) and solve_sudoku(self.model):
                return True
            else:
                self.cubes[row][column].set_value(0)
                self.cubes[row][column].set_temporary(0)
                self.update_model()
                return False

    def sketch(self, value):
        row, column = self.selected
        self.cubes[row][column].set_temporary(value)

    def draw(self, window):
        # Draw Sudoku grid lines
        cubeWidth = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(window, (0, 0, 0), (0, i * cubeWidth), (self.width, i * cubeWidth), thick)
            pygame.draw.line(window, (0, 0, 0), (i * cubeWidth, 0), (i * cubeWidth, self.width), thick)
        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.columns):
                self.cubes[i][j].draw(window)

    def select(self, row, column, window):
        # Deselect all cubes
        for i in range(self.rows):
            for j in range(self.columns):
                self.cubes[i][j].selected = False

        self.cubes[row][column].selected = True
        self.selected = (row, column)

    def clear(self):
        row, column = self.selected
        if self.cubes[row][column].value == 0:
            self.cubes[row][column].temporary = 0

    def click(self, position):
        if position[0] < self.width and position[1] < self.height:
            cubeWidth = self.width / 9
            x = position[0] // cubeWidth
            y = position[1] // cubeWidth
            return int(y), int(x)
        else:
            return None

    def completed_sudoku(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    def solve_visual(self, window, time, wrong):
        # Recursive function to solve Sudoku Board
        run = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        find = find_empty(self.model)
        if not find or run == False:
            return True
        else:
            row, column = find
            self.select(row, column, window)

        for k in range(1, 10):
            # Check if Board with value of k is valid
            self.sketch(k)
            update(self, window, time, wrong)

            if is_valid(self.model, k, row, column):
                # If the Board is valid, place the value k at that spot
                self.model[row][column] = k
                self.cubes[row][column].set_value(k)
                self.cubes[row][column].draw(window)
                update(self, window, time, wrong)
                pygame.time.delay(10)

                if self.solve_visual(window, time, wrong):
                    return True

                self.model[row][column] = 0
                self.cubes[row][column].set_value(0)
                update(self, window, time, wrong)
                self.cubes[row][column].draw(window)
                pygame.time.delay(10)
        return False


class Cube:
    rows = 9
    columns = 9

    def __init__(self, value, rows, columns, width, height):
        self.value = value
        self.temporary = 0
        self.rows = rows
        self.columns = columns
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, window):
        font = pygame.font.SysFont("times new roman", 40)
        cubeWidth = self.width / 9
        x = self.columns * cubeWidth
        y = self.rows * cubeWidth
        if self.temporary != 0 and self.value == 0:
            text = font.render(str(self.temporary), 1, (128, 128, 128))
            window.blit(text, (x + (cubeWidth / 2 - text.get_width() / 2), y + (cubeWidth / 2 - text.get_width() / 2)))
        elif not (self.value == 0):
            text = font.render(str(self.value), 1, (0, 0, 0))
            window.blit(text, (x + (cubeWidth / 2 - text.get_width() / 2), y + (cubeWidth / 2 - text.get_width() / 2)))

        if self.selected:
            self.set_background_selected(window)

    def set_value(self, value):
        self.value = value

    def set_temporary(self, temporary):
        self.temporary = temporary

    def set_background_selected(self, window):
        cubeWidth = self.width / 9
        x = self.columns * cubeWidth
        y = self.rows * cubeWidth

        pygame.draw.line(window, (255, 0, 0), (x, y), (x + cubeWidth, y), 2)
        pygame.draw.line(window, (255, 0, 0), (x, y), (x, y + cubeWidth), 2)
        pygame.draw.line(window, (255, 0, 0), (x, y + cubeWidth), (x + cubeWidth, y + cubeWidth), 2)
        pygame.draw.line(window, (255, 0, 0), (x + cubeWidth, y), (x + cubeWidth, y + cubeWidth), 2)


def redraw_window(window, board, time, wrong):
    window.fill((255, 255, 255))
    # Draw time
    font = pygame.font.SysFont("times new roman", 30)
    text = font.render("Time: " + format_time(time), 1, (0, 0, 0))
    window.blit(text, (540 - 170, 560))
    # Draw number of wrong counter
    text = font.render("Number Wrong: " + str(wrong), 1, (255, 0, 0))
    window.blit(text, (10, 560))
    # Draw grid and board
    board.draw(window)


def format_time(seconds):
    second = seconds % 60
    minute = seconds // 60
    hour = minute // 60
    timeFormatted = " " + str(hour) + ":" + str(minute) + ":" + str(second)
    return timeFormatted


def update(inputBoard, window, time, wrong):
    inputBoard.update_model()
    redraw_window(window, inputBoard, time, wrong)
    pygame.display.update()


def generate_random_board():
    main = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for row in range(0, 10):
        sub = nums
        for i in range(0, 9):
            num = randint(1, 10)
            while not is_valid(main, num, row, i):
                num = randint(1, 10)
            main[row][i] = num
    return main


def main():
    window = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku Game Solver")
    board = Grid(9, 9, 540, 540)
    key = None
    run = True
    start = time.time()
    wrong = 0
    while run:

        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_SPACE:
                    board.solve_visual(window, play_time, wrong)
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temporary != 0:
                        if not board.place(board.cubes[i][j].temporary):
                            wrong += 1
                        key = None

                        if board.completed_sudoku():
                            print("Game over")
                            run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1], window)
                    key = None

        if board.selected and key != None:
            board.sketch(key)

        redraw_window(window, board, play_time, wrong)
        pygame.display.update()
        board.update_model()


main()
pygame.quit()
