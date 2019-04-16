import heapq
from environment import Environment
from agent import Agent

class WaypointPlanner:

	def __init__(self, environment, agent):
		self.env = environment
		self.agent = agent

	def _state_to_key(self, state):
		return "("+str(state[0])+","+str(state[1])+")"

	def _manhattan_distance(self, state1, state2):
		return ( abs(state1[0]-state2[0]) + abs(state1[1]-state2[1]) )

	def _get_successor(self, current_state, action):

		if action == "moveLeft":
			if current_state[0] - 1 < self.env.grid_min_coord[0]:
				return (None, -1)

			for obstacle in self.env.obstacles:
				obstacle_max_coord = obstacle[1]
				if current_state[0] - 1 <= obstacle_max_coord[0]: and current_state[0] return (None, -1)

			return ((current_state[0]-1, current_state[1]), 1)

		elif action == "moveRight":
			if current_state[0] + 1 > self.env.grid_max_coord[0]:
				return (None, -1)

			for obstacle in self.env.obstacles:
				obstacle_min_coord = obstacle[0]
				if current_state[0] + 1 >= obstacle_min_coord[0]: return (None, -1)

			return ((current_state[0]+1, current_state[1]), 1)
		
		elif action == "moveForward":
			if current_state[1] + 1 > self.env.grid_max_coord[1]:
				return (None, -1)

			for obstacle in self.env.obstacles:
				obstacle_min_coord = obstacle[0]
				if current_state[1] + 1 >= obstacle_min_coord[1]: return (None, -1)

			return ((current_state[0], current_state[1]+1), 1)

		elif action == "moveBackward":
			if current_state[1] - 1 < self.env.grid_min_coord[1]:
				return (None, -1)

			for obstacle in self.env.obstacles:
				obstacle_max_coord = obstacle[1]
				if current_state[1] - 1 <= obstacle_max_coord[1]: return (None, -1)

			return ((current_state[0], current_state[1]-1), 1)


	def plan(self):
		
		init_state = self.env.agent_coord
		goal_state = self.env.goal_coord

		possible_actions = self.agent.possible_actions
		action_list = []

		priority_queue = [(0, init_state)]
		heapq.heapify(priority_queue)
	    
		parsed_states = {}
		parsed_states[self._state_to_key(init_state)] = 1

		trace = {}
		trace[self._state_to_key(init_state)] = None

		current_state = init_state

		while(len(priority_queue)>0):

			(cost, current_state) = heapq.heappop(priority_queue)
			cost = cost + self._manhattan_distance(current_state, goal_state)
	        
			if current_state[0]==goal_state[0] and current_state[1]==goal_state[1]:
				break

			for action in possible_actions:
				print(current_state, action)
				(nextstate, cost) = self._get_successor(current_state, action)
				print(nextstate, cost)
				if cost != -1 and self._state_to_key(nextstate) not in parsed_states:
					parsed_states[self._state_to_key(nextstate)] = 1
					heapq.heappush(priority_queue, (cost, nextstate))
					trace[self._state_to_key(nextstate)] = (current_state, action)

		if current_state[0]==goal_state[0] and current_state[1]==goal_state[1]:
			print("solved")
			while(trace[self._state_to_key(current_state)] != None):
				(parent_state, action) = trace[self._state_to_key(current_state)]
				action_list.append(action)
				current_state = parent_state
		else:
			print("unsolved")

		action_list.reverse()

		return action_list

def runner():

	env = Environment((0,0), (100,50), (1,1), (80,30))
	agent = Agent()

	env.add_obstacle((25,10),(75,20))
	env.add_obstacle((25,35), (75,45))

	wp = WaypointPlanner(env, agent)
	plan = wp.plan()

	print(plan)

runner()
