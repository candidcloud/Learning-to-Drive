"""
This module creates a class for a game called Tracker. The objective is to
track over all of the white tiles while avoiding excursions onto the black
tiles. Included in the Game class is a method called
"example" which takes no parameters and simply has the computer randomly
choose actions to play the game for illustration purposes.
"""

import matplotlib.pyplot as plt
import numpy as np
import random
from itertools import cycle

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
        self.player_color = (255,0,255)
        self.bonus_color = (200,150,0)
        self.board_params = (grid_size, path_radius)
        self.start_game()

    def start_game(self):
        """
        Resets the board and player.
        """
        self.board = self._draw_board(*self.board_params)
        self.player_pos = (8,5)
        center = self.board_params[0]//2
        self.order = [(4,7),(3,7),(3,6),(2,5),(3,4),(3,3),(4,3),(5,2),
                 (6,3),(7,3),(7,4),(8,5),(7,6),(7,7),(6,7),(5,8)]
        self.path = cycle(self.order)
        self.bonus_pos = next(self.path)
        self.score = 0
        self.time = 0
        self.board[self.player_pos[0], self.player_pos[1]] = self.player_color

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
        self.bonus_pos = next(self.path)
        self.board = self._draw_board(*self.board_params)
        self.board[self.bonus_pos] = self.bonus_color
        self.board[new_pos] = self.player_color
        self.player_pos = new_pos
        self.update_score()


    def update_score(self):
        """
        Allocates a reward to the player based on the result of the most
        recent move.
        """
        if self.player_pos == self.bonus_pos:
            reward = 10
        elif self.player_pos in self.order:
            reward = 5
        else:
            reward = -10
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

    def _get_circle(self, r, section='whole'):
        """
        Returns a list of pairs which correspond to pixel locations for drawing a
        circle of radius r. The section parameter should be one of 'whole',
        'half', 'fourth', or 'eighth'. Defaults to 'whole'.
        """
        stepsize = 1
        x = r
        y = 0

        limit = (r * 185363) >> 18  # approx sin(pi/4)
        xvals,yvals = [], []
        xvals.append(x)
        yvals.append(y)

        while y<x:
            if 2*(x*x+y*y-r*r)+stepsize > 0:
                x -= stepsize
            xvals.append(x)
            y += stepsize
            yvals.append(y)

        # Create circle parts using symmetry
        eighth = list(zip(xvals,yvals))
        fourth = eighth + [(y,x) for (x,y) in eighth]
        half = fourth + [(-x,y) for (x,y) in fourth]
        whole = half + [(x,-y) for (x,y) in half]

        parts = [eighth, fourth, half, whole]

        # Ensure no errors
        if section not in ['eighth', 'fourth', 'half']:
            section = 'whole'

        # Get values for plotting and display scatter plot
        xvals = [pt[0] for pt in eval(section)]
        yvals = [pt[1] for pt in eval(section)]

        # Ensure returned list has no duplicates
        return list(set(eval(section)))

    def _draw_board(self, grid_size, path_radius):
        """
        Draws a new board with the path in white and the rest in black. An
        AssertionError is raised if the path_radius is too large for the
        chosen grid_size.
        """
        assert grid_size>2*path_radius, "Board size is not large enough for path."
        center = grid_size//2
        board = np.zeros((grid_size,grid_size,3),dtype=np.uint8)
        path = self._get_circle(path_radius)
        path_color = (255,255,255)
        for x,y in path:
            board[x+center,y+center,:] = path_color
        return board
