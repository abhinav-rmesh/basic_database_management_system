import re
from datastructure import constants
from queryparser.parsetree import ParseTree

def __gettablename(query):
    tablename_re = re.search(r'UPDATE .* SET', query).group()
    tablename = tablename_re.replace("UPDATE", "").replace("SET", "").strip()
    return tablename


def __getcolumnvaluepairs(query):
    columnvaluepairs_re = re.search(r'SET .* WHERE', query).group()
    columnvaluepairs_raw = columnvaluepairs_re.replace("SET", "").replace("WHERE", "").strip()
    columnvaluepairs = columnvaluepairs_raw.split(",")
    pairlist = {}
    for e in columnvaluepairs:
        condition = list(map(lambda x: x.strip(), e.split("=")))
        pairlist[condition[0]]= condition[1]
    return pairlist


def __getcondition(query):
    condition_re = re.search(r'WHERE .*', query).group()
    condition_raw = condition_re.replace("WHERE", "").strip()
    comparator = ""
    for operator in constants.ALLOWED_COMPARATORS:
        if condition_raw.find(operator) != -1:
            if (operator == '<' or operator == '>') and condition_raw[condition_raw.find(operator) + 1] == '=':
                continue
            if operator == "=" and (condition_raw[condition_raw.find(operator) - 1] == '<' or condition_raw[condition_raw.find(operator) - 1] == '>'):
                continue
            comparator += operator
    if comparator == "":
        raise Exception("Only <,>,=,<=,>= operators are allowed")
    if len(comparator) > 1 and (comparator != "<=" and comparator != ">="):
        raise Exception("Only <,>,=,<=,>= operators are allowed")
    condition = condition_raw.split(comparator)
    condition = list(map(lambda x: x.strip(), condition))
    conditiondic = {condition[0]: condition[1]}
    return conditiondic, comparator


def parse(query):
    parsetree = ParseTree()
    query = query.upper()
    parsetree.table = __gettablename(query)
    parsetree.columnvaluepair = __getcolumnvaluepairs(query)
    parsetree.condition, parsetree.conditiontype = __getcondition(query)
    return parsetree



