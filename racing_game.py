"""
Main script which implements Q-learning to teach a computer how to drive
around a track quickly.
"""

class Game():
    """
    A class which maintains state, action, reward, policy, and Q variables as
    a game simulation progresses using the class methods provided.
    """

    def __init__():
        state =  # this will be the track with available rewards
        action_parameters =  # tuple or list
        Q =  # dictionary
        policy =  # function
        reward = 0  # accumulates rewards

    def get_action(state, Q, policy, action_parameters):

        return action

    def evolve(state, action):

        return next_state

    def get_reward(state, next_state, action):

        return reward

    def learn(state, next_state, action, Q, reward):

        return Q

    def check_end(next_state):

        return is_end

# Example of how the game should be played
while True:
    game = Game()
    action = game.get_action(game.state, game.Q, game.policy, game.action_parameters)
    next_state = game.evolve(game.state, action)
    reward = game.get_reward(game.state, next_state, action)
    game.Q = game.learn(game.state, next_state, action, game.Q, reward)
    game.reward += reward
    if game.check_end(next_state):
        print(f"End of Game: Total reward is {game.reward}.")
        break
    else:
        game.state = next_state
