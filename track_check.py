import numpy as np
import math as math


def is_detector_hit(data_array):
    return_array = []
    for index, event in enumerate(data_array):

        if is_detector_hit_event(event, detector_radius=13600):
            return_array.append(event)

    return return_array


def is_detector_hit_event(event, detector_radius=13600):

    muon_origin = np.array([event.x_pos_init, event.y_pos_init, event.z_pos_init])
    muon_direction = np.array([event.x_momentum_init, event.y_momentum_init, event.z_momentum_init])
    abs_direction = math.sqrt(event.x_momentum_init ** 2 + event.y_momentum_init ** 2 + event.z_momentum_init ** 2)

    intersec_coeff = (np.dot(np.dot(muon_direction / abs_direction, muon_origin),
                             np.dot(muon_direction / abs_direction, muon_origin))
                      - np.dot(muon_origin, muon_origin)
                      + math.pow(detector_radius, 2))

    if intersec_coeff > 0:
        print(intersec_coeff)

    if intersec_coeff > 0 and event.z_pos_init > 20000 and event.z_momentum_init / abs_direction < -0.55:
        return True
    else:
        return False