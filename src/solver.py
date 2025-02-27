from modules import parser as p
from modules.file_input import InputFile
from objects.node import Node
from objects.element import Element
from modules.draw import Artist
import modules.draw as draw
from pprint import pprint
import numpy as np
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



'''input = InputFile('work1_input_file.txt') #('~/Downloads/Job-1.inp')
k = buildGlobalK()
const_k, f_vec = constrainGlobalK(k)
uuu = solve_disp(const_k, f_vec)
fff = solveForces(k,uuu)'''




# BUG the bug on the interface is because we can't genereate matplotlib figs outside canvases in the tk window I THINK
'''fig, ax = plt.subplots()
artist = Artist(fig, ax, master=None)
draw.draw_structure(artist, plot=False, forces=False, constraints=True, colors=False, element_numbers=False, deformed=False)
draw.draw_structure(artist, forces=False, constraints=False, colors='stress', element_numbers=False, deformed=True)

'''