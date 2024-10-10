from src.modules import parser as p
from src.modules.file_input import InputFile
from src.objects.node import Node
from src.objects.element import Element
from src.modules import draw
from pprint import pprint
import numpy as np
from parser_tests import test_all
import copy
from tabulate import tabulate
import matplotlib.pyplot as plt
# from results import write_report

def buildGlobalK():
        '''Builds the global stiffness matrix by iterating over each element and, 
        by matching their nodes to the global nodes, summing their contributions.'''

        Element.getAllKes()

        K_global = np.zeros((2*len(Node.nodes), 2*len(Node.nodes)))
        for element in Element.elements.values():
            for localID_i, node_i in element.nodes.items():
                globalID_i = node_i.id
                for localID_j, node_j in element.nodes.items():
                    globalID_j= node_j.id

                    ke_block = element.Ke[2*p.RealToPy_ind(localID_i):2*p.RealToPy_ind(localID_i)+2, \
                                    2*p.RealToPy_ind(localID_j):2*p.RealToPy_ind(localID_j)+2]
                    
                    K_global[2*p.RealToPy_ind(globalID_i):2*p.RealToPy_ind(globalID_i)+2, \
                                    2*p.RealToPy_ind(globalID_j):2*p.RealToPy_ind(globalID_j)+2] += ke_block
                    
        return K_global

def constrainGlobalK(K):
    K_global_constrained = copy.copy(K) #FIXME
    #K_global_constrained = K
    force_vec = Node.nodesToVec('loads')

    for node in Node.nodes.values():
        for i, BC in enumerate(node.BCs):
            if not np.isnan(BC):
                ind = 2*p.RealToPy_ind(node.id)+i
                eliminateUnknown(K_global_constrained, ind)
                force_vec[ind] = BC
    return K_global_constrained, force_vec

def solve_disp(K_const, force_vec):
    disp_vec = np.linalg.solve(K_const, force_vec)
    Node.vecToNodes(disp_vec, 'u1u2')
    return disp_vec

def solveForces(K_global,disp_vec):
    force_vec = K_global @ disp_vec.T
    Node.vecToNodes(force_vec, 'loads')
    return force_vec

# Helper function, for clarity :          
def eliminateUnknown(K, ind):
    K[ind, :] = 0
    K[:, ind] = 0
    K[ind, ind] = 1

def write_report(fname='report.txt'):
    '''Writes a report with the results of the analysis.'''

    with open(fname, 'w') as f:
        f.write('Results of the analysis\n\n')
        
        # Displacements
        f.write('Displacements\n')
        displacements_table = [[node.id, node.u1u2[0], node.u1u2[1], np.linalg.norm(node.u1u2)] for node in Node.nodes.values()]
        f.write(tabulate(displacements_table, headers=['Node', 'u_1', 'u_2', 'Magnitude'], tablefmt='rounded_outline'))
        f.write('\n\n')
        
        # Strains
        f.write('Strains\n')
        strains_table = [[element.id, element.getStrain()] for element in Element.elements.values()]
        f.write(tabulate(strains_table, headers=['Element', 'Strain'], tablefmt='rounded_outline'))
        f.write('\n\n')
        
        # Stresses
        f.write('Stresses\n')
        stresses_table = [[element.id, element.getStress()] for element in Element.elements.values()]
        f.write(tabulate(stresses_table, headers=['Element', 'Stress'], tablefmt='rounded_outline'))
        f.write('\n\n')
        
        # Forces
        f.write('Forces\n')
        forces_table = np.array([[node.id, node.loads[0], node.loads[1], np.linalg.norm(node.loads)] for node in Node.nodes.values()])
        f.write(tabulate(forces_table, headers=['Node', 'F_x', 'F_y', 'Magnitude'], tablefmt='rounded_outline'))
        f.write('\n\n')
        
        # Reactions
        f.write('Reactions\n')
        reactions_table = []
        for node in Node.nodes.values():
            for i, BC in enumerate(node.BCs):
                if not np.isnan(BC):
                    reactions_table.append([node.id, i, node.loads[i]])
        f.write(tabulate(reactions_table, headers=['Node', 'Axis', 'Reaction'], tablefmt='rounded_outline'))
        f.write('\n\n')
        
        # Global stiffness matrix
        f.write('Global stiffness matrix\n')
        f.write(tabulate(buildGlobalK(), tablefmt='rounded_grid'))
        f.write('\n\n')
    
        f.write('End of report')
    print(f'Report written to {fname}')


input = InputFile('work1_input_file.txt')
k = buildGlobalK()
const_k, f_vec = constrainGlobalK(k)
uuu = solve_disp(const_k, f_vec)
fff = solveForces(k,uuu)
write_report('report_test_difstrain.txt')
fig, ax = plt.subplots()
draw.draw_structure(ax, plot=False, drawForces=True, drawConstraints=True)#, forces_colors=True)
Node.ToggleDeformation(scale=1000000)
#draw.draw_structure(ax, drawForces=False, drawConstraints=False, colors='u')



#test_all('work1_input_file.txt', 'results_test.txt')
#np.savetxt('test_output.txt', buildGlobalK(), fmt='%13.3e')
