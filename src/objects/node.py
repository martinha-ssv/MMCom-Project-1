import numpy as np
import matplotlib.pyplot as plt
from src.modules import parser
import pygame
import math as m


class Node():
    nodes = {}
    Nsets = {}

    def __init__(self, id, coordinates):
        self.id = int(id)
        self.coordinates = np.array(coordinates, dtype=float)
        self.loads = np.zeros(2)
        self.BCs = np.array([None, None], dtype=float)
        Node.nodes[self.id] = self
        self.deformed_coordinates = self.coordinates
        self.u1u2 = np.zeros(2)
        self.isDeformed = False

    def ToggleDeformation(self, isDeformed):
        if not isDeformed:
            self.coordinates = self.coordinates + self.u1u2
        else:
            self.coordinates = self.coordinates - self.u1u2

    
    def getNodeById(id):
        id = int(id)
        if id in Node.nodes.keys():
            return Node.nodes[id]
        else:  
            return None
        
    def __repr__(self):
        coords = ', '.join([str(coord) for coord in self.coordinates])
        return (
            f'Node {{\n'
            f'  id: {self.id},\n'
            f'  coordinates: ({coords}),\n'
            f'  loads: {self.loads.tolist()},\n'
            f'  boundary_conditions: {list(self.BCs)}\n'
            f'}}'
        )
    

    
