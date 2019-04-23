class Agent:

	def __init__(self, len_x, len_y, linear_velocity, angular_velocity):
		self.len_x = len_x
		self.len_y = len_y
		self.linear_velocity = linear_velocity
		self.angular_velocity = angular_velocity
		self.linear_noise_std = 1
		self.angular_noise_std = 5

	def distance_to_time(self, distance):
		return distance/self.linear_velocity

	def angle_to_time(self, angle):
		return angle/self.angular_velocity