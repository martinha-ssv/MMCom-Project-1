import numpy as np
import matplotlib.pyplot as plts
import src.modules.file_input as fi 
import math as m


class Node():
    nodes = {}
    Nsets = {}

    def nodesToVec(property):
        return np.concatenate([getattr(Node.nodes[i], property) for i in Node.nodes.keys()])
    
    def vecToNodes(vec, property):
        for i, node_id in enumerate(Node.nodes.keys()):
            setattr(Node.nodes[node_id], property, vec[2*i:2*i+2])

    def ToggleDeformation(scale=1):
        for node in Node.nodes.values():
            node.toggleNodeDeformation(scale)

    def __init__(self, id, coordinates):
        self.id = int(id)
        self.coordinates = np.array(coordinates, dtype=float)
        self.loads = np.zeros(2)
        self.BCs = np.full(2, np.nan)
        Node.nodes[self.id] = self

        self.deformed_coordinates = self.coordinates
        self.u1u2 = np.zeros(2)

        self.lastScale = 1

    def toggleNodeDeformation(self, scale=1):
        if self.lastScale == 1:
            self.coordinates = self.coordinates + scale*self.u1u2
            self.lastScale = scale
        else:
            self.coordinates = self.coordinates - self.lastScale*self.u1u2
            self.lastScale = 1

    
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
            f'  boundary_conditions: {self.BCs.tolist()}\n'
            f'}}'
        )
    

    
