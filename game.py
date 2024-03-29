"""
Main game module for minesweeper.

Created on 22.07.2018

@author: Ruslan Dolovanyuk

"""

import time
import pickle

import pygame

from configparser import ConfigParser

from board import Board

from constants import Colors

from player import Player

from speech import Speech


class Game:
    """Main running class for game."""

    def __init__(self):
        """Initialize running class."""
        self.config = ConfigParser()
        self.config.read('settings.ini')
        self.size_x = self.config.getint('screen', 'size_x')
        self.size_y = self.config.getint('screen', 'size_y')

        with open('languages.dat', 'rb') as lang_file:
            self.phrases = pickle.load(lang_file)[self.config.get('total', 'language')]

        self.speech = Speech(self.config)
        self.speech.speak(self.phrases['start'])

        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((self.size_x, self.size_y))
        pygame.display.set_caption(self.phrases['title'])

        self.board = Board(self.config, self.screen)
        self.player = Player(self.board, self.speech, self.phrases)
        self.game_over = True
        self.timer = 0

        self.fontObj = pygame.font.SysFont('arial', 50)
        self.clock = pygame.time.Clock()
        pygame.time.set_timer(pygame.USEREVENT, 1000)

        self.new_game()
        try:
            save_file = open('autosave.sav', 'rb')
        except IOError as e:
            pass
        else:
            with save_file:
                data = pickle.load(save_file)
                self.board.cells = data['cells']
                self.board.find_mines = data['find_mines']
                self.timer = data['timer']
                self.speech.speak(self.phrases['load'])
                for cell in self.board.cells:
                    cell.status = 0 if 9 != cell.status else cell.status
                self.board.calc_around_cells()
                self.player.speak()

    def mainloop(self):
        """Run main loop game."""
        self.running = True
        while self.running:
            self.handle_events()
            self.draw()

            self.clock.tick(15)
            pygame.display.flip()

        with open('autosave.sav', 'wb') as save_file:
            data = {'cells': self.board.cells, 'find_mines': self.board.find_mines, 'timer': self.timer}
            pickle.dump(data, save_file)
            self.speech.speak(self.phrases['save'])
        self.speech.speak(self.phrases['finish'])
        pygame.quit()

    def handle_events(self):
        """Check all game events."""
        for event in pygame.event.get():
            if pygame.QUIT == event.type:
                self.running = False
            elif pygame.USEREVENT == event.type:
                if not self.game_over:
                    self.timer += 1
            elif pygame.KEYDOWN == event.type:
                if pygame.K_ESCAPE == event.key:
                    self.running = False
                elif pygame.K_F1 == event.key:
                    self.help()
                elif pygame.K_F5 == event.key:
                    self.new_game()
                elif pygame.K_F9 == event.key:
                    self.change_language()
                elif pygame.K_LEFT == event.key:
                    if not self.game_over:
                        self.player.move(-1, 0)
                elif pygame.K_RIGHT == event.key:
                    if not self.game_over:
                        self.player.move(1, 0)
                elif pygame.K_UP == event.key:
                    if not self.game_over:
                        self.player.move(0, -1)
                elif pygame.K_DOWN == event.key:
                    if not self.game_over:
                        self.player.move(0, 1)
                elif pygame.K_f == event.key:
                    if not self.game_over:
                        self.board.cells[self.player.index].set_flag()
                        if self.board.cells[self.player.index].flag:
                            self.board.find_mines += 1
                            self.speech.speak(self.phrases['flag'])
                        else:
                            self.board.find_mines -= 1
                            self.speech.speak(self.phrases['close'])
                elif pygame.K_SPACE == event.key:
                    if not self.game_over:
                        cell = self.board.cells[self.player.index]
                        if cell.draw_num and not cell.reopen_flag:
                            cell.reopen()
                        result = cell.open()
                        if not result:
                            self.game_over = True
                            self.speech.speak(self.phrases['game_over'])
                        elif 0 == (self.board.mines-self.board.find_mines):
                            self.game_over = True
                            self.speech.speak(self.phrases['win'])
                        elif not cell.flag and (0 == cell.status):
                            self.speech.speak(self.phrases['empty'])
                        elif not cell.flag:
                            self.speech.speak(str(cell.status))
                elif pygame.K_m == event.key:
                    self.speech.speak(str(self.board.mines-self.board.find_mines))
                elif pygame.K_t == event.key:
                    self.speech.speak(self.get_timer())
                elif pygame.K_c == event.key:
                    row = self.player.index // self.board.cols
                    col = self.player.index % self.board.cols
                    self.speech.speak('%s; %s' % (col, row))

    def draw(self):
        """Main draw function."""
        self.screen.fill(Colors.GRAY)
        self.board.draw()
        textSurfaceTimer = self.fontObj.render(self.get_timer(), True, Colors.BLUE)
        textRectTimer = textSurfaceTimer.get_rect()
        textRectTimer.left = 30
        textRectTimer.top = 30
        self.screen.blit(textSurfaceTimer, textRectTimer)
        textSurfaceMines = self.fontObj.render(str(self.board.mines-self.board.find_mines), True, Colors.BLUE)
        textRectMines = textSurfaceMines.get_rect()
        textRectMines.right = self.size_x - 30
        textRectMines.top = 30
        self.screen.blit(textSurfaceMines, textRectMines)
        if self.game_over:
            if 0 == (self.board.mines - self.board.find_mines):
                textSurfaceObj = self.fontObj.render(self.phrases['win'], True, Colors.GREEN)
            else:
                textSurfaceObj = self.fontObj.render(self.phrases['game_over'], True, Colors.RED)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (self.size_x//2, self.size_y//2)
            self.screen.blit(textSurfaceObj, textRectObj)
        else:
            self.player.draw()

    def new_game(self):
        """Start new game."""
        self.speech.speak(self.phrases['new_game'])
        self.board.generate()
        self.game_over = False
        self.timer = 0
        self.player.index = 0
        self.player.speak()

    def get_timer(self):
        """Return string with hours:minutes:seconds from seconds timer."""
        seconds = self.timer % 60
        minutes = (self.timer // 60) % 60
        hours = (self.timer // 60) // 60
        return '%d:%d:%d' % (hours, minutes, seconds)

    def help(self):
        """Speak help for keys control game."""
        file_name = 'help_' + self.config.get('total', 'language') + '.txt'
        with open(file_name, 'r', encoding='utf8') as help_file:
            data = help_file.readlines()
            for line in [line for line in data if '\n' != line]:
                self.speech.speak(line)
                time.sleep(0.1)

    def change_language(self):
        """Change language for phrases."""
        if 'ru' == self.config.get('total', 'language'):
            self.config.set('total', 'language', 'en')
            with open('languages.dat', 'rb') as lang_file:
                self.phrases = pickle.load(lang_file)['en']
        else:
            self.config.set('total', 'language', 'ru')
            with open('languages.dat', 'rb') as lang_file:
                self.phrases = pickle.load(lang_file)['ru']
        self.player.phrases = self.phrases
        self.speech.speak(self.phrases['language'])
        with open('settings.ini', 'w') as config_file:
            self.config.write(config_file)
