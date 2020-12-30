import queryparser.delete as parsedelete
import queryvalidator.delete as validatedelete
from datastructure.table import Table
from transaction import helper
from datastructure import constants
import logger.querylogging as logger


def execute(database, query, transaction=None):
    try:
        parsetree = parsedelete.parse(query)
        parsetree.database = database
        validatedelete.validate(parsetree)

        lock = helper.typeoflock(database, parsetree.table)
        if transaction==None:
            if lock !=None:
                logger.get_event_logger().warning("Table {} is locked by a transaction".format(parsetree.table))
                raise Exception("Table {} is locked by a transaction".format(parsetree.table))
            table = Table(database, parsetree.table)
        else:
            if parsetree.table in transaction.accessed_tables.keys():
                table = transaction.accessed_tables[parsetree.table]
            else:
                if lock ==None:
                    table = Table(database, parsetree.table, parsetree.columns)
                    helper.locktable(database, parsetree.table, constants.SHARED)
                    transaction.accessed_tables[parsetree.table] = table
                else:
                    logger.get_event_logger().warning("Table {} is locked by a transaction".format(parsetree.table))
                    raise Exception("Table {} is locked by a transaction".format(parsetree.table))
        records_before_deletion = len(table.iterator())
        if parsetree.condition is not None:
            column = list(parsetree.condition.keys())[0]
            value = parsetree.condition[column]
            table.delete(column, value, parsetree.conditiontype)
            table.columns = parsetree.columns
            records_after_deletion = len(table.iterator())
            total_records_deleted = records_before_deletion - records_after_deletion
            print(f"{total_records_deleted} records have been successfully deleted")
            logger.get_event_logger().info(f"{total_records_deleted} records have been successfully deleted")
        else:
            table.deletetable()
            print(f"{parsetree.table} table has been successfully deleted")
            logger.get_event_logger().info(f"{parsetree.table} table has been successfully deleted")

        if transaction==None:
            table.save()

    except Exception as e:
        print(e)
