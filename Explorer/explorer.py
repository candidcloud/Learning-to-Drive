"""
This module creates a class for a game called Explorer. The objective is
to reach the end of each level (pngs stored separately).
"""

import matplotlib.pyplot as plt
import numpy as np
import random
from pathlib import Path

class Game():
    """
    A class which implements the Tracker game. Initializes with a grid_size
    and path_radius. There is an "example" method to illustrate how the
    game is played.
    """
    def __init__(self, grid_size, path_radius):
        """
        Initializes the player color and a game board.
        """
        self.levels = [plt.imread(str(img_path)) for img_path in list(Path('.').glob('level*.png'))]
        self.player_color = (255,0,255)
        self.object_colors = {(255,202,24):'goal',
                              (236,28,36):'lava',
                              (0,0,0):'wall'}
        self.board_params = []
        self.start_game()

    def start_game(self):
        """
        Resets the board and player.
        """
        self.board = self.levels[0]
        self.player_pos = _get_start()
        self.score = 0
        self.time = 0

    def show_board(self):
        """
        Throws the current board to the active plot window.
        """
        plt.imshow(self.board)
        plt.show(block=False)

    def update_board(self, new_pos):
        """
        Performs the board update using a desired action (in the form of a
        destination square).
        """
        self.time += 1
        self.board[new_pos] = self.player_color
        self.player_pos = new_pos
        self.update_score()


    def update_score(self):
        """
        Allocates a reward to the player based on the result of the most
        recent move.
        """
        ####################################
        self.score += reward

    def get_actions(self):
        """
        Returns available moves using the current board configuration.
        """
        x,y = self.player_pos
        actions = [(x+1,y), (x+1,y+1), (x,y+1),
                   (x-1,y), (x-1,y-1), (x,y-1),
                   (x+1,y-1), (x-1,y+1)]
        valid = []
        for a in actions:
            if (a[0] > self.board_params[0]-1 or a[1] > self.board_params[0]-1 or
                a[0] < 0 or a[1] < 0):
                pass
            else:
                valid.append(a)
        return valid

    def check_end(self):
        """
        Assesses whether all white tiles have been removed.
        """
        if self.time < 50:
            return False
        else:
            return True

    def example(self):
        """
        Illustrates how to play the game.
        """
        end = False
        while not end:
            plt.pause(0.25)
            self.update_board(random.choice(self.get_actions()))
            end = self.check_end()

    def _get_start(self):
        """
        Identify the square in a loaded map which identifies the
        player's start location.
        """
        s = self.board.shape
        for i in range(s[0]):
            for j in range(s[1]):
                if (levels[0][i,j,:] == np.array([255,0,255])).all():
                    self.player_pos = (i,j)
