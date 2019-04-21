import grid_world
import random
import matplotlib.pyplot as plt
import numpy as np

plt.ion()

class Agent():
    def __init__(self, Q = {}, policy = 0.5, lr = 0.5, discount = 0.2):
        self.game = grid_world.Game()
        self.state = self.game.board
        self.actions = self.game.get_actions()
        self.policy = policy
        self.lr = lr
        self.Q = Q
        self.discount = discount
        self.reward = 0

    def get_action(self):
        actions = self.game.get_actions()
        if self.game.player_pos not in self.Q:
            self.Q[self.game.player_pos] = dict.fromkeys(actions,0)

        max_Q = max(self.Q[self.game.player_pos].items(), key=lambda x:x[1])
        max_actions = [i[0] for i in self.Q[self.game.player_pos].items() if i[1]==max_Q[1]]
        other_actions = [i[0] for i in self.Q[self.game.player_pos].items() if i[1]!=max_Q[1]]
        #compute best choice
        coin_flip = np.random.rand()
        if self.policy < coin_flip and max_actions != []:
            choice = random.choice(max_actions)
        elif other_actions != []:
            choice = random.choice(other_actions)
        else:
            choice = random.choice(max_actions)

        return choice

    def evolve(self, choice, show_plt=False):
        old_pos = self.game.player_pos
        end = self.game.update_board(choice, show_plt)
        return old_pos, end


    def get_reward(self, choice):
        if np.sum(np.abs(np.array(choice) -  np.array(self.game.goal_pos))) < np.sum(np.abs(np.array(self.game.player_pos) -  np.array(self.game.goal_pos))):
            if np.sum(np.abs(np.array(choice) -  np.array(self.game.goal_pos))) ==1:
                R = 100
            else:
                R = 1
        # elif np.sum(np.abs(np.array(choice) -  np.array(self.game.goal_pos))) ==1:
        #     R = 100
        else:
            R = -0.1
            
        self.reward += R
        return R


    def learn(self, old_pos, R, choice):
        if self.game.player_pos in self.Q:
            self.Q[old_pos][choice] = (1-self.lr)*self.Q[old_pos][choice] + self.lr*R + self.discount*max(self.Q[self.game.player_pos].items(), key=lambda x:x[1])[1]
        else:
            self.Q[old_pos][choice] = (1-self.lr)*self.Q[old_pos][choice] + self.lr*R

    def play(self,epochs):
        rewards = []
        for i in range(epochs):
            end = False
            while not end:
                choice = self.get_action()
                old_pos, end = self.evolve(choice)
                R = self.get_reward(choice)
                self.learn(old_pos, R, choice)
            rewards.append(self.reward)
            self.reward = 0
        return rewards


    def play_slow(self):
        end = False
        while not end:
            plt.pause(0.5)
            choice = self.get_action()
            old_pos, end = self.evolve(choice, True)
            R = self.get_reward(choice)
            self.learn(old_pos, R, choice)
        R = self.reward
        self.reward = 0
        return R


