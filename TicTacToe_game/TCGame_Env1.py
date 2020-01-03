import numpy as np
import random
#import itertools
from itertools import groupby
from itertools import product
from gym import spaces



class TicTacToe():

    def __init__(self):
        """initialise the board"""
        # initialise state as an array
        self.state = [np.nan for _ in range(9)]  # initialises the board position, can initialise to an array or matrix
        # all possible numbers
        self.all_possible_numbers = [i for i in range(1, len(self.state) + 1)] # , can initialise to an array or matrix

        self.reset()


    def is_winning(self, curr_state):
        """Takes state as an input and returns whether any row, column or diagonal has winning sum
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan]
        Output = False"""
        lines = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for line in lines:
            line_state = curr_state[line[0]] + curr_state[line[1]] + curr_state[line[2]]
            if line_state == 15:
                return True
        return False

    def is_terminal(self, curr_state):
        # Terminal state could be winning state or when the board is filled up
        if self.is_winning(curr_state) == True:
            return True, 'Win'
        elif len(self.allowed_positions(curr_state)) ==0:
            return True, 'Tie'
        else:
            return False, 'Resume'


    def allowed_positions(self, curr_state):
        """Takes state as an input and returns all indexes that are blank"""
        #print(curr_state)
        return [i for i, val in enumerate(curr_state) if np.isnan(val)]


    def allowed_values(self, curr_state):
        """Takes the current state as input and returns all possible (unused) values that can be placed on the board"""
        used_values = [val for val in curr_state if not np.isnan(val)]
        agent_values = [val for val in self.all_possible_numbers if val not in used_values and val % 2 !=0]
        env_values = [val for val in self.all_possible_numbers if val not in used_values and val % 2 ==0]
        return (agent_values, env_values)


    def action_space(self, curr_state):
        """Takes the current state as input and returns all possible actions, i.e, all combinations of allowed positions and allowed values"""
        #print("Action space ->",self.allowed_positions(curr_state))
        agent_actions = product(self.allowed_positions(curr_state), self.allowed_values(curr_state)[0])
        env_actions = product(self.allowed_positions(curr_state), self.allowed_values(curr_state)[1])
        return (agent_actions, env_actions)

    def state_transition(self, curr_state, curr_action):
        """Takes current state and action and returns the board position just after agent's move.
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan], action- [7, 9] or [position, value]
        Output = [1, 2, 3, 4, nan, nan, nan, 9, nan]
        """
        curr_state[curr_action[0]] = curr_action[1]
        return curr_state

    def step(self, curr_state, curr_action):
        """Takes current state and action and returns the next state, reward and whether the state is terminal. Hint: First, check the board position after
        agent's move, whether the game is won/loss/tied. Then incorporate environment's move and again check the board status.
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan], action- [7, 9] or [position, value]
        Output = ([1, 2, 3, 4, nan, nan, nan, 9, nan], -1, False)"""
        reward = -1 # Incorporate the reward of the move agent made
        if self.is_terminal(curr_state)[0] == True and self.is_terminal(curr_state)[1] == 'Win':
            print("$$$   Game over. Agent wins!")
            new_reward = 10 + reward
            return (curr_state,new_reward,True)
        elif self.is_terminal(curr_state)[0] == True and self.is_terminal(curr_state)[1] == 'Tie':
            print("$$$   Game over. It is a tie!")
            new_reward = 0 + reward
            return (curr_state,new_reward,True)
        elif self.is_terminal(curr_state)[0] == False:
            env_action = (np.random.choice(self.allowed_positions(curr_state)), np.random.choice(self.allowed_values(curr_state)[1]))
            #print("ENVIRONMENT: curr_state ->",agent_state,", action->",env_action)
            env_state = self.state_transition(curr_state,env_action)
            if self.is_terminal(env_state)[0] == True and self.is_terminal(env_state)[1] == 'Win':
                print("$$$   Game over. Agent lost!")
                new_reward = -10 + reward
                return (env_state,new_reward,True)
            elif self.is_terminal(env_state)[0] == True and self.is_terminal(env_state)[1] == 'Tie':
                print("$$$   Game over.It is a tie!")
                new_reward = 0 + reward
                return (env_state,new_reward,True)
            elif self.is_terminal(env_state)[0] == False:
                new_reward = reward
                return (env_state,new_reward,False)

    def reset(self):
        return self.state
