"""
Cell on board minesweeper.

Created on 22.07.2018

@author: Ruslan Dolovanyuk

"""

import pygame

from constants import Colors


class Cell:
    """Cell class on board for minesweeper."""

    def __init__(self, left, top, size):
        """Initialize cell class."""
        self.left = left
        self.top = top
        self.size = size
        self.status = 0
        self.color = Colors.SILVER
        self.flag = False
        self.draw_num = False
        self.reopen_flag = False

    def set_flag(self):
        """Set status flag attribute."""
        self.flag = not self.flag
        self.color = Colors.RED if self.flag else Colors.SILVER

    def open(self):
        """Open cell on board."""
        if not self.flag:
            if 9 == self.status:
                self.color = Colors.BLACK
                return False
            else:
                self.color = Colors.GREEN
                self.draw_num = True
        return True

    def reopen(self):
        """Open around cells."""
        mines = False
        for cell in self.around:
            if (9 == cell.status) and not cell.flag:
                mines = True

        if not mines:
            self.reopen_flag = True
            for cell in self.around:
                if not cell.flag:
                    cell.open()
                    if not cell.reopen_flag:
                        cell.reopen()

    def draw(self, board):
        """Draw method for cell."""
        pygame.draw.rect(board, self.color, (self.left, self.top, self.size, self.size))
        if self.draw_num and (0 != self.status):
            board.blit(self.textSurfaceObj, self.textRectObj)

    def calc_status(self, cells):
        """Calculate status with around cells."""
        if 9 != self.status:
            for cell in cells:
                if 9 == cell.status:
                    self.status += 1

            if 0 != self.status:
                fontObj = pygame.font.SysFont('arial', 14)
                self.textSurfaceObj = fontObj.render(str(self.status), True, Colors.BLUE)
                self.textRectObj = self.textSurfaceObj.get_rect()
                self.textRectObj.center = (self.left+(self.size//2), self.top+(self.size//2))

            self.around = cells
