from ble import BLE
import numpy as np

def filter(estimate, measurement, error_estimate, error_measurement):
	kalman_gain = error_estimate / (error_estimate + error_measurement)
	estimate = estimate + kalman_gain*(measurement-estimate)
	error_estimate = (1-kalman_gain)*error_estimate
	return estimate, error_estimate

def triangulate(ble1, dist1, ble2, dist2, ble3, dist3):

	x_coeff_eq_1 = 2*(ble2.coord[0]-ble1.coord[0])
	y_coeff_eq_1 = 2*(ble2.coord[1]-ble1.coord[1])
	x_coeff_eq_2 = 2*(ble3.coord[0]-ble1.coord[0])
	y_coeff_eq_2 = 2*(ble3.coord[1]-ble1.coord[1])

	const_eq_1 = dist1**2 - dist2**2 - ble1.coord[0]**2 + ble2.coord[0]**2 - ble1.coord[1]**2 + ble2.coord[1]**2
	const_eq_2 = dist1**2 - dist3**2 - ble1.coord[0]**2 + ble3.coord[0]**2 - ble1.coord[1]**2 + ble3.coord[1]**2

	coeff = np.array([[x_coeff_eq_1, y_coeff_eq_1], [x_coeff_eq_2, y_coeff_eq_2]])
	const = np.array([const_eq_1, const_eq_2])

	solution = tuple(np.linalg.solve(coeff, const))

	return solution

def localise(ble1, rssi1, ble2, rssi2, ble3, rssi3, estimates, error_estimates, error_measurements, num_iter):

	estimate_ble1, estimate_ble2, estimate_ble3 = estimates[0], estimates[1], estimates[2]
	error_estimate_ble1, error_estimate_ble2, error_estimate_ble3 = error_estimates[0], error_estimates[1], error_estimates[2]
	error_measurement_ble1, error_measurement_ble2, error_measurement_ble3 = error_measurements[0], error_measurements[1], error_measurements[2]

	for i in range(0,num_iter):

		estimate_ble1, error_estimate_ble1 = filter(estimate_ble1, rssi1, error_estimate_ble1, error_measurement_ble1) 
		estimate_ble2, error_estimate_ble2 = filter(estimate_ble2, rssi2, error_estimate_ble2, error_measurement_ble2)
		estimate_ble3, error_estimate_ble3 = filter(estimate_ble3, rssi3, error_estimate_ble3, error_measurement_ble3)

	dist1 = ble1.rssi_to_distance(estimate_ble1)
	dist2 = ble2.rssi_to_distance(estimate_ble2)
	dist3 = ble3.rssi_to_distance(estimate_ble3)

	point = localise(ble1, dist1, ble2, dist2, ble3, dist3)

	return point


def runner():

	ble1 = BLE(4, -73, (0,0))
	ble2 = BLE(4, -73, (0,100))
	ble3 = BLE(4, -73, (100,100))

	test_point = (40, 50)

	estimate_ble1, estimate_ble2, estimate_ble3 = ble1.coord_to_rssi((38,50)), ble2.coord_to_rssi((40,50)), ble2.coord_to_rssi((39,52))
	error_estimate_ble1, error_estimate_ble2, error_estimate_ble3 = -1, -1, -2
	error_measurement_ble1, error_measurement_ble2, error_measurement_ble3 = 0.2, 0.2, 0.2

	for i in range(0,100):

		rssi1 = ble1.coord_to_rssi(test_point)
		estimate_ble1, error_estimate_ble1 = filter(estimate_ble1, rssi1, error_estimate_ble1, error_measurement_ble1) 

		rssi2 = ble2.coord_to_rssi(test_point)
		estimate_ble2, error_estimate_ble2 = filter(estimate_ble2, rssi2, error_estimate_ble2, error_measurement_ble2)
	
		rssi3 = ble3.coord_to_rssi(test_point)
		estimate_ble3, error_estimate_ble3 = filter(estimate_ble3, rssi3, error_estimate_ble3, error_measurement_ble3)

	dist1 = ble1.rssi_to_distance(estimate_ble1)
	dist2 = ble2.rssi_to_distance(estimate_ble2)
	dist3 = ble3.rssi_to_distance(estimate_ble3)

	point = localise(ble1, dist1, ble2, dist2, ble3, dist3)
	print(point)

# runner()