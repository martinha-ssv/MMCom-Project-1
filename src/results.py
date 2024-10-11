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
from objects.node import Node
from objects.element import Element
from tabulate import tabulate

class Results():
    '''Class to handle the results of the analysis.'''
    results_string = ''

    @staticmethod
    def write_report_txt(fname='report1.txt'):
        '''Writes a report with the results of the analysis.'''

        with open(fname, 'w') as f:
            results_str = Results.build_results_string()
            f.write(results_str)
        print(f'Report written to {fname}')


    def build_results_string(k, units=None):
        '''Builds the results string for the report.'''
        results = []
        results.append('FEA Analysis Results\n\n')

        # Nodes
        results.append('Nodes\n')
        nodes_table = [[node.id, node.coordinates[0], node.coordinates[1]] for node in Node.nodes.values()]
        results.append(tabulate(nodes_table, headers=['Node', 'X', 'Y'], tablefmt='rounded_outline'))
        results.append('\n\n')

        # Elements
        results.append('Elements\n')
        elements_table = [[element.id, element.nodes[1].id, element.nodes[2].id] for element in Element.elements.values()]
        results.append(tabulate(elements_table, headers=['Element', 'Node 1', 'Node 2'], tablefmt='rounded_outline'))
        results.append('\n\n')

        # Constraints
        results.append('Constraints\n')
        constraints_table = []
        for node in Node.nodes.values():
            for i, BC in enumerate(node.BCs):
                if not np.isnan(BC):
                    constraints_table.append([node.id, i+1, BC])
        results.append(tabulate(constraints_table, headers=['Node', 'Axis', 'Constraint'], tablefmt='rounded_outline'))
        results.append('\n\n')

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
                    reactions_table.append([node.id, i+1, node.loads[i]])
        results.append(tabulate(reactions_table, headers=['Node', 'Axis', 'Reaction'], tablefmt='rounded_outline'))
        results.append('\n\n')
        
        # Global stiffness matrix
        results.append('Global stiffness matrix\n')
        formatted_k = [[f"{value:.3e}" for value in row] for row in k]
        results.append(tabulate(formatted_k, tablefmt='rounded_grid'))
        results.append('\n\n')
        
        results.append('End of report')

        Results.results_string = ''.join(results)

        return Results.results_string



