from datastructure.supporting_structures import Metadata
import queryvalidator.common_methods as validator
import logger.querylogging as logger

def validatedata(parsetree):
    metadata = Metadata(parsetree.database,parsetree.table)

    for column in parsetree.columnvaluepair.keys():
        if not metadata.hascolumn(column):
            raise Exception("Column '{}' does not exist in table '{}'".format(column,parsetree.table))
            logger.get_event_logger().warning("Column '{}' does not exist in table '{}'".format(column,parsetree.table))

        validator.checkdatatype(metadata,column,parsetree.columnvaluepair[column])
        validator.transformvalue(metadata,parsetree.columnvaluepair,column)
        validator.validatelength(metadata,column,parsetree.columnvaluepair[column])


def validate(parsetree):
    validator.validatetable(parsetree)
    validatedata(parsetree)
    validator.validatecondition(parsetree)
