def cleanLine(line):
    return [word.strip(' ') for word in line.strip('\n').split(',')]

def isComment(line):
    return line.startswith("**")

def isHeading(line):
    return (line.startswith("*") and not isComment(line))

def getHeading(line):
    heading_name = line[1:].split(",")[0].strip()
    content = cleanLine(line[1:])[1:] if ("," in line) else None
    return heading_name, content

def heading_hasOneLine(line):
    return (line.startswith("*") and not isComment(line) and ("," in line))


def parseNodeSetContent(Nset_content):
    '''Takes in the list of fields in the Nset section and returns the 
    name of the set and the node IDs in said set.'''
    name = Nset_content[0].split("=")[1]
    if 'generate' in Nset_content:
        node_content = cleanLine(Nset_content[2])
        start= int(node_content[0])
        end = int(node_content[1])
        step = int(node_content[2])
        nodes = [i for i in range(start, end+1, step)]
    else:
        nodes = [line.strip(',\n') for line in Nset_content[2:]]
    return name, nodes