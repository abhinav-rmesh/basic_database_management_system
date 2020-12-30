from queryparser.parsetree import ParseTree
import datastructure.constants as constants
import re

def __gettablename(query):

    if query.find("WHERE")!=-1:
        tablename_re = re.search(r'FROM .* WHERE',query).group()

        tablename = tablename_re.replace("FROM","").replace("WHERE","").strip()

    else:
        tablename_re = re.search(r'FROM .*',query).group()

        tablename = tablename_re.replace("FROM","").strip()
        tablename = tablename.replace(";","").strip()

    return tablename

def __getcolumns(query):

    columns_re = re.search(r'SELECT .* FROM',query).group()
    columns_raw = columns_re.replace("SELECT","").replace("FROM","").strip()

    if columns_raw == "*":
        return ["*"]

    columns = columns_raw.split(",")

    columns = list(map(lambda x: x.strip(), columns))

    return columns

def __getcondition(query):
    if query.find("WHERE")==-1:
        return None,None

    condition_re = re.search(r'WHERE .*;?',query).group()

    condition_raw = condition_re.replace("WHERE","").strip()
    condition_raw = condition_raw.replace(";","").strip()

    comparator = ""
    for operator in constants.ALLOWED_COMPARATORS:
        if condition_raw.find(operator)!=-1:
            if (operator=='<' or operator=='>') and condition_raw[condition_raw.find(operator)+1]=='=':
                continue

            if operator=="=" and (condition_raw[condition_raw.find(operator)-1]=='<' or condition_raw[condition_raw.find(operator)-1]=='>'):
                continue
            comparator+=operator

    if comparator == "":
        raise Exception("Only <,>,=,<=,>= operators are allowed")

    if len(comparator)>1 and (comparator!="<=" and comparator!=">="):
        raise Exception("Only <,>,=,<=,>= operators are allowed")

    condition = condition_raw.split(comparator)

    condition = list(map(lambda x: x.strip(),condition))

    conditiondic = {condition[0]: condition[1]}

    return conditiondic,comparator

def parse(query):
    parsetree = ParseTree()

    query = query.upper()

    parsetree.table = __gettablename(query)
    parsetree.columns = __getcolumns(query)
    parsetree.condition,parsetree.conditiontype = __getcondition(query)


    return parsetree
