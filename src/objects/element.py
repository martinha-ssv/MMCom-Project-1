import sys
import os
from node import *
import numpy as np
# TODO: fix import below ######################################
import fem_geometry as f_geom

class Element():
    def __init__(self, node_start, node_end, id):
        self.node_start = node_start
        self.node_end = node_end
        self.id = id
    
    def length(self):
        return f_geom.get_distance(self.node_start, self.node_end)
    
    