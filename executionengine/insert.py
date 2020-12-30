from datastructure.supporting_structures import Record
import queryparser.insert as parseinsert
import queryvalidator.insert as validateinsert
from datastructure.table import Table
from transaction import helper
from datastructure import constants
import logger.querylogging as logger

def execute(database,query,transaction = None):
    try:
        parsetree = parseinsert.parse(query)
        parsetree.database = database
        validateinsert.validate(parsetree)

        record = Record()
        record.data = parsetree.columnvaluepair

        lock = helper.typeoflock(database, parsetree.table)

        if transaction==None:
            if lock != None:
                raise Exception("Table {} is locked by a transaction".format(parsetree.table))
                logger.get_event_logger().warning("Table {} is locked by a transaction".format(parsetree.table))
            t = Table(database,parsetree.table)
            t.insert(record)
            t.save()
        else:
            if parsetree.table in transaction.accessed_tables.keys():
                table = transaction.accessed_tables[parsetree.table]
            else:
                if lock != None:
                    raise Exception("Table {} is locked by a transaction".format(parsetree.table))
                    logger.get_event_logger().warning("Table {} is locked by a transaction".format(parsetree.table))
                table = Table(database, parsetree.table, parsetree.columns)
                helper.locktable(database,parsetree.table,constants.EXCLUSIVE)
                transaction.accessed_tables[parsetree.table] = table
            table.insert(record)
        print("1 Row inserted successfully")
        logger.get_event_logger().info("1 Row inserted successfully")
    except Exception as e:
        print(e)

