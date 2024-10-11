from src.objects.node import Node
from src.objects.element import Element
import matplotlib.pyplot as plt
import numpy as np
import src.modules.fem_geometry as f_geom
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk



def draw_el(element, ax, colormap=True, attr='u', number=True): # TODO test
        '''Draws the element on the given axis.'''
        # Draw the element number
        centroid = np.mean([node.coordinates for node in element.nodes.values()], axis=0)
        if number: ax.text(centroid[0], centroid[1], str(element.id), color='blue', fontsize=8, ha='center')
        
        if colormap:
            us, points = element.interpolate_u()
            if attr=='ux':
                us = np.array([u[0] for u in us])
                vmin = Node.u1min
                vmax = Node.u1max
            elif attr=='uy':
                us = np.array([u[1] for u in us])
                vmin = Node.u2min
                vmax = Node.u2max
            elif attr=='strain':
                us = np.array([element.strain for u in us])
                vmin = Element.strainmin
                vmax = Element.strainmax
            elif attr=='stress':
                us = np.array([element.stress for u in us])
                vmin = Element.stressmin
                vmax = Element.stressmax
            else:
                us = np.array([np.linalg.norm(u) for u in us])
                vmin = 0
                vmax = Node.umax
            scatter = ax.scatter(points[:,0], points[:, 1], c=us, cmap='rainbow', vmin=vmin, vmax=vmax, s=5, zorder=3) 
        



def draw_structure(ax=None, plot=True, drawForces=True, drawConstraints=True, colors=False, plot_params=''): #TODO: TEST
        

    if ax is None:
        return
    
    # Draw the element as a line
    for element in Element.elements.values():
        
        ax.plot([element.nodes[1].coordinates[0], element.nodes[2].coordinates[0]], 
                [element.nodes[1].coordinates[1], element.nodes[2].coordinates[1]], 'k-')

        if colors:
            for element in Element.elements.values():
                draw_el(element, ax, colormap=True, attr=plot_params)
    # Draw the node as a point

        
    
         

    for node in Node.nodes.values():
        ax.plot(node.coordinates[0], node.coordinates[1], 'bo')  # blue dot for the node

        if drawForces:
            # Draw force vectors
            if node.loads[0] != 0:
                ax.arrow(node.coordinates[0], node.coordinates[1], 30*(-1 if node.loads[0]<0 else 1), 0, head_width=5, head_length=5, fc='r', ec='r')
            if node.loads[1] != 0:
                ax.arrow(node.coordinates[0], node.coordinates[1], 0, 30*(-1 if node.loads[1]<0 else 1), head_width=5, head_length=5, fc='r', ec='r')


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


class Draw():
    def __init__(self, fig, ax, canvas, master):
        Element.getMaxMinValues() #TODO; strainmax, stressmax
        Node.getMaxMinValues() #TODO: u1max, u2max, umax, force_max
        self.fig = fig
        self.ax = ax
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()
        self.toolbar = NavigationToolbar2Tk(self.canvas, master)
        self.toolbar.update