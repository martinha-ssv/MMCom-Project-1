import sys
sys.path.append('..')
import src.parser as parser
import pprint

def test_getHeading():
    heading = parser.getHeading("*Heading")
    assert heading == "Heading", "Should be Heading but was " + str(heading)
    assert parser.getHeading("*Heading, title") == "Heading", "Should be Heading but was " + str(heading)
    assert parser.getHeading("**Heading, title") == None,  "Line is a comment"

def test_getHeadings(file):
    lines = ''
    headings = []
    with open(file) as f:
        lines = f.readlines()
    for line in lines:
        if parser.isHeading(line):
            headings.append(parser.getHeading(line))
    pprint.pprint(headings)

test_getHeadings('work1_input_file.txt')