import Environment as en
import VI as vi 
from random import random
import sys
def main():
	#initialize the environment
	env = None
	num_cars, grid = get_input()
	env = en.Environment(num_cars,grid=grid)	
	run_learning(env,num_cars)

#get the input from the user
def get_input():
	#check if the given files are correct
	if(len(sys.argv) == 3):
		file_name = sys.argv[1]
		num_cars = int(sys.argv[2])
		grid = []
		#turn the file into a grid that can be used
		file = open(file_name, "r")
		for line in file:
			new_line = []
			parts = line.split(" ")
			for part in parts:
				new_line.append(int(part))
			grid.append(new_line)
		return num_cars, grid
	else:
		raise Exception("usage: python VI_runner.py grid_file num_cars")

def run_learning(env,num_cars):
	#initialize Value iteration with discount of 1
	valIter = vi.ValueIteration(.95)
	time = 0
	#keep track of the run summary to do Value Iteration after each Run
	prev_states = env.get_states()
	run_summary = create_run_summary(num_cars)
	num_complete = 0
	search_prob = .6
	while(num_complete < 20000):
		time+=1
		actions = get_actions(prev_states, valIter,search_prob)
		# print("actions" + str(actions))
		env.tick(actions)
		#update the run summary
		next_states = env.get_states()
		end = (env.is_done() or time >= 1000)
		rewards = env.get_rewards(end = end)
		for i in range(num_cars):
			run_summary[i].append((prev_states[i],actions[i],next_states[i],rewards[i]))
		if(end):
			print("New Run " + str(num_complete))
			search_prob = search_prob * .999
			num_complete +=1
			time = 0
			env.hard_reset()
			valIter.update(run_summary)
			if(num_complete%20 == 0):
				valIter.do_iterations()
			run_summary = create_run_summary(num_cars)

def get_actions(states, valIter, search_prob):

	actions = []
	for state in states:
			action = valIter.get_action(state)
			if(action == -1 or random() <=search_prob):
				action = int(random()*5)
			actions.append(action)
	return actions

def create_run_summary(num_cars):
	run_summary = []
	for i in range(num_cars):
		run_summary.append([])
	return run_summary
if __name__ == '__main__':
    main()





