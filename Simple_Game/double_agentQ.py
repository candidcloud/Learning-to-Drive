import tracker as imported_game
import random
import matplotlib.pyplot as plt
from tqdm import tqdm

class Agent():
    """
    A class implementation of the Q-learning algorithm. This class first
    creates a local instance of the imported game, sets defaults for the
    Q-learning algorithm, and defines methods which act on the game instance.
    The imported_game is assumed to have similar attributes and methods to the
    gobble or tracker game.
    """
    def __init__(self, Q = [{},{}], policy = 0.25, lr = 0.5, discount = 0.2):
        """
        Initializes game and Q-learning attributes.
        """
        self.game = imported_game.Game(10,3)
        self.state = self.game.board
        self.actions = self.game.get_actions()
        self.policy = policy
        self.lr = lr
        self.Q = Q
        self.discount = discount
        self.reward = 0

    def get_action(self):
        """
        Chooses an action from the game's get_actions() method using the
        current Q-learning policy.
        """
        actions = self.game.get_actions()
        if self.game.player_pos not in self.Q[0]:
            self.Q[0][self.game.player_pos] = dict.fromkeys(actions,0)
        if self.game.player_pos not in self.Q[1]:
            self.Q[1][self.game.player_pos] = dict.fromkeys(actions,0)

        avgQ = { k : (self.Q[0][self.game.player_pos][k] + self.Q[1][self.game.player_pos][k])/2 for k in self.Q[0][self.game.player_pos].keys() }
        max_Q = max(avgQ.items(), key=lambda x:x[1])
        max_actions = [i[0] for i in avgQ.items() if i[1]==max_Q[1]]
        #other_actions = [i[0] for i in self.Q[self.game.player_pos].items() if i[1]!=max_Q[1]]

        r = random.random()
        if r > self.policy:  # choose optimally
            choice = random.choice(max_actions)
        else:
            choice = random.choice(actions)

        return choice

    def evolve(self, choice):
        """
        Updates the game and records the previous board position with the
        previous score. Also runs a check_end() method on the game for
        returning a boolean affirming or denying that the game has ended.
        """
        old_pos = self.game.player_pos
        old_score = self.game.score
        self.game.update_board(choice)
        end = self.game.check_end()
        return old_pos, old_score, end

    def get_reward(self, old_score):
        """
        Allocate a reward to the agent based on the difference in current and
        previous game scores. Returns the reward change for use in learning.
        """
        R = self.game.score - old_score
        if R > 0:
            self.reward += R
        else:
            R = 1/(1+abs(R))
            self.reward += R
        return R

    def double_learn(self, old_pos, R, choice):
        """
        Uses the double Q-learning formula to update the Q-tables for the last
        state and action combination. Expects as input the reward returned
        from the agent's get_reward() method.
        """
        if random.random() < 0.5:
            self.updateQ(0, old_pos, R, choice)
        else:
            self.updateQ(1, old_pos, R, choice)

    def updateQ(self, idx, old_pos, R, choice):
        """
        Uses the Q-learning formula to update the Q-table for the last state
        and action combination. Expects as input the reward returned from the
        agent's get_reward() method.
        """
        other_idx = (idx + 1) % 2
        if self.game.player_pos in self.Q[idx]:
            self.Q[idx][old_pos][choice] = ( (1-self.lr)*self.Q[idx][old_pos][choice] + self.lr*(R
                                            + self.discount*max(self.Q[other_idx][self.game.player_pos].items(), key=lambda x:x[1])[1]) )
        else:
            self.Q[idx][old_pos][choice] = (1-self.lr)*self.Q[idx][old_pos][choice] + self.lr*R

        normalizer = sum(self.Q[idx][old_pos].values())
        if normalizer > 1:
            for key in self.Q[idx][old_pos]:
                self.Q[idx][old_pos][key] = self.Q[idx][old_pos][key]/normalizer

    def play(self,epochs):
        """
        Replays the local game instance for a given number of epochs. At the
        end of each game, the cumulative score (not agent reward) is appended
        to a list which is then returned after all epochs have been run.
        """
        scores = []
        self.reward = 0
        for i in tqdm(range(epochs)):
            end = False
            self.game.start_game()
            while not end:
                choice = self.get_action()
                old_pos, old_score, end = self.evolve(choice)
                R = self.get_reward(old_score)
                self.double_learn(old_pos, R, choice)
            scores.append(self.game.score)
            self.reward = 0
        return scores

    def play_slow(self):
        """
        Plays one game from start to finish, plotting the board for each
        move. Note that the agent does learn when this is run. Returns
        the cumulative reward for the game.
        """
        end = False
        plt.figure()
        plt.title("Tracker Game")
        self.game.start_game()
        self.reward = 0
        while not end:
            self.game.show_board()
            plt.pause(0.05)
            choice = self.get_action()
            old_pos, old_score, end = self.evolve(choice)
            R = self.get_reward(old_score)
            self.double_learn(old_pos, R, choice)
        R = self.reward
        self.reward = 0
        return R
