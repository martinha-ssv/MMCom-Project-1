from ..modules import parser
from ..objects.node import Node
from ..objects.element import Element
import numpy as np

class InputFile():
    def __init__(self, file: str) -> None:
        self.full_text = ''
        with open(file) as f:
            self.full_text = f.readlines()
            self.full_text = [line for line in self.full_text if (not parser.isComment(line))] # WARNING: If we need to implement loads which aren't concentrated forces, we might need some comments (unsure, have to check Abaqus Docs).
            self.headings_content = self.contentParse()

    def contentParse(self):
        '''
        This function parses the full text of the input file and returns a dictionary (```headings_content```) with 
        the headings as keys and the content as values.

        Each time a heading is found, the function will look for the next heading and store 
        the content between the two headings as a list of strings.

        Essentially, if the same heading appears multiple times (e.g., multiple Nset headings), 
        the function will store each of the sections in a list of lines. 

        These are grouped into a bigger list, whose key is the heading.
        '''

        heading_indexes = [i for i in range(len(self.full_text)) if parser.isHeading(self.full_text[i])]
        headings_content = {}

        for i in range(len(heading_indexes)):
            heading_index = heading_indexes[i]
            next_heading_index = heading_indexes[i+1] if i+1 < len(heading_indexes) else len(self.full_text)
            heading, content = parser.getHeading(self.full_text[heading_index])
            if heading not in headings_content.keys():
                headings_content[heading] = []

            # IF heading has content in the same line --> store it in the list (only the content)
            if parser.heading_hasOneLine(self.full_text[heading_index]):
                heading_content = content + self.full_text[heading_index+1:next_heading_index]
            else:
                heading_content = self.full_text[heading_index+1:next_heading_index]
            
            headings_content[heading].append(heading_content)

        return headings_content
            

    def getNodesText(self):
        nodes_text = self.headings_content['Node'][0]
        return nodes_text

    def getNodes(self):
        nodes_txt = [parser.cleanLine(nodeText) for nodeText in self.getNodesText()]
        for node_txt in nodes_txt:
            id = node_txt[0]
            coordinates = node_txt[1:]
            Node(id, coordinates)


    def getElementsText(self):
        elements_text = self.headings_content['Element'][0]
        return elements_text
            
    def getElements(self):
        elements_txt_lst = self.getElementsText()
        elements = [parser.cleanLine(element) for element in elements_txt_lst][1:] # IF upgrading functionality to have different elements -> beware of this
        for element in elements:
            id = element[0]
            node_start = Node.getNodeById(element[1])
            node_end = Node.getNodeById(element[2])
            Element(id, node_start, node_end)
    
    def getSectionText(self):
        return parser.cleanLine(self.headings_content['Solid Section'][0][-1])[0]
            
    def getSection(self):
        section = float(self.getSectionText())
        Element.A_section = section
        return section
    
    def getNsets(self):
        sets = self.headings_content['Nset']
        #for set in sets:
            
        for set in sets:
            name, nodes = parser.parseNodeSetContent(set)
            nodes = [Node.getNodeById(int(node)) for node in nodes]
            Node.Nsets[name] = nodes
    
    def getCLoads(self):
        cloads_txt_list = [parser.cleanLine(cload[0]) for cload in self.headings_content['Cload']]
        for cload_txt in cloads_txt_list:
            set = cload_txt[0]
            for node in Node.Nsets[set]:
                axis = parser.RealToPy_ind(int(cload_txt[1]))
                magnitude = float(cload_txt[2])

                node.loads[axis] = magnitude

    def getBCs(self):
        BCs_txt_list = [BC for BC in self.headings_content['Boundary']]
        BCs_txt_list = [item for sublist in BCs_txt_list for item in sublist] 
        BCs_txt_list = [parser.cleanLine(BC) for BC in BCs_txt_list]
        for BC_txt in BCs_txt_list:
            set = BC_txt[0]
            for node in Node.Nsets[set]:
                    for axis in range(int(BC_txt[1]), int(BC_txt[2])+1):
                        i = parser.RealToPy_ind(axis)
                        if len(BC_txt) == 4:
                            node.BCs[i] = float(BC_txt[3])
                        else:
                            node.BCs[i] = 0

    def getMaterialText(self):
        content = parser.cleanLine(self.headings_content['Elastic'][0][0])
        return content
    
    def getMaterial(self):
        E = float(self.getMaterialText()[0])
        v = float(self.getMaterialText()[1])
        Element.E_young = E
        Element.v_poisson = v
        print(Element.E_young, Element.v_poisson)

    