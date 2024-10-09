import math
import numpy as np


def get_distance(start, end):
    return np.linalg.norm(np.array(start.coordinates) - np.array(end.coordinates)) 

def get_angle(u, v):
    return math.acos(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)))

def get_angle_from_horizontal(v):
    return get_angle(v, np.array([1, 0]))


