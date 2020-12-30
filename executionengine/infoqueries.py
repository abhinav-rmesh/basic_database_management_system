import glob
from datastructure.supporting_structures import Metadata
from prettytable import PrettyTable
from datastructure.constants import Metadata as META, ROOT_DIRECTORY
from queryvalidator import common_methods
from queryparser import desc
import os

def gettables(database):
    tables = []
    for file in glob.glob(database+"/*_meta.json"):
        last_slash = file.rindex("/")
        i_meta = file.rindex("_meta")
        tables.append(file[last_slash+1:i_meta])
    return tables

def showtables(database):
    tables = gettables(database)
    ptable = PrettyTable(["Tables"])

    for table in tables:
        ptable.add_row([table])
    print(ptable)

def showdatabases():

    ptable = PrettyTable(["Databases"])

    for database in os.listdir(ROOT_DIRECTORY):
        if os.path.isdir(ROOT_DIRECTORY+"/"+database):
            ptable.add_row([database])

    print(ptable)


def describe(database,query):

    pt = desc.parse(query)
    pt.database = database
    common_methods.validatetable(pt)

    metadata = Metadata(database,pt.table)
    columns = ["Column","Type","Length","PK","FK"]

    ptable = PrettyTable(columns)

    for col in metadata.columns.keys():
        data = []
        data.append(col)
        data.append(metadata.columns[col][META.COLUMNS_TYPE])
        data.append(metadata.columns[col][META.COLUMNS_LENGTH])

        if col in metadata.primarykeys:
            data.append("YES")
        else:
            data.append("-")

        if col in metadata.foreignkeys.keys():
            fk = metadata.foreignkeys[col][META.KEYS_FOREIGN_REF_TABLE]
            fk+="("+metadata.foreignkeys[col][META.KEYS_FOREIGN_REF_COLUMN]+")"
            data.append(fk)
        else:
            data.append("-")

        ptable.add_row(data)

    print(ptable)






