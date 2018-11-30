from random import random
class ValueIteration:
	# Variables:
	# discount: the discount factor for future rewards
	# t_probs: stores the probability of tranistioning to next state from state, action
	# rewards: stores the expected rewards for a particular state
	# action_rewards: stores the rewards for a state, action, next staet group
	# prev_states: stores the previous states from a given state to allow for easier iterations

	#initialize the values to be everything empty
	#set the discount to be appropriate
	def __init__(self, discount):
		self.discount = discount
		self.policy = {}
		self.t_probs = {}
		self.rewards = {}
		self.action_rewards = {}
		self.prev_states = {}

	#take in a run summary of the format (state, action, next state, reward)
	def update(self, all_runs):
		for run in all_runs:
			self.update_single_car(run)

	def update_single_car(self, run_summary):
		for summary in run_summary:
			#get the values for each state
			state = summary[0]
			action = summary[1]
			next_state = summary[2]
			reward = summary[3]
			#update the rewards
			self.action_rewards[(state,action,next_state)] = reward
			#if the state is unseen, create an entry for it
			if(not state in self.t_probs):
				self.t_probs[state]={}
			#if the action has not been performed before add it
			if(not action in self.t_probs[state]):
				self.t_probs[state][action] = {}
				self.t_probs[state][action]["total"]=0.0
			#update the total number of actions and the transition from this action
			self.t_probs[state][action]["total"] += 1
			self.t_probs[state][action][next_state] = self.t_probs[state][action].get(next_state,0) +1
			#update previous states (no reason to do checks for already existing)
			if(not next_state in self.prev_states):
				self.prev_states[next_state] = {}
			self.prev_states[next_state][state] = 1
	#return the optimal policy or -1 if unseen state
	def get_action(self, state):
		if(state in self.policy):
			return self.policy[state]
		else:
			return -1


	#calculate the rewards for each state
	def do_iterations(self, iterations=3000):
		check_states = self.t_probs.keys()
		for i in range(iterations):
			changed_states = {}
			for state in check_states:
				best_action = 4
				best_rewards = -9999999999
				for action in self.t_probs[state]:
					reward = 0
					for next_state in self.t_probs[state][action]:
						if(next_state == "total"):
							continue
						prob = self.t_probs[state][action][next_state]/self.t_probs[state][action]["total"]
						reward += prob *float(self.action_rewards.get((state,action,next_state),0) +
								self.discount * self.rewards.get(next_state,0))
					if(reward > best_rewards):
						best_rewards = reward
						best_action = action
				if(self.policy.get(state,-1) != best_action):
					changed_states[state] = abs(best_rewards-self.rewards.get(state,0))
				self.policy[state] = best_action
				self.rewards[state] = best_rewards
		total = float(len(changed_states))
		check_states = []
		#priority trick:
		#just update the states with the most change to reduce size
		if(total <= 100 or i%1000 == 0):
			check_states = self.t_probs.keys()
		else:
			avg = 0.0
			alt_set = {}
			for val in changed_states:
				avg += changed_states[val]
			avg = avg/total
			for state in changed_states:
				if(changed_states[state]>=avg):
					for prev in self.prev_states[state]:
						alt_set[prev]=1
			check_states = alt_set.keys()


















