import numpy as np
import random
import math
import scipy.stats
from agent import Agent


SIZE_FACTOR_OF_WAYPOINT = 1
BELIEF_FOR_ACTION_SUCCESSFUL = 0.8
BELIEF_FOR_ADJACENT_ACTION = 0.4
BELIEF_FOR_OTHER_ACTION = 0.2

class WayPoint:
      def __init__(self,W,means,variances):
          self.W = W
          self.means = means
          self.variances = variances

class A_BLE:

    def __init__(self, N, measured_power, coord):
        self.ID = hex(random.randrange(0, 2 ^ 16))
        self.N = N
        self.measured_power = measured_power
        self.noise_std_dev = random.uniform(0, 4)
        self.coord = coord
        self.waypoints = []

    def _euclidean_distance(self, point1, point2):
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)*SIZE_FACTOR_OF_WAYPOINT

    def distance_to_rssi(self, distance):
        rssi = self.measured_power
        if distance > 0:
            rssi = self.measured_power - (math.log(distance, 10) * 10 * self.N)
        else:
            rssi = rssi/5
        return rssi

    def coord_to_rssi(self, coord):
        distance = self._euclidean_distance(self.coord, coord)
        rssi = self.distance_to_rssi(distance)
        rssi -= np.random.normal(0, self.noise_std_dev)
        return rssi

    def coord_to_rssi_without_noise(self, coord):
        distance = self._euclidean_distance(self.coord, coord)
        rssi = self.distance_to_rssi(distance)
        return rssi



def fill_beliefs_equally(waypoints):
     beliefs = {}
     value = 1
     for waypoint in waypoints:
         beliefs[waypoint.W] = value
     return beliefs




def fill_the_way_points(bles):
    waypoints = []
    variance = 4
    for i in range(0,11):
       for j in range(0,11):
          means={}
          variances = {}
          for ble in bles:
             means[ble.ID]= ble.coord_to_rssi_without_noise((i,j))
             variances[ble.ID] = variance
          waypoint = WayPoint(str(i) + "_" + str(j),means,variances)
          waypoints.append(waypoint)
    return waypoints

def is_valid_waypoint(coor):
    if coor[0]>=0 and coor[0]<=10 and coor[1]>=0 and coor[1]<=10:
        return True
    else :
        return False



