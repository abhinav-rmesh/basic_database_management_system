from queryparser.parsetree import ParseTree
import re


def validate_query(query):
    pattern = re.compile('DELETE\s+FROM\s+(.*?)\s*(WHERE\s(.*?)\s*)?', re.IGNORECASE)
    if pattern.match(query):
        return True
    else:
        return False


def extract_table_name(query):
    if query.find("WHERE") !=-1:
        name = re.search('FROM(.*)WHERE', query)
        # print(f"the table name is : {name.group(1).strip()}")
        return name.group(1).strip(), True
    else:
        name = re.search('FROM(.*)', query)
        # print(f"the table name is : {name.group(1).strip()}")
        return name.group(1).strip(), False


def extract_column_value_pair(query):
    operators = ['<=', '>=', '=', '<', '>']
    for operator in operators:
        result = re.search('WHERE (.*)'+operator+'(.*)', query)
        if result is not None:
            column_name = result.group(1).strip()
            pattern = re.compile('^[a-zA-Z0-9 ]*$')
            if not pattern.match(column_name):
                raise Exception("Only specific operation are allowed")
                break
            column_value = result.group(2).strip()
            # print(f"the column name is {column_name} and the column value is {column_value}")
            column_value_pair = {column_name: column_value}
            return column_value_pair, operator
        else:
            continue


def parse(delete_query):
    parsetree = ParseTree()
    delete_query = delete_query.upper()
    delete_query = re.sub(r"\s+", " ", delete_query)
    delete_query.strip()
    delete_query = delete_query.replace(";","")
    if not validate_query(delete_query):
        raise Exception("The Delete query is not valid")
    table_name, where_flag = extract_table_name(delete_query)
    if where_flag:
        column_value_dictionary,  operator_value = extract_column_value_pair(delete_query)
        parsetree.table = table_name
        parsetree.condition = column_value_dictionary
        parsetree.conditiontype = operator_value
        return parsetree
    else:
        parsetree.table = table_name
        return parsetree
