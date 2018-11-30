import car as Car
import sys
import math as math
import random as rand
import numpy as np

FREE = 0
BUILDING = 1
CAR = 2
TEMP_CAR = 3
CRASH = 4
DESTINATION_MARKER = 5
CRASH_TIMER = 8
REWARD_VAL = 10000
# ANY non 1 2 3 4 action is no action

class Environment():
	def __init__(self,num_cars, grid = None, width = 10, height = 10):
		if(grid != None):
			self.map = grid
			self.other_init(len(grid), len(grid[0]), num_cars)
		else:
			self.generate_map(width,height)
			self.other_init(height,width,num_cars)

	def other_init(self, height, width, num_cars):
		self.height = height
		self.width = width
		self.active_cars = num_cars
		self.num_cars = num_cars
		self.crashed_cars = {}
		self.assign_cars()
		# self.print_map()
		self.finished_cars = {}

	def hard_reset(self):
		for i in range(self.height):
			for j in range(self.width):
				val = self.map[i][j]
				if(val == CAR or val == TEMP_CAR or val == CRASH):
					self.map[i][j] = FREE
		self.active_cars = self.num_cars
		self.crashed_cars = {}
		self.assign_cars()
		# self.print_map()
		self.finished_cars = {}


	def assign_cars(self):
		self.cars = []
		start_locations = {}
		end_locations = {}
		for i in range(self.num_cars):
			x = int(rand.random()*self.height)
			y = int(rand.random()*self.width)
			while(self.map[x][y] != FREE or (x,y) in start_locations):
				x = int(rand.random()*self.height)
				y = int(rand.random()*self.width)
			start_locations[(x,y)] = 0
			end_x = int(rand.random()*self.height)
			end_y = int(rand.random()*self.width)
			while(self.map[end_x][end_y] != FREE or (end_x,end_y) in end_locations):
				end_x = int(rand.random()*self.height)
				end_y = int(rand.random()*self.width)
			end_locations[(end_x,end_y)] = 0
			temp = Car.car(x,y,(end_x,end_y))
			self.cars.append(temp)


	def is_done(self):
		for car in self.cars:
			if(not (car.is_done() or car.is_crashed())):
				return False
		return True

	def generate_map(self, width, height):
		self.width = width
		self.height = height
		self.map = []
		for i in range(height):
			self.map.append([])
			for j in range(width):
				self.map[i].append(FREE)

	def print_map(self):
		print("")
		for i in range(self.height):
			print(self.map[i])
		print("")

	#tick to update the position of all of the cars
	def tick(self, actions):
		self.car_locations = {}
		for i in range(self.height):
			for j in range(self.width):
				if(self.map[i][j] == CAR):
					self.map[i][j] = FREE
		self.assign_act(actions)
		self.perform_act()
		# self.print_map()
		self.reset_map()
		active = 0
		for i in range(self.num_cars):
			car = self.cars[i]
			if(not(car.is_done() or car.is_crashed())):
				active += 1
		self.active_cars = active


	#remove all of the cars from the map and update the crashed cars
	def reset_map(self):
		for i in range(self.height):
			for j in range(self.width):
				if(self.map[i][j] == TEMP_CAR):
					self.map[i][j] = FREE
				elif(self.map[i][j] == CRASH):
					time = self.crashed_cars[(i,j)]
					if(time == 0):
						self.map[i][j] = FREE
					else:
						self.crashed_cars[(i,j)] = time-1

	def assign_act(self, actions):
		for i in range(len(self.cars)):
			car = self.cars[i]
			car.take_action(actions[i])

	def perform_act(self):
		for i in range(len(self.cars)):
			car = self.cars[i]
			if(car.is_crashed() or car.is_done()):
				continue
			path, new_pos = car.tick()
			if(self.check_crash(path,new_pos)):
				car.crash()
			else:
				self.update_map(path,new_pos, i)
	#check if anything on the path is not free, if there is a car crash it
	def check_crash(self, path, new_pos):
		for pos in path:
			x = pos[0]
			y = pos[1]
			val = self.map[x][y]
			if(val != FREE):
				if(val == CAR or val == TEMP_CAR):
					car = self.cars[self.car_locations[pos]]
					car.crash()
					final_pos = car.position()
					self.map[final_pos[0]][final_pos[1]] = FREE
				if(val != BUILDING):
					self.crashed_cars[pos] = CRASH_TIMER
					self.map[x][y] = CRASH
				self.active_cars -= 1
				# elif (val == BUILDING):
				# 	self.crashed_cars[pos]
				return True
		x = new_pos[0]
		y = new_pos[1]
		val = self.map[x][y]
		if(val != FREE):
			if(val == CAR or val == TEMP_CAR):
				car = self.cars[self.car_locations[(pos)]]
				car.crash()
				final_pos = car.position()
				self.map[final_pos[0]][final_pos[1]] = FREE
			return True
		return False

	def update_map(self, path, new_pos, i):
		for pos in path:
			x = pos[0]
			y = pos[1]
			self.map[x][y] = TEMP_CAR
			self.car_locations[(x,y)] = i
		x = new_pos[0]
		y = new_pos[1]
		self.map[x][y] = CAR
		self.car_locations[(x,y)] = i

	def get_states(self):
		states = []
		for car in self.cars:
			state = []
			pos = car.position()
			x = pos[0]
			y = pos[1]
			dest = car.get_destination()
			vel = car.get_velocity()
			x_dest = dest[0]
			y_dest = dest[1]
			dist = (max(-10,min(x_dest-x,10)),max(-10,min(y_dest-y,10)))
			state.append(vel)
			state.append(dist)
			if(car.is_crashed()):
				state.append(0)
			else:
				state.append(1)
			view = []
			for i in range(x-4,x+5):
				view.append([])
				for j in range(y-4,y+5):
					if(i < 0 or j < 0 or i >= self.height or j >= self.width):
						view.append(1)
					elif(i == x_dest and j == y_dest):
						view.append(DESTINATION_MARKER)
					else:
						view.append(self.map[i][j])
			state.append(view)
			states.append(str(state))
		return states

	def get_rewards(self, end = False):
		rewards = []
		for i in range(self.num_cars):
			if(i in self.finished_cars):
				rewards.append(0)
				continue
			car = self.cars[i]
			rew = 0
			if(car.is_done()):
				rew = REWARD_VAL *(1.0+ 1.0/(1+np.exp(car.get_ticks()/8)))
				self.finished_cars[i] = 0
			elif(car.is_crashed()):
				rew = -1 * REWARD_VAL *(1.0+ 1.0/(1+np.exp(car.get_ticks()/8)))
				self.finished_cars[i] = 0
			elif(end):
				pos = car.position()
				dest = car.get_destination()
				distance = math.sqrt((pos[0]-dest[0])**2 + (pos[0]-dest[0])**2)
				rew = (REWARD_VAL/10.0) *(1.0/(1+np.exp(distance/8)))
			rewards.append(rew)
		return rewards




def main():
	env = None
	num_cars = 0
	if(len(sys.argv) == 4):
		height = int(sys.argv[1])
		width = int(sys.argv[2])
		num_cars = int(sys.argv[3])
		env = Environment(num_cars, width = width,height = height)
	elif(len(sys.argv) == 3):
		file_name = sys.argv[1]
		num_cars = int(sys.argv[2])
		grid = []
		file = open(file_name, "r")
		for line in file:
			new_line = []
			parts = line.split(" ")
			for part in parts:
				new_line.append(int(part))
			grid.append(new_line)
		env = Environment(num_cars, grid = grid)
	else:
		raise Exception("usage: python environment.py height width num_cars\nor\npython environment.py grid_file num_cars")

	while(True):
	# for i in xrange(2):
		actions = []
		for i in range(num_cars):
			actions.append(int(input("car " + str(i) + " action: ")))
		# print("mom" + str(actions))
		env.tick(actions)
		print env.active_cars
		if not env.active_cars:
			print 'All crashed!'
			break


if __name__ == '__main__':
    main()
