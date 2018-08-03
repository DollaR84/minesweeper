"""
Board for minesweeper.

Created on 22.07.2018

@author: Ruslan Dolovanyuk

"""

import random

import pygame

from cell import Cell

from constants import Colors


class Board:
    """Board class for minesweeper."""

    def __init__(self, config, screen):
        """Initialize board class."""
        self.config = config
        self.screen = screen

        self.mines = self.config.getint('board', 'mines')
        self.rows = self.config.getint('board', 'rows')
        self.cols = self.config.getint('board', 'cols')
        self.size_cell = self.config.getint('board', 'size_cell')
        self.cells = []
        self.find_mines = 0

        self.board = pygame.Surface(self.get_sizes())
        self.calc_offset()

    def get_sizes(self):
        """Return calculated sizes x and y."""
        return (self.cols*self.size_cell, self.rows*self.size_cell)

    def calc_offset(self):
        """Calculate position board on screen."""
        screen_x = self.config.getint('screen', 'size_x')
        screen_y = self.config.getint('screen', 'size_y')
        board_sizes = self.get_sizes()
        board_x = board_sizes[0]
        board_y = board_sizes[1]

        offset_x = (screen_x - board_x) // 2
        offset_y = screen_y - board_y

        self.offset = (offset_x, offset_y)

    def draw(self):
        """Draw method for board."""
        self.screen.blit(self.board, self.offset)
        for cell in self.cells:
            cell.draw(self.board)
        for row in range(self.rows):
            for col in range(self.cols):
                pygame.draw.rect(self.board, Colors.WHITE, (col*self.size_cell, row*self.size_cell, self.size_cell, self.size_cell), 1)

    def generate(self):
        """Generate objects cells."""
        self.cells.clear()
        self.find_mines = 0

        for row in range(self.rows):
            for col in range(self.cols):
                self.cells.append(Cell(col*self.size_cell, row*self.size_cell, self.size_cell))

        mines = set()
        random.seed()
        while len(mines) < self.mines:
            value = random.randint(0, len(self.cells)-1)
            if value not in mines:
                mines.add(value)

        for mine in mines:
            self.cells[mine].status = 9

        self.calc_around_cells()

    def calc_around_cells(self):
        """Calculate around cells."""
        for index, cell in enumerate(self.cells):
            row = index // self.cols
            col = index % self.cols
            cells = []
            if (0 < row) and ((self.rows-1) > row):
                if (0 < col) and ((self.cols-1) > col):
                    cells.append(self.cells[(row-1)*self.cols+(col-1)])
                    cells.append(self.cells[(row-1)*self.cols+(col+1)])
                    cells.append(self.cells[(row-1)*self.cols+col])

                    cells.append(self.cells[row*self.cols+(col-1)])
                    cells.append(self.cells[row*self.cols+(col+1)])

                    cells.append(self.cells[(row+1)*self.cols+(col-1)])
                    cells.append(self.cells[(row+1)*self.cols+(col+1)])
                    cells.append(self.cells[(row+1)*self.cols+col])
                elif 0 == col:
                    cells.append(self.cells[(row-1)*self.cols+(col+1)])
                    cells.append(self.cells[(row-1)*self.cols+col])

                    cells.append(self.cells[row*self.cols+(col+1)])

                    cells.append(self.cells[(row+1)*self.cols+(col+1)])
                    cells.append(self.cells[(row+1)*self.cols+col])
                elif (self.cols-1) == col:
                    cells.append(self.cells[(row-1)*self.cols+(col-1)])
                    cells.append(self.cells[(row-1)*self.cols+col])

                    cells.append(self.cells[row*self.cols+(col-1)])

                    cells.append(self.cells[(row+1)*self.cols+(col-1)])
                    cells.append(self.cells[(row+1)*self.cols+col])
            elif 0 == row:
                if (0 < col) and ((self.cols-1) > col):
                    cells.append(self.cells[row*self.cols+(col-1)])
                    cells.append(self.cells[row*self.cols+(col+1)])

                    cells.append(self.cells[(row+1)*self.cols+(col-1)])
                    cells.append(self.cells[(row+1)*self.cols+(col+1)])
                    cells.append(self.cells[(row+1)*self.cols+col])
                elif 0 == col:
                    cells.append(self.cells[row*self.cols+(col+1)])

                    cells.append(self.cells[(row+1)*self.cols+(col+1)])
                    cells.append(self.cells[(row+1)*self.cols+col])
                elif (self.cols-1) == col:
                    cells.append(self.cells[row*self.cols+(col-1)])

                    cells.append(self.cells[(row+1)*self.cols+(col-1)])
                    cells.append(self.cells[(row+1)*self.cols+col])
            elif (self.rows-1) == row:
                if (0 < col) and ((self.cols-1) > col):
                    cells.append(self.cells[(row-1)*self.cols+(col-1)])
                    cells.append(self.cells[(row-1)*self.cols+(col+1)])
                    cells.append(self.cells[(row-1)*self.cols+col])

                    cells.append(self.cells[row*self.cols+(col-1)])
                    cells.append(self.cells[row*self.cols+(col+1)])
                elif 0 == col:
                    cells.append(self.cells[(row-1)*self.cols+(col+1)])
                    cells.append(self.cells[(row-1)*self.cols+col])

                    cells.append(self.cells[row*self.cols+(col+1)])
                elif (self.cols-1) == col:
                    cells.append(self.cells[(row-1)*self.cols+(col-1)])
                    cells.append(self.cells[(row-1)*self.cols+col])

                    cells.append(self.cells[row*self.cols+(col-1)])
            cell.calc_status(cells)
