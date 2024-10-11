from objects.node import Node
from objects.element import Element
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib as mpl


def draw_el(element, ax, colormap=True, attr='u', number=True): # TODO test
        '''Draws the element.'''

        # Draw the element number
        centroid = np.mean([node.coordinates for node in element.nodes.values()], axis=0)
        if number:
            circle = plt.Circle((centroid[0], centroid[1]), radius=6, color='white', fill=True, alpha=0.8, lw=3) #TODO zorder (was 9)
            ax.add_patch(circle)
            ax.text(centroid[0], centroid[1], str(element.id), color='blue', fontsize=8, ha='center', va='center') #TODO ZORDER (was 10)
            


        if colormap:
            us, points = element.interpolate_u()
            if attr=='u_1':
                us = np.array([u[0] for u in us])
                vmin = Node.u1min
                vmax = Node.u1max
            elif attr=='u_2':
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
            elif attr=='u':
                us = np.array([np.linalg.norm(u) for u in us])
                vmin = 0
                vmax = Node.umax
            scatter = ax.scatter(points[:,0], points[:, 1], c=us, cmap='gist_rainbow', vmin=vmin, vmax=vmax, s=5, zorder=3) 

            return vmin, vmax
        else:
            ax.plot([element.nodes[1].coordinates[0], element.nodes[2].coordinates[0]], 
                    [element.nodes[1].coordinates[1], element.nodes[2].coordinates[1]], 'k-')
            return None, None


def draw_colorbar(artist, vmin, vmax):
        fig = artist.fig
        ax = artist.ax
 
        norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
        sm = mpl.cm.ScalarMappable(cmap='gist_rainbow', norm=norm)
        sm.set_array([])  # You need to set an empty array for the ScalarMappable

        # Create the colorbar
        colorbar = fig.colorbar(sm, ax=ax)

def draw_constraints(node, artist):
    fig, ax = artist.fig, artist.ax
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

def draw_forces(node, artist, scale=1):
    fig, ax = artist.fig, artist.ax
    scale = scale/100
    if node.loads[0] != 0:
        ax.arrow(node.coordinates[0], node.coordinates[1], node.loads[0]*scale, 0, head_width=5, head_length=5, fc='r', ec='r')
    if node.loads[1] != 0:
        ax.arrow(node.coordinates[0], node.coordinates[1], 0, node.loads[1]*scale, head_width=5, head_length=5, fc='r', ec='r')


def draw_node(node, artist, forces, constraints):
    fig, ax = artist.fig, artist.ax
    ax.plot(node.coordinates[0], node.coordinates[1], 'bo', zorder=8)  # blue dot for the node
    if forces:
        draw_forces(node, artist)
    if constraints:
        draw_constraints(node, artist)
     
def draw_structure(artist, plot=True, forces=True, forces_scale=1, constraints=True, colors=False, element_numbers=False, deformed=False, deformation_scale=1e6): #TODO: TEST
        
    ax = artist.ax
    
    if deformed: 
        Node.ToggleDeformation(scale=deformation_scale)
    for element in Element.elements.values():
        vmin, vmax = draw_el(element, ax, colormap=colors, attr=colors, number=element_numbers)
    if colors:
            draw_colorbar(artist, vmin, vmax)



    for node in Node.nodes.values():
        ax.plot(node.coordinates[0], node.coordinates[1], 'bo')  # blue dot for the node

        if forces:
            draw_forces(node, artist, forces_scale)
        if constraints: 
           draw_constraints(node, artist)

        
    
    
    ax.set_aspect('equal')
    if plot:    
        plt.show()

    if deformed:
        Node.ToggleDeformation(scale=1/deformation_scale)

class Artist():
    def __init__(self, fig, ax, master):
        Element.getMaxMinValues() 
        Node.getMaxMinValues() 
        self.fig = fig
        self.ax = ax
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().pack(side="right", fill="both", expand=True, padx=10, pady=10)
        self.canvas.draw()
        self.toolbar = NavigationToolbar2Tk(self.canvas, master, pack_toolbar=False)
        self.toolbar.update
        # Set the background grid
        self.ax.grid(True, which='both', color='lightgray', linestyle='-', linewidth=0.5)

        # Set the axes color
        self.ax.spines['bottom'].set_color('lightgray')
        self.ax.spines['top'].set_color('lightgray')
        self.ax.spines['right'].set_color('lightgray')
        self.ax.spines['left'].set_color('lightgray')

        # Set the ticks and numbers color
        self.ax.tick_params(axis='both', colors='darkgray')
        self.ax.yaxis.label.set_color('darkgray')
        self.ax.xaxis.label.set_color('darkgray')
        self.ax.title.set_color('darkgray')

       
    def center_view(self):
        all_x_coords = []
        all_y_coords = []

        for element in Element.elements.values():
            for node in element.nodes.values():
                all_x_coords.append(node.coordinates[0])
                all_y_coords.append(node.coordinates[1])

        for node in Node.nodes.values():
            all_x_coords.append(node.coordinates[0])
            all_y_coords.append(node.coordinates[1])

        if all_x_coords and all_y_coords:
            min_x, max_x = min(all_x_coords), max(all_x_coords)
            min_y, max_y = min(all_y_coords), max(all_y_coords)

            self.ax.set_xlim(min_x - 10, max_x + 10)
            self.ax.set_ylim(min_y - 10, max_y + 10)
            self.canvas.draw()
        self.ax.set_aspect('equal') # BUG this may cause it to be off center
        

    def getLastZ(self):
        highest_zorder = max([drawing.zorder for drawing in plt.gca().get_children()])
        return highest_zorder