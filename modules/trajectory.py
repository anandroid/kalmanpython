class Trajectory:

	def __init__(self, from_point, to_point, init_theta):
		
		self.from_point = from_point
		self.to_point = to_point
		self.init_theta = init_theta

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

	def check_correction(self, current_point):
		pass

	def plan(self):
		pass