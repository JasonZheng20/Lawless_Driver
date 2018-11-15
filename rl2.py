# rl2.py
#==============================================================================#
# Reinforcement Learning Driver Simulator
# v2.0 -- using James Liljenwall's state framework
#==============================================================================#
import sys
import tensorflow as tf
from tensorflow import keras
from Environment import Environment
import numpy as np
import matplotlib.pyplot as plt

score_crash = -6 #TODO: correlate with real life times
score_goal = 1 #TODO: correlate with real life times/income measures
learning_rate = 0.5
discount_factor = 0.95
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
def choose_action(Q, s, score_crash, score_goal):
    exp_arr = dict()
    lambda_v = 1
    actions = [0, 1, 2, 3, 4]
    for action in actions:
        u = 1
        if s in Q and action in Q[s]:
            u = Q[s][action]
        exp_arr[action] = np.exp(lambda_v * np.log(u))
    denominator = sum(exp_arr.values())
    for action in actions:
        exp_arr[action] /= denominator
    a = np.random.choice(exp_arr.keys(), p = exp_arr.values())
    return a
    # TODO: create a heuristic for each agent based on their current location and end goal


def max_Q(s, Q):
    if s in Q and Q[s]:
        return max(Q[s].values())
    return 0


def learn_update(Q, s, s_, a):
    r = 1 #TODO CHANGE
    if s in Q:
        if a in Q[s]:
            change = learning_rate * (r + discount_factor *  max_Q(s_, Q) - Q[s][a])
            Q[s][a] += change
            return change
        else:
            change = learning_rate * (r + discount_factor *  max_Q(s_, Q))
            if change != 0:
                Q[s][a] = change
            return change
    else:
        Q[s] = dict()
        change = learning_rate * (r + discount_factor *  max_Q(s_, Q))
        if change != 0:
            Q[s][a] = change
        return change


# Idea: Train using K-logit model where you only train one car at a time and
# all the other cars are using the previous generation
# TODO: ONLY ASSUMES ONE AGENT, GENERALIZE TO MULTIPLE AGENTS, HOW TO DO Q
def q_learn(num_agents, num_simulations, env):
    Q = dict()
    discount = 0.95
    learning_rate = 0.5
    episode = 0
    while episode < num_simulations:
        env.reset_map() #TODO: replace with hard-reset function
        num_steps = 0
        while(True):
            actions = []
            states = env.get_states()
            for i in xrange(num_agents):
                action = choose_action(Q, str(states[i]), score_crash, score_goal)
                actions.append(action)
    		env.tick(actions)
            states_ = env.get_states()
            for i in xrange(num_agents):
                learn_update(Q, str(states[i]), str(states_[i]), actions[i])
            num_steps += 1
            print "Currently on step #" + str(num_steps)
            if not env.active_cars:
                print 'All Crashed or Terminated'
                break
        episode += 1
    print Q


def t_sampling(num_agents, num_simulations, env):
    pass

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
    grid = []
    env = create_map(map_name, grid, num_agents)
    if simulation_type == 'ql':
        q_learn(num_agents, num_simulations, env)
    # elif simulation_type == 'dqn':
    #     dq_network(num_agents, num_simulations, env)


if __name__ == '__main__':
    main()
