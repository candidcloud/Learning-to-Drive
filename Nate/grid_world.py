import matplotlib.pyplot as plt
import numpy as np
import random

plt.ion()

def draw_board(grid_size, hole_pos):
    board = np.ones((grid_size,grid_size))
    board[hole_pos] = 0
    return board

class Game():
    """
    A class which implements the Gobble game. Initializes with a grid_size
    and path_radius. There is an "example" method to illustrate how the
    game is played.
    """
    def __init__(self, grid_size):
        self.score = 0
        self.grid_size = grid_size
        #self.player_pos = (np.random.randint(grid_size),np.random.randint(grid_size))
        self.start_game(grid_size)
        #self.show_board()
        plt.title("Nate's Lame Game")

    def start_game(self, grid_size):
        self.goal_pos = (0,0)
        self.board = draw_board(grid_size, self.goal_pos)
        self.player_pos = (5,5)
        self.board[self.player_pos] = .5
        
        # self.board[self.player_pos] = .5

    def show_board(self):
        plt.imshow(self.board)

    def update_board(self, new_pos, show_plt=False):
        # if np.sum(np.abs(np.array(new_pos) -  np.array(self.goal_pos))) < np.sum(np.abs(np.array(self.player_pos) -  np.array(self.goal_pos))):
        #     self.score += 1
        # else:
        #     self.score -= 1
        if np.sum(np.abs(np.array(new_pos) -  np.array(self.goal_pos))) == 0:
            self.score  += 1

        self.board[self.player_pos] = 1
        self.board[new_pos] = .5
        self.player_pos = new_pos

        if show_plt:
            self.show_board()
        if self.check_end():
            print('Game over yo')
            self.start_game(self.grid_size)
            return True


        return False

    def get_actions(self):
        x,y = self.player_pos
        actions = [(x+1,y), (x,y+1),
                   (x-1,y), (x,y-1)]

        v_dim = self.board.shape[0]
        valid = []
        for a in actions:
            if a[0] < v_dim and a[1] < v_dim and a[0] > -1 and a[1] > -1:
                valid.append(a)

        return valid


    def check_end(self):
        if self.player_pos == self.goal_pos:
            print('game is finished')
            return True
        else:
            return False

    def example(self):
        """
        Illustrates how to play the game.
        """
        while self.check_end() == False:
            plt.pause(0.25)
            end = self.update_board(random.choice(self.get_actions()), True)

