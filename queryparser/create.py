import re
import json
import os
from queryparser.parsetree import ParseTree
from queryvalidator import common_methods


def __getdatabasename(query):
    databasename_re = re.search(r'DATABASE .*$', query).group()
    databasename = databasename_re.replace("DATABASE", "").strip()
    return databasename


def __gettablename(database,query):
    tablename_re = re.search(r'TABLE .*\(', query).group()
    tablename = tablename_re.replace("TABLE", "").strip()
    tablename = tablename[:tablename.find("(")].strip()

    if os.path.exists(database+"/"+tablename+".json"):
        raise Exception("Table {} Already Exists".format(tablename))
    return tablename


def __getcolumns(database,query):
    columns = re.search(r'\(.*\)', query).group()
    columns = columns[1:-1].strip().split(",")
    columns = list(map(lambda x:x.strip(),columns))
    metadata = {"columns":[], "keys": {"primary":[],"foreign":[]}}
    columns_names = []
    columnlist = []
    for e in columns:
        pair = list(map(lambda x: x.strip(), e.split()))
        if pair[0] == "PRIMARY":
            primarykey = re.search(r'\(.*\)', e).group()
            primarykey = primarykey[1:-1].split(",")
            primarykey = list(map(lambda x: x.strip(), primarykey))

            for key in primarykey:
                if key not in columns_names:
                    raise Exception("Primary Key {} is Unknown".format(key))

            metadata["keys"]["primary"].append(primarykey[0])
        elif pair[0] == "FOREIGN":
            parts = e.split()
            parts = list(map(lambda x: x.strip(), parts))

            col = parts[2][1:-1]
            if col not in columns_names:
                    raise Exception("Foreign Key {} is Unknown".format(col))

            ref_table = parts[4][:parts[4].find("(")]
            ref_col = parts[4][parts[4].find("(")+1:-1]

            parsetree = ParseTree()
            parsetree.table = ref_table
            parsetree.columns = [ref_col]
            parsetree.database = database

            common_methods.validatetable(parsetree)
            common_methods.validatecolumns(parsetree)

            foreign_key = {"name":col,"ref_table":ref_table,"ref_column":ref_col}

            metadata["keys"]["foreign"].append(foreign_key)
        elif "INT" in pair[1]:
            column = {}
            column["name"] = pair[0]
            datatype = "INT"
            length = re.search(r'\(.*\)', e).group()
            length = int(length[1:-1])
            column["type"] = datatype
            column["length"] = int(length)
            columnlist.append(column)
            columns_names.append(pair[0])
        elif "VARCHAR" in pair[1]:
            column = {}
            column["name"] = pair[0]
            datatype = "VARCHAR"
            length = re.search(r'\(.*\)', e).group()
            length = int(length[1:-1])
            column["type"] = datatype
            column["length"] = int(length)
            columnlist.append(column)
            columns_names.append(pair[0])
        elif "DOUBLE" in pair[1]:
            column = {}
            column["name"] = pair[0]
            datatype = "DOUBLE"
            length = re.search(r'\(.*\)', e).group()
            length = int(length[1:-1])
            column["type"] = datatype
            column["length"] = int(length)
            columnlist.append(column)
            columns_names.append(pair[0])
        else:
            raise Exception("Error in Create Query")
        metadata["columns"] = columnlist

    return metadata


def parse(database,query,user):
    query = query.upper()
    parts = query.split()
    if parts[1] == "DATABASE":
        if len(parts) != 3:
            raise Exception("Invalid 'Create Database' query")
        try:
            database = __getdatabasename(query)
            os.mkdir("dbms/" + database)
            file = open("dbms/"+database+"/permission.json", "w")
            permission = {"owner":user,"users":[]}
            json.dump(permission,file)
            file.close()

            file = open("dbms/" + database + "/locks.json", "w")
            file.write("[]")
            file.close()

            print("Database {} Created Successfully".format(database))
        except Exception as e:
            print(e)
    elif parts[1] == "TABLE":
        tablename = __gettablename(database,query)
        columnlist = __getcolumns(database,query)
        with open(database+"/"+tablename + "_meta.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(columnlist, indent=4, ensure_ascii=False))
        file = open(database+"/"+tablename + ".json", "w", encoding="utf-8")
        file.write("[]")
        file.close()
        print("Table {} Created Successfully".format(tablename))
    else:
        raise Exception("Invalid 'Create' query structure")
