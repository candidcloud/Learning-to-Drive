"""
This module creates a class for a game called Gobble. The objective is to
gobble up all of the white tiles while avoiding excursions onto the black
tiles. Landing on a white tile adds 1 to the score; landing on a black square
subtracts 1 from the score. Included in the Game class is a method called
"example" which takes no parameters and simply has the computer randomly
choose actions to play the game for illustration purposes.
"""

import matplotlib.pyplot as plt
import numpy as np
import random

# Ensure the plot windows will update properly
plt.ion()

def get_circle(r, section='whole'):
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
#    fig,ax = plt.subplots()
#    ax.scatter(xvals,yvals)
#    ax.axis('equal')
#    plt.show(block=False)

    # Ensure returned list has no duplicates
    return list(set(eval(section)))

def draw_board(grid_size, path_radius):
    """
    Draws a new board with the path in white and the rest in black. An
    AssertionError is raised if the path_radius is too large for the
    chosen grid_size.
    """
    assert grid_size>2*path_radius, "Board size is not large enough for path."
    center = grid_size//2
    board = np.zeros((grid_size,grid_size,3),dtype=np.uint8)
    path = get_circle(path_radius)
    path_color = (255,255,255)
    for x,y in path:
        board[x+center,y+center,:] = path_color
#    plt.imshow(board)
#    plt.show(block=False)
    return board

class Game():
    """
    A class which implements the Gobble game. Initializes with a grid_size
    and path_radius. There is an "example" method to illustrate how the
    game is played.
    """
    def __init__(self, grid_size, path_radius):
        self.score = 0
        self.player_color = (255,0,255)
        self.start_game(grid_size, path_radius)
        self.board[0][self.player_pos[0], self.player_pos[1]] = self.player_color
        #self.show_board()
        plt.title("The Gobble Game")

    def start_game(self, grid_size, path_radius):
        """
        Resets the board and player.
        """
        self.board = [draw_board(grid_size, path_radius), grid_size, path_radius]
        self.player_pos = (8,5)

    def show_board(self):
        """
        Throws the current board to the active plot window.
        """
        plt.imshow(self.board[0])
        plt.show(block=False)

    def update_board(self, new_pos, show_plt=False):
        """
        Performs the board update using a desired action (in the form of a
        destination square). Also checks if the game is over. If so, prompts
        the user to end or continue with a new game.
        """
        if self.board[0][new_pos].sum() == 765:
            self.score += 10
        else:
            self.score -= 1
        self.board[0][self.player_pos] = (0,0,0)
        self.board[0][new_pos] = self.player_color
        self.player_pos = new_pos
        if show_plt:
            self.show_board()

        if self.check_end():
            #print(f"Congratulations: Your score is {self.score}.")
            #new_game = str(input("Play Again? (y/n)"))
            #if new_game == 'y':
            #    self.start_game(self.board[1],self.board[2])
            #    self.show_board()
            self.start_game(self.board[1],self.board[2])
            return True
        return False

    def get_actions(self):
        """
        Returns available moves using the current board configuration.
        """
        x,y = self.player_pos
        actions = [(x+1,y), (x+1,y+1), (x,y+1),
                   (x-1,y), (x-1,y-1), (x,y-1)]
        valid = []
        for a in actions:
            try:
                self.board[0][a]
                valid.append(a)
            except:
                pass
        return valid

    def check_end(self):
        """
        Assesses whether all white tiles have been removed.
        """
        if (self.board[0]>self.player_color).any():
            return False
        else:
            return True

    def example(self):
        """
        Illustrates how to play the game.
        """
        while not end:
            plt.pause(0.25)
            end = self.update_board(random.choice(self.get_actions()), True)
