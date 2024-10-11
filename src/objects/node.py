import numpy as np
import math as m


class Node():
    nodes = {}
    Nsets = {}

    def getMaxMinValues():
        u1_lst = [node.u1u2[0] for node in Node.nodes.values()]
        Node.u1max = max(u1_lst)
        Node.u1min = min(u1_lst)

        u2_lst = [node.u1u2[1] for node in Node.nodes.values()]
        Node.u2max = max(u2_lst)
        Node.u2min = min(u2_lst)

        u_lst = [np.linalg.norm(node.u1u2) for node in Node.nodes.values()]
        Node.umax = max(u_lst)


    def nodesToVec(property):
        return np.concatenate([getattr(Node.nodes[i], property) for i in Node.nodes.keys()])
    
    def vecToNodes(vec, property):
        for i, node_id in enumerate(Node.nodes.keys()):
            setattr(Node.nodes[node_id], property, vec[2*i:2*i+2])

    def ToggleDeformation(scale=1e6):
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

    def toggleNodeDeformation(self, scale):
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
    

    
