import queryparser.select as parseselect
import queryvalidator.select as validateselect
from datastructure.table import Table
from prettytable import PrettyTable
from transaction import helper
from datastructure import constants
import logger.querylogging as logger

def execute(database,query,transaction=None):
    try:
        parsetree = parseselect.parse(query)
        parsetree.database = database
        validateselect.validate(parsetree)

        lock = helper.typeoflock(database,parsetree.table)
        if transaction==None:
            if lock == constants.EXCLUSIVE:
                raise Exception("Table {} is locked by a transaction".format(parsetree.table))
                logger.get_event_logger().warning("Table {} is locked by a transaction".format(parsetree.table))
            table = Table(database,parsetree.table,parsetree.columns)
        else:
            if parsetree.table in transaction.accessed_tables.keys():
                table = transaction.accessed_tables[parsetree.table]
            else:
                if lock == None or lock == constants.SHARED:
                    table = Table(database, parsetree.table, parsetree.columns)
                    helper.locktable(database,parsetree.table,constants.SHARED)
                    transaction.accessed_tables[parsetree.table] = table
                else:
                    raise Exception("Table {} is locked by a transaction".format(parsetree.table))
                    logger.get_event_logger().warning("Table {} is locked by a transaction".format(parsetree.table))

        if parsetree.condition is not None:
            column = list(parsetree.condition.keys())[0]
            value = parsetree.condition[column]
            table = table.filter(column,value,parsetree.conditiontype)
            table.columns = parsetree.columns

        if parsetree.columns is None:
            columns = table.metadata.columns
        else:
            columns = parsetree.columns
        ptable = PrettyTable(columns)

        for row in table.iterator():
            data = []
            for column in columns:
                data.append(row.data[column])
            ptable.add_row(data)
        print(ptable)
    except Exception as e:
        print(e)