from src.objects.node import Node
from src.objects.element import Element
import matplotlib.pyplot as plt
import numpy as np

def draw_structure(ax=None, plot=True, drawForces=True, drawConstraints=True): #TODO: TEST
        

    if ax is None:
        fig, ax = plt.subplots(figsize=(5,7))

    # Draw the element as a line

    for element in Element.elements.values():
        ax.plot([element.nodes[1].coordinates[0], element.nodes[2].coordinates[0]], 
                [element.nodes[1].coordinates[1], element.nodes[2].coordinates[1]], 'k-')

    # Draw the node as a point
    for node in Node.nodes.values():
        ax.plot(node.coordinates[0], node.coordinates[1], 'bo')  # blue dot for the node

        if drawForces:
            # Draw force vectors
            if node.loads[0] != 0:
                ax.arrow(node.coordinates[0], node.coordinates[1], 30*(-1 if node.loads[0]<0 else 1), 0, head_width=5, head_length=5, fc='r', ec='r')
            if node.loads[1] != 0:
                ax.arrow(node.coordinates[0], node.coordinates[1], 0, 30*(-1 if node.loads[0]<0 else 1), head_width=5, head_length=5, fc='r', ec='r')

        if drawConstraints:
            # Draw constraints
            if not np.isnan(node.BCs[0]):  # constraint in x direction
                triangle = plt.Polygon([
                    [node.coordinates[0], node.coordinates[1]], 
                    [node.coordinates[0] + 10, node.coordinates[1] + 5], 
                    [node.coordinates[0] + 10, node.coordinates[1] - 5]
                ], closed=True, color='g')
                ax.add_patch(triangle)

            if not np.isnan(node.BCs[1]):  # constraint in y direction
                triangle = plt.Polygon([
                    [node.coordinates[0], node.coordinates[1]], 
                    [node.coordinates[0] + 5, node.coordinates[1] - 10], 
                    [node.coordinates[0] - 5, node.coordinates[1] - 10]
                ], closed=True, color='g')
                ax.add_patch(triangle)
    
    
    ax.set_aspect('equal')
    if plot:    
        plt.show()