import os.path
from queryparser import use
from accessuser import authentication
from datastructure.constants import ROOT_DIRECTORY
import logger.querylogging as logger
import logger.databaseparser as counter

def execute(query,user):
    try:
        database = use.parse(query)

        if os.path.exists(ROOT_DIRECTORY+"/"+database):
            if not authentication.hasaccess(user, database):
                print("Does not have access to the database")
                return None
            print("Database Selected: '{}'".format(database))
            logger.get_general_logger().info("Database Selected: '{}'".format(database))
            logger.get_event_logger().info("Database Selected: '{}'".format(database))
            database_val = ROOT_DIRECTORY+"/"+database
            logger.get_general_logger().info(
                f"The total number of tables in the database are {counter.count_tables_in_database(database_val)}")
            return ROOT_DIRECTORY+"/"+database
        print("Database does not exist '{}'".format(database))
        return None
    except Exception as e:
        print(e)
        return None

