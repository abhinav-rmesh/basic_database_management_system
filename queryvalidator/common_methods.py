from datastructure.constants import Metadata as META
from datastructure.supporting_structures import Metadata
import datastructure.constants as constants
import logger.querylogging as logger

def validatetable(parsetree):
        directory = parsetree.database
        ext = ".json"
        file = directory+"/"+ parsetree.table + ext

        try:
            open(file,'r')

        except:
            raise Exception("Table Not Found: "+parsetree.table)
            logger.get_event_logger().warning(
                "Table Not Found: "+parsetree.table)

def validatecolumns(parsetree):

    if len(parsetree.columns)==1 and parsetree.columns[0]=="*":
        parsetree.columns = None
        return
    metadata = Metadata(parsetree.database,parsetree.table)

    for column in parsetree.columns:
        if not metadata.hascolumn(column):
            raise Exception("Column '{}' does not exist in table '{}'".format(column,parsetree.table))
            logger.get_event_logger().warning("Column '{}' does not exist in table '{}'".format(column,parsetree.table))

def checkdatatype(metadata,column,value):

    if value=="NULL":
        return

    datatype = metadata.columntype(column)

    if datatype== META.VARCHAR:
        if value[0]!=value[-1] or (value[0]!="'" and value[0]!='"'):
            raise Exception("Invalid data '{}' for column '{}'".format(value,column))
            logger.get_event_logger().warning(
                "Invalid data '{}' for column '{}'".format(value,column))

    if datatype== META.INT:
        if value.find(".")!=-1:
            raise Exception("For column: {}\nExpecting: {}\nProvided: {}".format(column,datatype,value))
            logger.get_event_logger().warning(
                "For column: {}\nExpecting: {}\nProvided: {}".format(column,datatype,value))
        try:
            int(value)
        except:
            raise Exception("For column: {}\nExpecting: {}\nProvided: {}".format(column,datatype,value))
            logger.get_event_logger().warning(
                "For column: {}\nExpecting: {}\nProvided: {}".format(column,datatype,value))


    if datatype== META.DOUBLE:
        try:
            float(value)
        except:
            raise Exception("For column: {}\nExpecting: {}\nProvided: {}".format(column,datatype,value))
            logger.get_event_logger().warning(
                "For column: {}\nExpecting: {}\nProvided: {}".format(column,datatype,value))

def validatelength(metadata,column,value):

    allowedlength = metadata.columnlength(column)
    givenlength = len(str(value))

    if metadata.columntype(column) == constants.Metadata.DOUBLE:
        givenlength = len(str(value).split(".")[0])

    if givenlength > allowedlength:
        raise Exception("Length Exceeded: {}\nAllowed: {}\nProvided: {}".format(column,allowedlength,givenlength))
        logger.get_event_logger().warning(
            "Length Exceeded: {}\nAllowed: {}\nProvided: {}".format(column,allowedlength,givenlength))

def transformvalue(metadata,dict,column):
    datatype = metadata.columntype(column)

    if dict[column]=='NULL':
        return

    if datatype == META.VARCHAR:
        dict[column] = dict[column][1:-1]
    if datatype == META.INT:
        dict[column] = int(dict[column])
    if datatype == META.DOUBLE:
        dict[column] = float(dict[column])

def transformcomparator(parsetree):
    if parsetree.conditiontype=="=":
        parsetree.conditiontype = constants.Compare.EQ
    elif parsetree.conditiontype=="<":
        parsetree.conditiontype = constants.Compare.LT
    elif parsetree.conditiontype==">":
        parsetree.conditiontype = constants.Compare.GT
    elif parsetree.conditiontype=="<=":
        parsetree.conditiontype = constants.Compare.LE
    elif parsetree.conditiontype==">=":
        parsetree.conditiontype = constants.Compare.GE

def validatecondition(parsetree):
    if parsetree.condition is None:
        return

    metadata = Metadata(parsetree.database,parsetree.table)

    column = list(parsetree.condition.keys())[0]
    value = parsetree.condition[column]

    if not metadata.hascolumn(column):
            raise Exception("Column '{}' does not exist in table '{}'".format(column,parsetree.table))
            logger.get_event_logger().warning(
                "Column '{}' does not exist in table '{}'".format(column,parsetree.table))

    checkdatatype(metadata,column,value)

    transformvalue(metadata,parsetree.condition,column)
    transformcomparator(parsetree)


def validatecolumnvaluepair(parsetree):
    metadata = Metadata(parsetree.database, parsetree.table)
    for pair in parsetree.columnvaluepair:
        column = pair.key
        if not metadata.hascolumn(column):
            raise Exception("Column '{}' does not exist in table '{}'".format(column, parsetree.table))
            logger.get_event_logger().warning(
                "Column '{}' does not exist in table '{}'".format(column, parsetree.table))
