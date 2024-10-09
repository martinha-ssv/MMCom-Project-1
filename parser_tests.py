from src.modules import parser
from src.modules import file_input
from src.objects.node import Node
from src.objects.element import Element
from pprint import pprint

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

def test_getNsets(file):
    input_file = file_input.InputFile(file)
    pprint(input_file.headings_content)
    input_file.getNodes()
    pprint(Node.nodes)
    input_file.getNsets()
    pprint(Node.Nsets)
    input_file.getElements()
    pprint(Element.elements)
    input_file.getSection()
    input_file.getMaterial()
    print(Element.elements[1].Ke())



test_getNsets('work1_input_file.txt')

#pprint(input_file.headings_content)
