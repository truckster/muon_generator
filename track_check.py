import numpy as np
import math as math


def is_detector_hit(data_array):
    detector_radius = 19.6
    return_array = []
    for index, event in enumerate(data_array):
        muon_origin = np.array([event.x_pos_init, event.y_pos_init, event.z_pos_init])/1000
        muon_direction = np.array([event.x_momentum_init, event.y_momentum_init, event.z_momentum_init])
        abs_direction = math.sqrt(event.x_momentum_init**2 + event.y_momentum_init**2 + event.z_momentum_init**2)

        intersec_coeff = (math.pow(np.dot(muon_direction/abs_direction, muon_origin), 2)
                          - np.dot(muon_origin, muon_origin)
                          + math.pow(detector_radius, 2))

        if intersec_coeff > 0:
            return_array.append(event)

    return return_array
