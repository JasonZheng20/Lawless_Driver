# rl.py
#==============================================================================#
# Reinforcement Learning
# Driver Simulator
# We are using a Q-Learning algorithm with Deep Neural Net Global Approximator
# References:
# https://storage.googleapis.com/deepmind-media/dqn/DQNNaturePaper.pdf (DQN)
# https://towardsdatascience.com/introduction-to-various-reinforcement-learning-algorithms-i-q-learning-sarsa-dqn-ddpg-72a5e0cb6287 (side reading)
# https://towardsdatascience.com/welcome-to-deep-reinforcement-learning-part-1-dqn-c3cab4d41b6b (More on DQN)
# https://medium.com/@awjuliani/simple-reinforcement-learning-with-tensorflow-part-4-deep-q-networks-and-beyond-8438a3e2b8df (Tensorflow and DQN, and experience replay)
# https://medium.com/tensorflow/training-and-serving-ml-models-with-tf-keras-fd975cc0fa27 (creating neural net)
# https://medium.com/emergent-future/simple-reinforcement-learning-with-tensorflow-part-0-q-learning-with-tables-and-neural-networks-d195264329d0 (Tensorflow and DQN pt 1)
#==============================================================================#
import sys
import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
#==============================================================================#
# Classes
#==============================================================================#
# Class defining randomly generated cars and their associated fields
class agent():
    def __init__(self, map):
        self.actions = ['left', 'right', 'accelerate', 'brake'] #TODO: how to implement this so simultaneous actions are ok
        self.gas = np.random.randint(10, 35) # According to rough estimates from https://itstillruns.com/average-size-automobile-gas-tank-6787985.html
        self.start = get_unique_random_location(map)
        self.end = get_unique_random_location(map)
        self.x = self.start
        self.y = self.end
        self.angle = 0

class state():
    def __init__(self):
        self.agents = None # TODO: track positions and active/terminated

# Class defining a single simulation runtime given a map and a number of agents
class simulation():
    def __init__(self, agents, map):
        self.num_agents = len(agents)
        self.active_agents = agents
        self.terminated_agents = set()
        self.map = map

    def reset():
        pass
        # TODO. use tf

    def run():
        pass
        # inputs1 = tf.placeholder(shape=[1,16],dtype=tf.float32)
        # action = choose_action()
        # sp, reward, end = take_action(action)
        # learn_Q(s, action, reward, sp)
        # s = sp
        # if end: break
        # it is an end state if it crashes into a wall or another car or reaches the goal or runs out of gas

    def crash():
        pass

# Class defining a map and its associated fields
class map():
    def __init__(self):
        self.available_spaces = set()
        self.taken_spaces = set()
        # Other fields for James to Define

    def get_unique_random_location(map):
        choice = np.random.choice(self.availabe_spaces)
        self.available_spaces.remove(choice)
        self.taken_spaces.add(choice)
        return choice

#==============================================================================#
# Reinforcement Learning Algorithms
#==============================================================================#
def initialize_agents(self, map, num_agents):
    return set(agent(map) for i in xrange(num_agents))


# Regular Q Learning with Local Approximation
def q_learn(num_agents, num_simulations, map, score_crash, score_goal):
    Q = dict()
    agents = initialize_agents(map, num_agents)
    iter = 0
    simulation = simulation(agents, map)
    while iter < num_simulations:
        simulation.reset()
        simulation.run() #TODO check how this was done in 221 car
            # for agent in active_agents:
                # do a step for that agent, wait will this imply all cars will work together? do I need to run them seperately?
            # pass
            # run the simulation, incrementing num_terminated_agents in crash or goal
        iter += 1


# Deep Q Learning using Multi-layered CNN with Experience Replay
def dq_network(num_agents, num_simulations, map, score_crash, score_goal):
    convolution_layer = tf.contrib.layers.convolution2d(inputs,num_outputs,kernel_size,stride,padding)
    agents = initialize_agents(map, num_agents)
    simulation = 0
    while simulation < num_simulations:
        simulation = simulation()
        simulation.run()
        simulation += 1
    # Uses a Neural Network to predict Q at each step


def t_sampling(num_agents, num_simulations, map, score_crash, score_goal):
    pass


# Dueling Deep Q Learning using Multi-layered CNN
def ddq_network(num_agents, num_simulations, map, score_crash, score_goal):
    pass
    # Does value iteration across all agents to find a global maximum

#==============================================================================#
# Main
#==============================================================================#
def main():
    if len(sys.argv) != 4:
        raise Exception("usage: num_agents, num_simulations (ql | dqn)")
    num_agents = int(sys.argv[1])
    num_simulations = int(sys.argv[2])
    simulation_type = sys.argv[3]
    score_crash = -6 #TODO: correlate with real life times
    score_goal = 1 #TODO: correlate with real life times/income measures
    map = create_map()
    if simulation_type == 'ql':
        q_learn(num_agents, num_simulations, map, score_crash, score_goal) #TODO: put these values in a class
    elif simulation_type == 'dqn':
        dq_network(num_agents, num_simulations, map, score_crash, score_goal)


if __name__ == '__main__':
    main()
