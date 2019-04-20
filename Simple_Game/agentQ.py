import tracker
import random
import matplotlib.pyplot as plt
from tqdm import tqdm

class Agent():
    def __init__(self, Q = {}, policy = 0.25, lr = 0.5, discount = 0.2):
        self.game = tracker.Game(10,3)
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

        r = random.random()
        if r > self.policy or other_actions==[]:  # choose optimally
            choice = random.choice(max_actions)
        else:
            choice = random.choice(other_actions)

        return choice

    def evolve(self, choice):
        old_pos = self.game.player_pos
        old_score = self.game.score
        self.game.update_board(choice)
        end = self.game.check_end()
        return old_pos, old_score, end

    def get_reward(self, old_score):
        R = self.game.score - old_score
        if R > 0:
            self.reward += R
        else:
            R = 1/(1+abs(R))
            self.reward += R
        return R

    def learn(self, old_pos, R, choice):
        if self.game.player_pos in self.Q:
            self.Q[old_pos][choice] = (1-self.lr)*self.Q[old_pos][choice] + self.lr*R + self.discount*max(self.Q[self.game.player_pos].items(), key=lambda x:x[1])[1]
        else:
            self.Q[old_pos][choice] = (1-self.lr)*self.Q[old_pos][choice] + self.lr*R

        normalizer = sum(self.Q[old_pos].values())
        if normalizer > 1:
            for key in self.Q[old_pos]:
                self.Q[old_pos][key] = self.Q[old_pos][key]/normalizer

    def play(self,epochs):
        scores = []
        for i in tqdm(range(epochs)):
            end = False
            self.game.start_game()
            while not end:
                choice = self.get_action()
                old_pos, old_score, end = self.evolve(choice)
                R = self.get_reward(old_score)
                self.learn(old_pos, R, choice)
            scores.append(self.game.score)
            self.reward = 0
        return scores

    def play_slow(self):
        end = False
        plt.figure()
        plt.title("Tracker Game")
        self.game.start_game()
        while not end:
            self.game.show_board()
            plt.pause(0.05)
            choice = self.get_action()
            old_pos, old_score, end = self.evolve(choice)
            R = self.get_reward(old_score)
            self.learn(old_pos, R, choice)
        R = self.reward
        self.reward = 0
        return R
