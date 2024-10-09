import numpy as np
class Node():
    nodes = {}
    Nsets = {}

    def __init__(self, id, coordinates):
        self.id = int(id)
        self.coordinates = np.array(coordinates, dtype=float)
        Node.nodes[self.id] = self

    
    def getNodeById(id):
        id = int(id)
        if id in Node.nodes.keys():
            return Node.nodes[id]
        else:  
            return None
        
    def __repr__(self):
        coords = ', '.join([str(coord) for coord in self.coordinates])
        return f'N{self.id}, ({coords})'