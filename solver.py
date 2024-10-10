from src.modules import parser as p
from src.modules.file_input import InputFile
from src.objects.node import Node
from src.objects.element import Element
from src.modules import draw
from pprint import pprint
import numpy as np
from parser_tests import test_all
import copy
import matplotlib.pyplot as plt

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
    K_global_constrained = copy.copy(K)
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
          

'''
input = InputFile('work1_input_file.txt')
k = buildGlobalK()
const_k, f_vec = constrainGlobalK(k)
uuu = solve_disp(const_k, f_vec)
fff = solveForces(k,uuu)

fig, ax = plt.subplots()
draw.draw_structure(ax, plot=False, drawForces=False, drawConstraints=False)
Node.ToggleDeformation(scale=1000000)
draw.draw_structure(ax, drawForces=False, drawConstraints=False)


test_all('work1_input_file.txt', 'results_test.txt')
np.savetxt('test_output.txt', buildGlobalK(), fmt='%13.3e')'''
