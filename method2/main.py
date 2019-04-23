import localiser as localiser
import trajectory as trajectory
from waypoint_planner import WaypointPlanner

from agent import Agent
from ble import BLE
from environment import Environment
from simulator import Simulator

import matplotlib.pyplot as plt
import math
import numpy as np

def define_problem():

	env = Environment((0,0), (100,50), (1,1), (80,30), 100, 50)
	env.add_obstacle((25,10),(75,20))
	env.add_obstacle((25,35), (75,45))

	agent = Agent(0, 0, 5, 5)

	ble1 = BLE(4, -73, (0,0))
	ble2 = BLE(4, -73, (100,0))
	ble3 = BLE(4, -73, (50,50))

	sim = Simulator(env, agent, [ble1, ble2, ble3])

	return sim

def read_rssis(sim):
	return [sim.bles[0].coord_to_rssi(sim.env.agent_coord), sim.bles[1].coord_to_rssi(sim.env.agent_coord), sim.bles[2].coord_to_rssi(sim.env.agent_coord)]

def localise(sim, rssis, coord, num_sense_iter):

	estimate_ble1, estimate_ble2, estimate_ble3 = sim.bles[0].coord_to_rssi(coord), sim.bles[1].coord_to_rssi(coord), sim.bles[2].coord_to_rssi(coord)
	error_estimate_ble1, error_estimate_ble2, error_estimate_ble3 = 0.5, 0.5, 0.5
	error_measurement_ble1, error_measurement_ble2, error_measurement_ble3 = 10, 10, 10
	
	for j in range(num_sense_iter):
		estimate_ble1, error_estimate_ble1 = localiser.filter(estimate_ble1, rssis[0], error_estimate_ble1, error_measurement_ble1) 
		estimate_ble2, error_estimate_ble2 = localiser.filter(estimate_ble2, rssis[1], error_estimate_ble2, error_measurement_ble2)
		estimate_ble3, error_estimate_ble3 = localiser.filter(estimate_ble3, rssis[2], error_estimate_ble3, error_measurement_ble3)

	dist1 = sim.bles[0].rssi_to_distance(estimate_ble1)
	dist2 = sim.bles[1].rssi_to_distance(estimate_ble2)
	dist3 = sim.bles[2].rssi_to_distance(estimate_ble3)

	point = localiser.triangulate(sim.bles[0], dist1, sim.bles[1], dist2, sim.bles[2], dist3)

	return point

def visualise(sim, state_list):

	mat = np.zeros(( (sim.env.grid_max_coord[1])+1, (sim.env.grid_max_coord[0])+1 ))

	for obstacle in sim.env.obstacles:
		x_list = [x for x in range(obstacle[0][0],obstacle[1][0]+1)]
		y_list = [y for y in range(obstacle[0][1],obstacle[1][1]+1)]
		for x in x_list:
			for y in y_list:
				mat[y,x] = 1

	for state in state_list:
		mat[state[1],state[0]] = 0.5

	# mat[sim.env.agent_coord[1], sim.env.agent_coord[0]] = 2
	mat[sim.env.goal_coord[1], sim.env.goal_coord[0]] = 2

	plt.matshow(mat)
	plt.show()

def generate_parsed_coordinates(sim):
	to_parse_x, to_parse_y = sim.env.agent_coord[0], sim.env.agent_coord[1]
	if to_parse_x < 1: to_parse_x = 1
	if to_parse_y < 1: to_parse_y = 1
	to_parse_x = math.floor(to_parse_x)
	to_parse_y = math.floor(to_parse_y)
	return (to_parse_x, to_parse_y)

def main():

	sim = define_problem()

	wp = WaypointPlanner(sim.env)
	plan = wp.plan()

	num_sense_iter = 100
	parsed = []

	for i in range(len(plan)-1):

		parsed_coordinates = generate_parsed_coordinates(sim)
		parsed.append(parsed_coordinates)

		print("agent coordinate: ", sim.env.agent_coord)
		print("agent angle: ", sim.env.agent_theta)

		actions = trajectory.plan(sim.env.agent_coord, plan[i+1], sim.env.agent_theta)

		if len(actions) == 1:
			_, distance = actions[0][0], actions[0][1]
			time = sim.agent.distance_to_time(distance)
			sim.execute_move(time)
			continue

		turn_action, move_action = actions[0], actions[1]

		turn_time = sim.agent.angle_to_time(turn_action[1])
		move_time = sim.agent.distance_to_time(move_action[1])

		if turn_action[0] == "turnCW": sim.execute_turnCW(turn_time)
		elif turn_action[0] == "turnCCW": sim.execute_turnCCW(turn_time)
		sim.execute_move(move_time)

		rssis = read_rssis(sim)
		sim.env.agent_coord = localise(sim, rssis, plan[i+1], 100)

	visualise(sim, parsed)

main()