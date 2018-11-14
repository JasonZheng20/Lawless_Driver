# rl2.py
#==============================================================================#
# Reinforcement Learning Driver Simulator
# v2.0 -- using James Liljenwall's state framework
#==============================================================================#
import sys
import tensorflow as tf
from tensorflow import keras
from environment import Environment
import numpy as np
import matplotlib.pyplot as plt
#==============================================================================#
# Utilities
#==============================================================================#
def create_map(file_name, grid, num_cars):
    file = open(file_name, "r")
    for line in file:
        new_line = []
        parts = line.split(" ")
        for part in parts:
            new_line.append(int(part))
        grid.append(new_line)
    env = Environment(num_cars, grid = grid)
    return env

#==============================================================================#
# Reinforcement learning
#==============================================================================#
# Choose an action based on the observable state space
def choose_action(env, score_crash, score_goal):
    action_space = [0, 1, 2, 3, 4]
    action = np.random.choice(action_space)
    return action
    # TODO: create a heuristic for each agent based on their current location and end goal


# Idea: Train using K-logit model where you only train one car at a time and
# all the other cars are using the previous generation
# TODO: ONLY ASSUMES ONE AGENT, GENERALIZE TO MULTIPLE AGENTS, HOW TO DO Q
def q_learn(num_agents, num_simulations, env, score_crash, score_goal):
    Q = dict()
    discount = 0.95
    learning_rate = 0.5
    episode = 0
    while episode < num_simulations:
        num_steps = 0
        while(True):
            actions = []
            for i in xrange(num_agents):
                action = choose_action(env, score_crash, score_goal)
                actions.append(action)
    		env.tick(actions)
            # for i in xrange(num_cars):
            #     # current_car_action = actions[i]
            #     state_, reward = observe_update(env)
            #     learn_update(Q, state_, reward, actions[i], env)
            num_steps += 1
            print num_steps
            if not env.active_cars:
    			break
        episode += 1

#==============================================================================#
# Main
#==============================================================================#
def main():
    if len(sys.argv) != 5:
        raise Exception("usage: num_agents, map, num_simulations (ql | dqn)")
    num_agents = int(sys.argv[1])
    map_name = sys.argv[2]
    num_simulations = int(sys.argv[3])
    simulation_type = sys.argv[4]
    score_crash = -6 #TODO: correlate with real life times
    score_goal = 1 #TODO: correlate with real life times/income measures
    grid = []
    env = create_map(map_name, grid, num_agents)
    if simulation_type == 'ql':
        q_learn(num_agents, num_simulations, env, score_crash, score_goal)
    # elif simulation_type == 'dqn':
    #     dq_network(num_agents, num_simulations, env, score_crash, score_goal)


if __name__ == '__main__':
    main()
