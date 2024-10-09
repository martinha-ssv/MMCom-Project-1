import numpy as np
from ..modules import fem_geometry as f_geom
from ..objects.node import Node
from math import cos as c, sin as s
from ..modules import parser as p

class Element():
    elements = {}
    globalK = np.zeros(0) # Initialize global stiffness matrix
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
    
    def h_e(self):
        return f_geom.get_distance(self.nodes[1], self.nodes[2])
    
    def __repr__(self):
        return f'E{self.id:<5} N{self.nodes[1].id:<5} --> N{self.nodes[2].id:<5} h_e = {self.h_e():.3f}'
    
    def Ke(self):
        '''Calculates the element stiffness matrix in global coordinates.'''
        oo = self.theta
        pre_block_diagonal = np.array([[c(oo)**2, c(oo)*s(oo)]\
                                      ,[c(oo)*s(oo), s(oo)**2]])
        pre_block = np.block([[pre_block_diagonal, -pre_block_diagonal]\
                             ,[-pre_block_diagonal, pre_block_diagonal]])
        return (Element.E_young * Element.A_section / self.h_e()) * pre_block
    
    def constrain_Ke(self):
        '''Constrains the element stiffness matrix.'''
        BC_vec = np.array([node.BCs for node in Node.nodes.values()]).flatten()
        loads_vec = np.array([node.loads for node in Node.nodes.values()]).flatten()
        print('BOUNDARY CONDITIONS:', BC_vec)
        for i, BC in enumerate(BC_vec):
            if BC != None:
                self.Ke[i] = 0
                self.Ke[:, i] = 0
                self.Ke[i, i] = 1
                #self.forces[i] = BC #TODO: these forces -> when there are constraints, the force vector is not the same as the loads
            else:
                print('still can´t constrain force vector')
                #self.forces[i] = self.loads[i]
        return self.Ke#, self.forces
    
    def build_Ke(self):
        '''Builds the element stiffness matrix.'''
        self.Ke = self.Ke()
        return self.Ke
    

        
    