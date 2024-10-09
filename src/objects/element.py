import numpy as np
from ..modules import fem_geometry as f_geom
from ..objects.node import Node
from math import cos as c, sin as s

class Element():
    elements = {}
    A_section = 0
    E_young = 0
    v_poisson = 0

    def __init__(self, id, node_start, node_end):
        self.node_start = node_start
        self.node_end = node_end
        self.id = int(id)
        self.theta = f_geom.get_angle_from_horizontal(self.node_end.coordinates - self.node_start.coordinates)
        Element.elements[self.id] = self

    
    def h_e(self):
        return f_geom.get_distance(self.node_start, self.node_end)
    
    def __repr__(self):
        return f'E{self.id:<5} N{self.node_start.id:<5} N{self.node_end.id:<5} h_e = {self.h_e():.3f}'
    
    def Ke(self):
        '''Calculates the element stiffness matrix in global coordinates.'''
        oo = self.theta
        pre_block_diagonal = np.array([[c(oo)**2, c(oo)*s(oo)]\
                                      ,[c(oo)*s(oo), s(oo)**2]])
        pre_block = np.block([[pre_block_diagonal, -pre_block_diagonal]\
                             ,[-pre_block_diagonal, pre_block_diagonal]])
        return (Element.E_young * Element.A_section / self.h_e()) * pre_block
        
    