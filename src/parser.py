def isComment(line):
    return line.startswith("**")

def isHeading(line):
    return (line.startswith("*") and not isComment(line))

def getHeading(line):
    heading_name = line[1:].split(",")[0].strip()
    return heading_name

