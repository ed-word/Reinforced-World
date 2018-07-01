"""
Game 2048 execution
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import time
import logging
import json

from tensorforce import TensorForceError
from tensorforce.execution import Runner
from tensorforce.agents import Agent, PPOAgent, DQNAgent
from myWorld import myEnv


# python examples/game_2048.py -a examples/configs/ppo.json -n examples/configs/mlp2_network.json

# python examples/game_2048.py -a examples/configs/ppo_cnn.json -n examples/configs/cnn_network_2048.json


def main():
    environment = myEnv()

    def episode_finished(r):
        if r.episode % 10 == 0:
            print(
                "Finished episode {ep} after {ts} timesteps (reward: {reward})".format(ep=r.episode, ts=r.episode_timestep,
                                                                                       reward=r.episode_rewards[-1]))
        return True

    # Network is an ordered list of layers
    network_spec = [dict(type='flatten'), dict(type='dense', size=256), dict(type='dense', size=4)]

    agent = PPOAgent(
        states=environment.states,
        actions=environment.actions,
        network=network_spec,
        memory=dict(
            type='latest',
            include_next_states=False,
            capacity=100000,
        ),
    )


    runner = Runner(
        agent=agent,
        environment=environment,
        repeat_actions=1
    )

    runner.run(
        timesteps=6000000,
        episodes=1000,
        max_episode_timesteps=10000,
        deterministic=False,
        episode_finished=episode_finished
    )

    terminal = False
    state = environment.reset()
    while not terminal:
        action = agent.act(state)
        state, terminal, reward = environment.execute(action)
    environment.print_state()

    runner.close()


if __name__ == '__main__':
    main()
