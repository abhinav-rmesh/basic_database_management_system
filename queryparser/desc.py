from queryparser.parsetree import ParseTree
def parse(query):
    query = query.upper()
    parts = query.split(" ")

    if len(parts)!=2:
        raise Exception("Invalid Format of Describe Table Query")

    parsetree = ParseTree()
    parsetree.table = parts[1]

    return parsetree