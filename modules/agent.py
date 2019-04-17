class Agent:

	def __init__(self, width=None, height=None):
		self.width = 0
		self.height = 0
		self.abstract_actions = ["moveLeft", "moveRight", "moveForward", "moveBackward"]