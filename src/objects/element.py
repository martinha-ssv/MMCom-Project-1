import numpy as np
from math import cos as c, sin as s
from .node import Node
from ..modules import fem_geometry as f_geom
import matplotlib.pyplot as plt

class Element():
    elements = {}
    A_section = 0
    E_young = 0
    v_poisson = 0

    def getElementById(id):
        id = int(id)
        if id in Element.elements.keys():
            return Element.elements[id]
        else:  
            return None
    
    def getAllKes():
        for element in Element.elements.values():
            element.build_Ke()

    def __init__(self, id, node_start, node_end):
        self.nodes = {}
        self.nodes[1] = node_start
        self.nodes[2] = node_end
        self.id = int(id)
        self.theta = f_geom.get_angle_from_horizontal(self.nodes[2].coordinates - self.nodes[1].coordinates)
        Element.elements[self.id] = self
        self.Ke = np.zeros((4, 4))

    
    def __repr__(self):
        return f'E{self.id:<5} N{self.nodes[1].id:<5} --> N{self.nodes[2].id:<5} h_e = {self.h_e():.3f}'
    
    def build_Ke(self):
        '''Calculates the element stiffness matrix in global coordinates.'''
        oo = self.theta
        pre_block_diagonal = np.array([[c(oo)**2, c(oo)*s(oo)]\
                                      ,[c(oo)*s(oo), s(oo)**2]])
        pre_block = np.block([[pre_block_diagonal, -pre_block_diagonal]\
                             ,[-pre_block_diagonal, pre_block_diagonal]])
        self.Ke = (Element.E_young * Element.A_section / self.h_e()) * pre_block

        return self.Ke
    
    def h_e(self):
        '''Returns the length of the element.'''
        return f_geom.get_distance(self.nodes[1], self.nodes[2])
    
    def interpolation_weights(self, x):
        '''Interpolates the displacement vector for a given x.'''
        N1 = 1 - x/self.h_e()
        N2 = x/self.h_e()
        return np.array([N1, N2])

    def interpolate_u(self, no_intervals=100):
        '''Interpolates the displacement vector for a given x.'''
        coordinates_start = self.nodes[1].coordinates
        coordinates_end = self.nodes[2].coordinates
        points = np.linspace(coordinates_start, coordinates_end, no_intervals)
        uu = np.array([self.nodes[1].u1u2, self.nodes[2].u1u2]) #TODO: ver se o 0 fica exatamente u1
        us = np.array([uu.T @ self.interpolation_weights(i) for i in range(len(points))])
        xs = np.array(points[:, 0])
        ys = np.array(points[:, 1])
        return us, points
    
    #TODO implement projectInElementDirection
    #TODO implement getStrain
    #TODO implement getStress
    def projectInElementDirection(self, u):
        '''Projects a vector in the element direction.'''
        element_vector = self.nodes[2].coordinates - self.nodes[1].coordinates
        element_direction = element_vector / np.linalg.norm(element_vector)
        return u @ element_direction
    
    def projectInXYDirection(self, magnitude):
        '''Projects a vector that is in the element's direction to the XY direction, given its magnitude.'''
        element_vector = self.nodes[2].coordinates - self.nodes[1].coordinates
        element_direction = element_vector / np.linalg.norm(element_vector)


    def getStrain(self):
        '''Calculates the strain in the element.'''
        du = self.projectInElementDirection(self.nodes[2].u1u2-self.nodes[1].u1u2)
        self.strain = du / self.h_e()
        return self.strain
    
    def getStress(self):
        '''Calculates the stress in the element.'''
        self.stress = Element.E_young * self.getStrain()
        return self.stress