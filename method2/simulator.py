from environment import Environment
from agent import Agent
import math
import numpy as np

class Simulator:

	def __init__(self, env, agent, bles):
		self.env = env
		self.agent = agent
		self.bles = bles

	def execute_move(self, time_seconds):

		distance = self.agent.linear_velocity * time_seconds
		original_x, original_y = self.env.agent_coord[0], self.env.agent_coord[1]

		new_x = original_x + distance * math.cos(math.radians(self.env.agent_theta))
		new_y = original_y + distance * math.sin(math.radians(self.env.agent_theta))

		if original_y == new_y: new_x += np.random.normal(0, self.agent.linear_noise_std)
		elif original_x == new_x: new_y += np.random.normal(0, self.agent.linear_noise_std)

		self.env.agent_coord = (new_x, new_y)

	def execute_turnCW(self, time_seconds):
		
		angle = self.agent.angular_velocity * time_seconds
		angle = self.env.agent_theta - angle
		angle += np.random.normal(0, self.agent.angular_noise_std)

		if angle < 0: angle = 360-abs(angle)

		self.env.agent_theta = angle

	def execute_turnCCW(self, time_seconds):
		
		angle = self.agent.angular_velocity * time_seconds
		angle = self.env.agent_theta + angle
		angle += np.random.normal(0, self.agent.angular_noise_std)

		if angle > 360: angle = abs(360-angle) 

		self.env.agent_theta = angle

def runner():

	env = Environment((0,0), (100,50), (0,0), (80,30), 10, 5)
	agent = Agent(0, 0, 5, 5)

	sim = Simulator(env, agent, [])

	print(sim.env.agent_coord, sim.env.agent_theta)

	sim.execute_move(1)
	print(sim.env.agent_coord, sim.env.agent_theta)

	sim.execute_turnCCW(18)
	print(sim.env.agent_coord, sim.env.agent_theta)

runner()




