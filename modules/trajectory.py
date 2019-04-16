class Trajectory:

	def __init__(self):

		self.turn_actions = ["turnCW", "turnCCW"]
		self.move_actions = ["moveF"]

	def _euclidean_distance(self, state1, state2):
    	return math.sqrt((state1[0]-state2[0])**2 + (state1[1]-state2[1])**2)

	def _calculate_correction_angle(self, current_point):
		distance_error_offset = 1/self._euclidean_distance(current_point, self.to_point)
		angle_correction = math.degrees(math.atan(istance_error_offset))
		return angle_correction

	def _map_to_action(self):
		pass

	def check_correction(self, from_point, to_point, current_point):
		pass

	def plan(self, from_point, to_point, theta):

		# values of theta
		# 	0 - facing north
		# 	90 - facing east
		# 	180 - facing south
		# 	270 - facing west
		# use math.degrees to convert from radian to degrees. example on line number 13

		actions = []

		delta_x = self.to_point[0] - self.from_point[0]
		delta_y = self.from_point[1] - self.to_point[1]

		# case for moving towards north
		if delta_x == 0 and delta_y > 0:
		
		# case for moving towards south
		elif delta_x == 0 and delta_y < 0:

		# case for moving towards east
		elif delta_y == 0 and delta_x > 0:

		# case for moving towards west
		elif delta_y == 0 and delta_x < 0:


