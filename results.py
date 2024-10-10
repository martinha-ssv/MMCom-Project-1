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
from solver import buildGlobalK

def write_report(fname='report.txt'):
    '''Writes a report with the results of the analysis.'''
    with open(fname, 'w') as f:
        f.write('Results of the analysis\n\n')
        f.write('Displacements\n')
        for node in Node.nodes.values():
            f.write(f'Node {node.id}: {node.u1u2} magnitude: {np.linalg.norm(node.u1u2)}\n')
        f.write('\n\n')
        f.write('Strains\n')
        for element in Element.elements.values():
            f.write(f'Element {element.id}: {element.getStrain()} magnitude: {np.linalg.norm(element.getStrain())}\n')
        f.write('\n\n')
        f.write('Stresses\n')
        for element in Element.elements.values():
            f.write(f'Element {element.id}: {element.getStress()} magnitude: {np.linalg.norm(element.getStress())}\n')
        f.write('\n\n')
        f.write('Forces\n')
        for node in Node.nodes.values():
            f.write(f'Node {node.id}: {node.loads} magnitude: {np.linalg.norm(node.loads)}\n')
        f.write('\n\n')
        f.write('Reactions\n')
        for node in Node.nodes.values():
            for i, BC in enumerate(node.BCs):
                if not np.isnan(BC):
                    f.write(f'Node {node.id} axis {i}: {BC}\n')
        f.write('\n\n')
        f.write('Global stiffness matrix\n')
        f.write(f'{buildGlobalK()}')
        f.write('\n\n')
        f.write('End of report')
    print(f'Report written to {fname}')