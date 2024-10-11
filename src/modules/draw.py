from objects.node import Node
from objects.element import Element
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib as mpl




def draw_el(element, 
            artist,
            color='u', 
            number=True): # TODO test
        
        '''Draws the element.'''

        ax = artist.ax
        unit = artist.points_to_du(4)[0]

        # Draw the element number
        centroid = np.mean([node.coordinates for node in element.nodes.values()], axis=0)
        if number:
            circle = plt.Circle((centroid[0], centroid[1]), radius=0.01, color='white', fill=True, alpha=0.8, lw=3, zorder=9) #TODO zorder (was 9)
            ax.add_patch(circle)
            ax.text(centroid[0], centroid[1], str(element.id), color='blue', fontsize=8, ha='center', va='center', zorder=10) #TODO ZORDER (was 10)
        
        us, points = element.interpolate_u()
        if color=='u_1':
            us = np.array([u[0] for u in us])
            vmin, vmax = Node.getMinMaxValues('u_1')
        elif color=='u_2':
            us = np.array([u[1] for u in us])
            vmin, vmax = Node.getMinMaxValues('u_2')
        elif color=='strain':
            us = np.array([element.strain for u in us])
            vmin, vmax = Element.getMinMaxValues('strain')
        elif color=='stress':
            us = np.array([element.stress for u in us])
            vmin, vmax = Element.getMinMaxValues('stress')
        elif color=='u':
            us = np.array([np.linalg.norm(u) for u in us])
            vmin, vmax = Node.getMinMaxValues('u')
        
        if color!='black':
            ax.scatter(points[:,0], points[:, 1], c=us, cmap='gist_rainbow', vmin=vmin, vmax=vmax, s=unit, zorder=3) 
        
        if color=='black':
            ax.plot([element.nodes[1].coordinates[0], element.nodes[2].coordinates[0]], 
                [element.nodes[1].coordinates[1], element.nodes[2].coordinates[1]], 'k-', lw=2)


def draw_colorbar(artist, 
                  vmin, 
                  vmax,
                  name):
        
        '''Draws the colorbar.'''
        fig = artist.fig
        ax = artist.ax
 
        norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
        sm = mpl.cm.ScalarMappable(cmap='gist_rainbow', norm=norm)
        sm.set_array([])  # You need to set an empty array for the ScalarMappable

        # Create the colorbar
        colorbar = fig.colorbar(sm, ax=ax)

        colorbar.set_label(name)

def draw_constraints(node, artist):
    fig, ax = artist.fig, artist.ax
    tri_height = artist.points_to_du(10)[0]
      # Draw constraints
    if node.hasBC(1):  # constraint in x direction
        triangle = plt.Polygon([
            [node.coordinates[0], node.coordinates[1]], 
            [node.coordinates[0] + tri_height, node.coordinates[1] + tri_height/2], 
            [node.coordinates[0] + tri_height, node.coordinates[1] - tri_height/2]
        ], closed=True, color='g')
        ax.add_patch(triangle)

    if node.hasBC(2):  # constraint in y direction
        triangle = plt.Polygon([
            [node.coordinates[0], node.coordinates[1]], 
            [node.coordinates[0] + tri_height/2, node.coordinates[1] - tri_height], 
            [node.coordinates[0] - tri_height/2, node.coordinates[1] - tri_height]
        ], closed=True, color='g')
        ax.add_patch(triangle)

def draw_forces(node, 
                artist, 
                scale=5e-3):
    
    '''Draws forces in red, support reactions in green and given external loads in blueviolet.'''
    try:
        scale = float(scale)
    except ValueError:
        scale = 5e-3

    ax = artist.ax
    scale = scale
    color = 'r'
    unit = artist.points_to_du(5)[0]

    if node.loads[0] != 0:
        if node.hasBC(1): color = 'limegreen'
        ax.arrow(node.coordinates[0], node.coordinates[1], node.loads[0]*unit*scale, 0, head_width=unit, head_length=unit, fc=color, ec=color, zorder=10)
    if node.loads[1] != 0:
        if node.hasBC(2): color = 'limegreen'
        ax.arrow(node.coordinates[0], node.coordinates[1], 0, node.loads[1]*unit*scale, head_width=unit, head_length=unit, fc=color, ec=color, zorder=10)


