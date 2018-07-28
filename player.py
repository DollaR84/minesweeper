"""
Player for minesweeper.

Created on 24.07.2018

@author: Ruslan Dolovanyuk

"""

import pygame

from constants import Colors


class Player:
    """Player class for minesweeper."""

    def __init__(self, board, speech, phrases):
        """Initialize player class."""
        self.board = board
        self.speech = speech
        self.phrases = phrases
        self.color = Colors.BLUE
        self.index = 0

    def draw(self):
        """Draw method for player."""
        left = self.board.cells[self.index].left
        top = self.board.cells[self.index].top
        size = self.board.cells[self.index].size
        pygame.draw.rect(self.board.board, self.color, (left, top, size, size), 1)

    def move(self, x, y):
        """Move player on board."""
        current_row = self.index // self.board.cols
        current_col = self.index % self.board.cols
        if -1 == y:
            if 0 < current_row:
                current_row += y
            else:
                self.speech.speak(self.phrases['border'])
        elif 1 == y:
            if self.board.rows-1 > current_row:
                current_row += y
            else:
                self.speech.speak(self.phrases['border'])
        if -1 == x:
            if 0 < current_col:
                current_col += x
            else:
                self.speech.speak(self.phrases['border'])
        elif 1 == x:
            if self.board.cols-1 > current_col:
                current_col += x
            else:
                self.speech.speak(self.phrases['border'])

        self.index = (current_row * self.board.cols) + current_col
        self.speak()

    def speak(self):
        """Speak information for moving cell."""
        cell = self.board.cells[self.index]
        if cell.flag:
            self.speech.speak(self.phrases['flag'])
        elif cell.draw_num:
            if 0 == cell.status:
                self.speech.speak(self.phrases['empty'])
            else:
                self.speech.speak(str(cell.status))
        else:
            self.speech.speak(self.phrases['close'])
