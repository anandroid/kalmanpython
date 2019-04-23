import math

def _euclidean_distance(state1, state2):
	 return math.sqrt((state1[0]-state2[0])**2 + (state1[1]-state2[1])**2)

def _dot_product(v1, v2):
	return sum((a*b) for a, b in zip(v1, v2))

def _length(v):
	return math.sqrt(_dot_product(v, v))

def _angle(v1, v2):
	return math.degrees(math.acos(_dot_product(v1, v2) / (_length(v1) * _length(v2))))

def get_quadrant(from_point, to_point):

	new_to_point = (to_point[0]-from_point[0], to_point[1]-from_point[1])
	if new_to_point[0] >= 0 and new_to_point[1] >= 0: return 1
	elif new_to_point[0] <= 0 and new_to_point[1] >= 0: return 2
	elif new_to_point[0] <= 0 and new_to_point[1] <= 0:	return 3
	elif new_to_point[0] >= 0 and new_to_point[1] <= 0: return 4

def plan(from_point, to_point, theta):

	actions = []

	unit_vector = [math.cos(math.radians(theta)), math.sin(math.radians(theta))]
	other_vector = [to_point[0]-from_point[0], to_point[1]-from_point[1]]

	angle = _angle(unit_vector, other_vector)
	distance = _euclidean_distance(from_point, to_point)
	
	if angle <= (10**(-3)):
		actions.append(["moveFoward", distance])
		return actions

	quadrant = get_quadrant(from_point, to_point)
	print("quadrant: ", quadrant)

	if quadrant == 1:
		actions.append(["turnCW", angle])
		actions.append(["moveFoward", distance])
		return actions

	elif quadrant == 2:
		actions.append(["turnCCW", angle])
		actions.append(["moveFoward", distance])
		return actions

	elif quadrant == 3:
		actions.append(["turnCCW", angle])
		actions.append(["moveFoward", distance])
		return actions

	elif quadrant == 4:
		actions.append(["turnCW", angle])
		actions.append(["moveFoward", distance])
		return actions

	return actions

def runner():

	from_point = (1,1)
	to_point = (2,1)
	theta = 0

	quadrant = get_quadrant(from_point, to_point)
	print(quadrant)

	plan(from_point, to_point, theta)

# runner()




