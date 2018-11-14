# Road Generator
# TODO: Define function to determine maximum speed before spinout at different road conditions per vehicle
# TODO: not quite spinout chance, but spinout coefficient determining relative road safety per condition
class RoadMap():
	def RoadMap(width, height):
		#generate a roadmap with the given width and height randomly
		self.width = width
		self.height = height
		self.generateRoads()
	def RoadMap(grid):
		self.map = grid
		self.height = len(grid)
		self.width = len(grid[0])
	def generateRoads(self):
		self.map = []
		for i in range(self.height):
			self.map.append([])
			for j in range(self.width):
				self.map[i].append(0)
	#print map
	def print_map(self):
		print(self.map)
