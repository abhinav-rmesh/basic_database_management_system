import queryparser.drop as parsedrop
import queryvalidator.drop as validatedrop
from transaction import helper
import os
import logger.querylogging as logger
import sqldump.sqldumpcreation as sqldump

def execute(database, query, transaction=None):
    try:
        parsetree = parsedrop.parse(query)
        parsetree.database = database
        validatedrop.validate(parsetree)

        lock = helper.typeoflock(database, parsetree.table)

        if lock !=None:
            raise Exception("Table {} is locked by a transaction".format(parsetree.table))
            logger.get_event_logger().warning("Table {} is locked by a transaction".format(parsetree.table))

        tablename = parsetree.table
        directory = database
        ext = ".json"
        file = directory + "/" + tablename + ext
        if os.path.exists(file):
            os.remove(file)
            file = directory+"/"+tablename+"_meta"+ext
            os.remove(file)
            sqldump.updating_sql_dump(database, tablename)
            print(f"The {tablename} has been successfully dropped")
            logger.get_event_logger().info(f"The {tablename} has been successfully dropped")

    except Exception as e:
        print(e)