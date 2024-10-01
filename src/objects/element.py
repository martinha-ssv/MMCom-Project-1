import sys
import os
# fix import
import fem_geometry as f_geom

class Element():
    def __init__(self, node_start, node_end, id):
        self.node_start = node_start
        self.node_end = node_end
        self.id = id
        
    def get_node_start(self):
        return self.node_start 
    
    def get_node_end(self):
        return self.node_end
    
    def get_id(self):
        return self.id
    
    def get_length(self):
        return f_geom.get_distance(self.get_node_start.get_x(), self.get_node_start.get_y(), self.get_node_end.get_x(), self.get_node_end.get_y())
    
    