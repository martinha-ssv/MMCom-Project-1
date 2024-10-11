from src.modules import parser
from src.modules import file_input
from src.objects.node import Node
from src.objects.element import Element
from src.modules import draw
from pprint import pprint
from datetime import datetime

def test_getHeading():
    heading = parser.getHeading("*Heading")
    assert heading == "Heading", "Should be Heading but was " + str(heading)
    assert parser.getHeading("*Heading, title") == "Heading", "Should be Heading but was " + str(heading)
    assert parser.getHeading("**Heading, title") == None,  "Line is a comment"

def test_getHeading_all(file):
    lines = ''
    headings = []
    with open(file) as f:
        lines = f.readlines()
    for line in lines:
        if parser.isHeading(line):
            heading, _ = parser.getHeading(line)
            headings.append(heading)
    pprint(headings)

# test_getHeading_all('work1_input_file.txt')

# print(parser.parseNodeSetContent(['nset=Set-6','instance=Part-1-1','2']))

def test_all(file, out=False):
    input_file = file_input.InputFile(file)
    pprint(input_file.headings_content)
    input_file.getNodes()
    input_file.getNsets()
    input_file.getElements()
    input_file.getSection()
    input_file.getMaterial()
    input_file.getCLoads()
    input_file.getBCs()
    Element.getAllKes()
    print("NODES ######################################")
    pprint(Node.nodes)
    print("NSETS ######################################")
    pprint(Element.elements)
    for test_element in Element.elements.values(): print(test_element.Ke ,'\n')
    
    #draw.draw()

    if out:
        with open(out, 'w') as output_file:
            output_file.write(f"File written at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            output_file.write("NODES ######################################\n")
            pprint(Node.nodes, stream=output_file)
            output_file.write("ELEMENTS ######################################\n")
            pprint(Element.elements, stream=output_file)
            output_file.write("MATRICES ######################################\n")
            for test_element in Element.elements.values():
                output_file.write("E"+str(test_element.id) + '\n')
                output_file.write(str(test_element.Ke) + '\n\n')
            output_file.write("NODE BOUNDARY CONDITIONS\n")
            for node in Node.nodes.values():
                output_file.write("N" + str(node.id) + '\n')
                output_file.write(str(node.BCs)+'\n\n')
            
    



#test_all('work1_input_file.txt', 'output_withbcs.txt')

#pprint(input_file.headings_content)
