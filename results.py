# TODO
# - Displacements
#   -> displacements for each node. State the node ID and the displacement vector, as well as its magnitude. 
# - Strains
#   -> strains for each element. State the element ID and the strain vector (vector?), as well as its magnitude.  
# - Stresses
#   -> stresses for each element. State the element ID and the stress vector (vector?), as well as its magnitude.
# - Forces
#   -> forces for each node. State the node ID and the force vector, as well as its magnitude.
# - Reactions 
#   -> if there was a boundary condition on this axis, the force is a reaction force. State it, identifying the node ID, the axis, and the value
# - Global stiffness matrix
import numpy as np
from src.objects.node import Node
from src.objects.element import Element
from tabulate import tabulate
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def build_results_string(k):
        '''Builds the results string for the report.'''
        results = []
        results.append('Results of the analysis\n\n')
        
        # Displacements
        results.append('Displacements\n')
        displacements_table = [[node.id, node.u1u2[0], node.u1u2[1], np.linalg.norm(node.u1u2)] for node in Node.nodes.values()]
        results.append(tabulate(displacements_table, headers=['Node', 'u_1', 'u_2', 'Magnitude'], tablefmt='rounded_outline'))
        results.append('\n\n')
        
        # Strains
        results.append('Strains\n')
        strains_table = [[element.id, element.getStrain()] for element in Element.elements.values()]
        results.append(tabulate(strains_table, headers=['Element', 'Strain'], tablefmt='rounded_outline'))
        results.append('\n\n')
        
        # Stresses
        results.append('Stresses\n')
        stresses_table = [[element.id, element.getStress()] for element in Element.elements.values()]
        results.append(tabulate(stresses_table, headers=['Element', 'Stress'], tablefmt='rounded_outline'))
        results.append('\n\n')
        
        # Forces
        results.append('Forces\n')
        forces_table = np.array([[node.id, node.loads[0], node.loads[1], np.linalg.norm(node.loads)] for node in Node.nodes.values()])
        results.append(tabulate(forces_table, headers=['Node', 'F_x', 'F_y', 'Magnitude'], tablefmt='rounded_outline'))
        results.append('\n\n')
        
        # Reactions
        results.append('Reactions\n')
        reactions_table = []
        for node in Node.nodes.values():
            for i, BC in enumerate(node.BCs):
                if not np.isnan(BC):
                    reactions_table.append([node.id, i, node.loads[i]])
        results.append(tabulate(reactions_table, headers=['Node', 'Axis', 'Reaction'], tablefmt='rounded_outline'))
        results.append('\n\n')
        
        # Global stiffness matrix
        results.append('Global stiffness matrix\n')
        results.append(tabulate(k, tablefmt='rounded_grid'))
        results.append('\n\n')
        
        results.append('End of report')

        return ''.join(results)



def write_report_txt(fname='report1.txt'):
    '''Writes a report with the results of the analysis.'''

    with open(fname, 'w') as f:
        results_str = build_results_string()
        f.write(results_str)
    print(f'Report written to {fname}')