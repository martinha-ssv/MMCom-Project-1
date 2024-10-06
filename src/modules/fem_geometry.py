import math
import numpy as np

def get_distance(start, end):
    return np.linalg.norm(np.array(start.coordinates) - np.array(end.coordinates)) 