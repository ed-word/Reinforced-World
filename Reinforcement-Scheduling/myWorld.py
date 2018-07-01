
"""Game class to represent 2048 game state."""


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensorforce.environments import Environment
import numpy as np

dist = []
ACTION_NAMES = ["left", "up", "right", "down"]
ACTION_LEFT = 0
ACTION_UP = 1
ACTION_RIGHT = 2
ACTION_DOWN = 3
dep_cout = 0

class myEnv(Environment):
    """
    Represents a 2048 Game state and implements the actions.
    Most of this code comes from https://github.com/georgwiese/2048-rl/blob/master/py_2048_rl/game/game.py .
    Which implements the 2048 Game logic, as specified by this source file:
    https://github.com/gabrielecirulli/2048/blob/master/js/game_manager.js
    Game states are represented as shape (4, 4) numpy arrays whos entries are 0
    for empty fields and ln2(value) for any tiles.
    """

    def __str__(self):
        self.print_state()

    def reset(self):
        self.__init__()
        return self._state

    def execute(self, actions):
        reward = 0
        global dep_cout
        dep_cout+=1
        # Terminal
        terminal = self.game_over()
        if terminal:
            return self._state, terminal, reward

        # Valid action
        action_available = self.is_action_available(actions)

        if not action_available:
            return self._state, terminal, reward

        reward = self.do_action(actions)
        return self._state, terminal, reward


    @property
    def states(self):
        return dict(shape=self._state.shape, type='float32')

    @property
    def actions(self):
        return dict(num_actions=len(ACTION_NAMES), type='int')

    def __init__(self, state=None, initial_score=0):
        global dep_cout,dist
        self._score = initial_score
        dep_cout = 0
        dist = np.random.random_integers(0, 3, 500)
        if state is None:
            self._state = np.zeros((31, 31, 5), dtype=np.int)
            self._state[0][0][0] = 1

        else:
            self._state = state

    def copy(self):
        """Return a copy of self."""

        return MyEnv(np.copy(self._state), self._score)

    def game_over(self):
        """Whether the game is over."""
        global dep_cout
        if dep_cout < 500:
            return False
        return True

    def available_actions(self):
        """Computes the set of actions that are available."""
        return [action for action in range(4) if self.is_action_available(action)]

    def is_action_available(self, action):
        """Determines whether action is available.
        That is, executing it would change the state.
        """
        for i in range(31):
            for j in range(31):
                if self._state[i][j][0] == 1:
                    if action == 0 and j != 0:
                        return True
                    elif action == 1 and i != 0:
                        return True
                    elif action == 2 and j != 30:
                        return True
                    elif action == 3 and i != 30:
                        return True
                    else:
                        return False



    def do_action(self, action):
        """Execute action, add a new tile, update the score & return the reward."""
        global dep_cout
        global dist
        c_x = 0
        c_y = 0
        for i in range(31):
            for j in range(31):
                if self._state[i][j][0] == 1:
                    if action == 0:
                        c_x = j - 1
                    elif action == 1:
                        c_y = i - 1
                    elif action == 2:
                        c_x = j + 1
                    elif action == 3 :
                        c_y = i + 1
                    self._state[i][j][0] = 0

        if self._state[c_x][c_y][1] == 1:
            reward = 100*self._state[c_x][c_y][2] + 100*self._state[c_x][c_y][3]
        else:
            reward = -1
        self._state[c_x][c_y][0] = 1
        self._state[c_x][c_y][1] = 0
        self._state[c_x][c_y][2] = 0
        self._state[c_x][c_y][3] = 0
        self._state[c_x][c_y][4] = 0
        x_t = set()
        y_t = set()
        if dep_cout < len(dist):
            if dist[dep_cout] > 0 :
                for i in range(dist[dep_cout]):
                    x1 = np.random.randint(0,30)
                    y1 = np.random.randint(0,30)
                    while x_t.__contains__(x1):
                        x1 = np.random.randint(0, 30)
                    while y_t.__contains__(y1):
                        y1 = np.random.randint(0, 30)
                    self._state[x1][y1][0] = 0
                    self._state[x1][y1][1] = 1
                    self._state[x1][y1][2] = np.random.randint(1,5)
                    self._state[x1][y1][3] = np.random.randint(1,3)
                    self._state[x1][y1][4] = 0

        return reward


    def print_state(self):

        for i in range(31):
            s = ''
            for j in range(31):
                s += '{'
                for k in range(5):
                    s += str(self._state[i][j][k])
                    s += ' '
                s += '}'
            print(s)

    def state(self):
        """Return current state."""
        return self._state

    def score(self):
        """Return current score."""
        return self._score

    def render(self):
        self.print_state()