def draw_node(node, 
              artist, 
              forces, 
              constraints, 
              forces_scale):
    
    '''Draws the node.'''
    ax = artist.ax
    ax.plot(node.coordinates[0], node.coordinates[1], 'bo', zorder=8, markersize=3)  # blue dot for the node
    if forces:
        draw_forces(node, artist=artist, scale=forces_scale)
    if constraints:
        draw_constraints(node, artist)
     
def draw_structure(artist, 
                   forces=True, 
                   forces_scale=1, 
                   constraints=True, 
                   colors=False, 
                   element_numbers=False, 
                   nodes=True, 
                   elements=True,
                   deformed=None): #TODO: TEST
        
    ax = artist.ax
    
    if elements:
        for element in Element.elements.values():
            draw_el(element, artist, color=colors, number=element_numbers)
    if colors!="black":
            vmin, vmax = Element.getMinMaxValues(colors)
            if vmin==vmax:
                vmin, vmax = Node.getMinMaxValues(colors)
            if deformed == None:
                name = colors
            elif deformed:
                name = 'Deformed ' + colors
            else:
                name = 'Undeformed ' + colors
            draw_colorbar(artist, vmin, vmax, name)
    if nodes:
        for node in Node.nodes.values():
            draw_node(node, artist=artist, forces=forces, constraints=constraints, forces_scale=forces_scale)

    artist.ax.set_aspect('equal')
    return artist.ax


class Artist():
    normal_size = Element.avg_el_len()

    def __init__(self, fig, master):
        Element.setMaxMinValues() 
        Node.setMaxMinValues() 
        self.fig = fig
        self.config_grid(new=True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().pack(side="right", fill="both", expand=True, padx=10, pady=10)
        #self.canvas.draw()
        self.toolbar = NavigationToolbar2Tk(self.canvas, master, pack_toolbar=False)
        self.toolbar.update
        

    def reset_figure(self):
        # Create a new figure and axis
        self.fig.clf()
        self.config_grid(new=True)

    def config_grid(self, new=False):

        if new:
            self.ax = self.fig.add_subplot(111)

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


    def update_plot(self, 
                    draw_forces, 
                    forces_scale,   
                    draw_constraints,                   
                    deformed_colors,
                    undeformed_colors,
                    draw_nodes, 
                    draw_elements, 
                    element_numbers,
                    deformation_scale, 
                    draw_undeformed, 
                    draw_deformed):
        try:
            scale = float(deformation_scale)
        except ValueError:
            scale = 1e6

        #### CLEAR EVERYTHING
        self.reset_figure()
        
        # Remove existing colorbars
        for cbar in self.fig.axes[1:]:
            self.fig.delaxes(cbar)



            
        if draw_undeformed:
            self.ax = draw_structure(artist=self, 
                           forces=draw_forces, 
                           forces_scale=forces_scale, 
                           constraints=draw_constraints, 
                           colors=undeformed_colors, 
                           element_numbers=element_numbers, 
                           nodes=draw_nodes, 
                           elements=draw_elements,
                           deformed=False)
            self.canvas.draw()

        if draw_deformed:
            Node.ToggleDeformation(scale=scale)
            self.ax = draw_structure(artist=self, 
                           forces=draw_forces, 
                           forces_scale=forces_scale, 
                           constraints=draw_constraints, 
                           colors=deformed_colors, 
                           element_numbers=element_numbers, 
                           nodes=draw_nodes, 
                           elements=draw_elements,
                           deformed=True)
            self.canvas.draw()
            Node.ToggleDeformation()

     # Function to convert size in points to data units
    def points_to_du(self, size_in_points):
        # Get the figure DPI (dots per inch)
        dpi = self.fig.get_dpi()
        
        # Convert points to inches (1 point = 1/72 inch)
        size_in_inches = size_in_points / 72
        
        # Get the axis limits and axis size in inches
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        
        axis_width_in_data_units = xlim[1] - xlim[0]
        axis_height_in_data_units = ylim[1] - ylim[0]

        # Get figure size in inches (width and height in inches)
        fig_width_in_inches, fig_height_in_inches = self.fig.get_size_inches()

        # Calculate how much data units correspond to one inch (for both x and y axes)
        x_data_per_inch = axis_width_in_data_units / fig_width_in_inches
        y_data_per_inch = axis_height_in_data_units / fig_height_in_inches

        # Convert size from inches to data units
        width_in_data_units = size_in_inches * x_data_per_inch
        height_in_data_units = size_in_inches * y_data_per_inch

        return width_in_data_units, height_in_data_units

    def getLastZ(self):
        highest_zorder = max([drawing.zorder for drawing in plt.gca().get_children()])
        return highest_zorder