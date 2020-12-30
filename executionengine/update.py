from queryparser import update
import queryvalidator.update as validateupdate
from datastructure.table import Table
from transaction import helper
from datastructure import constants
import logger.querylogging as logger


def execute(database, query,transaction = None):
    try:
        parsetree = update.parse(query)
        parsetree.database = database
        validateupdate.validate(parsetree)

        lock = helper.typeoflock(database, parsetree.table)

        if transaction == None:
            if lock != None:
                raise Exception("Table {} is locked by a transaction".format(parsetree.table))
                logger.get_event_logger().warning("Table {} is locked by a transaction".format(parsetree.table))

            table = Table(database, parsetree.table)
        else:
            if parsetree.table in transaction.accessed_tables.keys():
                table = transaction.accessed_tables[parsetree.table]
            else:
                if lock != None:
                    raise Exception("Table {} is locked by a transaction".format(parsetree.table))
                    logger.get_event_logger().warning("Table {} is locked by a transaction".format(parsetree.table))
                table = Table(database, parsetree.table, parsetree.columns)
                helper.locktable(database, parsetree.table, constants.EXCLUSIVE)
                transaction.accessed_tables[parsetree.table] = table

        column = list(parsetree.condition.keys())[0]
        value = parsetree.condition[column]
        rows = table.update(parsetree.columnvaluepair, column, value, parsetree.conditiontype)

        print("{} Rows Updated".format(rows))
        logger.get_event_logger().info("{} Rows Updated".format(rows))
        if transaction==None:
            table.save()
    except Exception as e:
        print(e)