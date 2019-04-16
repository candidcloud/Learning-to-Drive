import gobble
import random
import matplotlib.pyplot as plt
from tqdm import tqdm

class Agent():
    def __init__(self, Q = {}, policy = 0.5, lr = 0.5, discount = 0.2):
        self.game = gobble.Game(10,3)
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
        #print(max_Q,max_actions,other_actions)
        r = random.random()
        if r > self.policy or other_actions==[]:  # choose optimally
            choice = random.choice(max_actions)
        else:
            choice = random.choice(other_actions)

        return choice

    def evolve(self, choice, show_plt=False):
        old_pos = self.game.player_pos
        old_score = self.game.score
        end = self.game.update_board(choice, show_plt)
        return old_pos, old_score, end

    def get_reward(self, old_score):
        R = self.game.score - old_score
        if R>0:
            R = R*10
        self.reward += R
        return R

    def learn(self, old_pos, R, choice):
        if self.game.player_pos in self.Q:
            self.Q[old_pos][choice] = (1-self.lr)*self.Q[old_pos][choice] + self.lr*R + self.discount*max(self.Q[self.game.player_pos].items(), key=lambda x:x[1])[1]
        else:
            self.Q[old_pos][choice] = (1-self.lr)*self.Q[old_pos][choice] + self.lr*R

    def play(self,epochs):
        rewards = []
        for i in tqdm(range(epochs)):
            end = False
            while not end:
                choice = self.get_action()
                old_pos, old_score, end = self.evolve(choice)
                R = self.get_reward(old_score)
                self.learn(old_pos, R, choice)
            rewards.append(self.reward)
            self.reward = 0
        return rewards

    def play_slow(self):
        end = False
        while not end:
            plt.pause(0.005)
            choice = self.get_action()
            old_pos, old_score, end = self.evolve(choice, True)
            R = self.get_reward(old_score)
            self.learn(old_pos, R, choice)
        R = self.reward
        self.reward = 0
        return R
