import re
from queryparser.parsetree import ParseTree

def __gettablename(query)->str:

    tablename_re = re.search(r'INTO .*\(',query).group()

    tablename = tablename_re.replace("INTO","").strip()

    tablename = tablename[:tablename.find('(')]
    tablename = tablename.strip()

    return tablename

def __getcolumns(query):
    columns_re = re.search(r'\(.*\).*VALUES', query).group()
    columns_raw = re.sub(r'\).*VALUES',"",columns_re)
    columns_raw = columns_raw.replace("(", "").strip()

    columns = columns_raw.split(",")

    columns = list(map(lambda x: x.strip(), columns))

    return columns

def __getvalues(query):
    values_re = re.search(r'VALUES.*\(.*\);?', query).group()
    values_re = re.sub(r'VALUES.*\(',"",values_re)
    values_raw = values_re.replace(")","").strip()
    values_raw = values_raw.replace(";","").strip()

    values = values_raw.split(",")

    values = list(map(lambda x: x.strip(), values))
    return values


def __getdata(query):

    columns = __getcolumns(query)
    values = __getvalues(query)

    if len(columns)!= len(values):
        raise Exception("Number of columns does not match with number of values")

    return dict(zip(columns,values))

def parse(query):

    query = query.upper()
    parsetree = ParseTree()

    parsetree.table = __gettablename(query)
    parsetree.columnvaluepair = __getdata(query)

    return parsetree
