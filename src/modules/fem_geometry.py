import math
import numpy as np


def get_distance(start, end):
    return np.linalg.norm(np.array(start.coordinates) - np.array(end.coordinates)) 

def get_angle(u, v):
    '''Get the directed angle from vector u to v'''
    angle_u = get_angle_from_horizontal(u)
    angle_v = get_angle_from_horizontal(v)
    return angle_v - angle_u

def get_angle_from_horizontal(v):
    return np.arctan2(v[1], v[0])


