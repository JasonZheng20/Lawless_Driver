# Car Behavior
# TODO: define car behavior and actions here. Import this file to policy.py
MAX_VELOCITY = 4
class car():
	def __init__(self,x,y,destination):
		self.x = x
		self.y = y
		self.destination = destination
		self.velocity = []
		self.velocity.append(0)
		self.velocity.append(0)
		self.crashed = False
		self.done = False
		self.ticks = 0

	def get_ticks(self):
		return self.ticks

	def is_crashed(self):
		return self.crashed

	def is_done(self):
		return self.done

	def position(self):
		return (self.x,self.y)

	def get_destination(self):
		return self.destination

	def get_velocity(self):
		return self.velocity

	def crash(self):
		self.crashed = True
		self.velocity[0] = 0
		self.velocity[1] = 0

	def take_action(self,action):
		if(self.done or self.crashed):
			return
		if(action == 0):
			self.velocity[0] = min(MAX_VELOCITY, self.velocity[0]+1)
		elif(action == 1):
			self.velocity[0] = max(-1*MAX_VELOCITY, self.velocity[0]-1)
		elif(action == 2):
			self.velocity[1] = min(MAX_VELOCITY, self.velocity[1]+1)
		elif(action == 3):
			self.velocity[1] = max(-1*MAX_VELOCITY, self.velocity[1]-1)

	def tick(self):
		self.ticks += 1
		print self.velocity
		new_x = self.x + self.velocity[0]
		new_y = self.y + self.velocity[1]
		new_pos = (new_x,new_y)
		change_x = float(self.velocity[0])/8.0
		change_y = float(self.velocity[1])/8.0
		path = []
		path_x = float(self.x)
		path_y = float(self.y)
		for i in range(9):
			path.append((int(path_x),int(path_y)))
			path_x+=change_x
			path_y+=change_y
		if(new_pos == self.destination and self.velocity[0] == 0 and self.velocity[1] == 0):
			self.done = True
		self.x = new_x
		self.y = new_y
		return path, new_pos





