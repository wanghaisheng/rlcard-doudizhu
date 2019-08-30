from rlcard.games.blackjack import *
from rlcard.envs.env import Env
from rlcard.games.blackjack.game import BlackjackGame as Game

import random

class BlackjackEnv(Env):
    """
    Blackjack Environment
    """

    def __init__(self):
        self.game = Game()
        #self.player_num = self.game.get_player_num() # get the number of players in the game
        self.player_num = 1 # get the number of players in the game


    def set_agents(self, agents):
        """ Set the agents that will interact with the environment

        Args:
                agents: list of Agent classes; [agents]
        """

        self.agents = agents

    def set_seed(self, seed):
        """ Set the seed 
        Args:
        seed: integer
        """
        random.seed(seed)
        self.game.set_seed(seed)
        print('############### seeded ############')

    def run(self):
        trajectories = [[] for _ in range(self.player_num)]

        # Loop to play the game
        player = self.game.get_player_id() # get the current player id
        state = self.game.get_state(player) # get the state of the first player
        trajectories[player].append(state)
        while not self.game.end():
            #for i in range(6):
            # First, agent plays
            action = self.agents[player].step(state)

            # Second, environment steps
            next_state, next_player = self.game.step(action)
            #print(action, next_state, next_player)

            # Finally, save the data
            trajectories[player].append(action)
            if not self.game.end():
                trajectories[next_player].append(state)
            state = next_state
            player = next_player


        ## add a final state to all the players
        for player in range(self.player_num):
            state = self.game.get_state(player)
            trajectories[player].append(state)

        ### the winner of the game
        if self.game.winner['player'] > self.game.winner['dealer']:
            player_wins = 'win'
        elif self.game.winner['player'] < self.game.winner['dealer']:
            player_wins = 'lose'
        else:
            player_wins = 'tie'
        return trajectories, player_wins


#####################################################################
    # Remove the rewarder for now
    # For later use

    # Then the trajectories look like this:
    # trajectories[0] = [s_0, a_0, s_1, a_1, ...]

    # We reorganize the trajectories with the rewarder
    # And outout:
    # trajectories[0] = [[s, a, s', r]]
    def reorganize(self, trajectories):
        """
                A simple function to add reward to the trajectories.
                The reward is only given in the end of a game,
                i.e. 1 if winning and 0 otherwise
        """
        ### the wiiner of the game
        player_wins = [self.game.is_winner(p) for p in range(self.player_num)]
        #print('######## ', player_wins)
        new_trajectories = [[] for _ in range(self.player_num)]

        for player in range(self.player_num):
            for i in range(0, len(trajectories[player])-2, 2):
                transition = trajectories[player][i:i+3].copy()\
                # Reward. Here, I simply reward at the end of the game
                # TODO: use better rewarder later
                if i < len(trajectories[player]) - 3:
                    reward = self.rewarder.get_reward(0)
                else:
                    reward = self.rewarder.get_reward(player_wins[player])

                transition.append(reward)
                new_trajectories[player].append(transition)
        return new_trajectories











