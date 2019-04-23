import numpy as np
import random
import math

class BLE:

	def __init__(self, N, measured_power, coord):
		self.ID = hex(random.randrange(0,2^16))
		self.N = N
		self.measured_power = measured_power
		self.noise_std_dev = random.uniform(0,1)
		self.coord = coord

	def _euclidean_distance(self, point1, point2):
	    return math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)

	def rssi_to_distance(self, rssi):
		exp = (self.measured_power - rssi) / (10 * self.N)
		distance = 10 ** exp
		return distance

	def distance_to_rssi(self, distance):
		rssi = self.measured_power - (math.log(distance,10) * 10*self.N)
		return rssi

	def coord_to_rssi(self, coord):
		distance = self._euclidean_distance(self.coord, coord)
		rssi = self.distance_to_rssi(distance)
		rssi += np.random.normal(0, self.noise_std_dev)
		return rssi

def runner():

	ble1 = BLE(4, -73, (0,0))
	ble2 = BLE(4, -73, (0,100))
	ble3 = BLE(4, -73, (100,100))

	test_point = (40, 50)

	rssi1 = ble1.coord_to_rssi(test_point)
	dist1 = ble1.rssi_to_distance(rssi1)

	rssi2 = ble2.coord_to_rssi(test_point)
	dist2 = ble2.rssi_to_distance(rssi2)

	rssi3 = ble3.coord_to_rssi(test_point)
	dist3 = ble3.rssi_to_distance(rssi3)

	point = localise(ble1, dist1, ble2, dist2, ble3, dist3)
	print(point)

	for i in range(0,100):
		print(ble1.coord_to_rssi(test_point))


# runner()


