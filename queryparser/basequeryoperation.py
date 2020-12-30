from datastructure.constants import Operation
import datastructure.constants as const

def findoperation(query):
    operation = query.split(" ")[0].upper()
    query = query.replace(";","")

    if operation == 'SELECT':
        return Operation.SELECT
    if operation == 'INSERT':
        return Operation.INSERT
    if operation == 'UPDATE':
        return Operation.UPDATE
    if operation == 'DELETE':
        return Operation.DELETE
    if operation == 'CREATE':
        return Operation.CREATE
    if operation == 'DROP':
        return Operation.DROP
    if operation == 'EXIT':
        return Operation.EXIT
    if operation == 'USE':
        return Operation.USE
    if operation == 'GRANT':
        return Operation.GRANT
    if operation == 'REVOKE':
        return Operation.REVOKE
    if operation == "DESC":
        return Operation.DESC

    if query.upper() == const.START_TRANSACTION:
        return Operation.STRT_TRNAS
    if query.upper() == const.COMMIT:
        return Operation.COMMIT
    if query.upper() == const.ROLLBACK:
        return Operation.ROLLBACK
    if query.upper() == const.SHOW_TABLES:
        return Operation.SHW_TBLS
    if query.upper() == const.SHOW_DATABASES:
        return Operation.SHW_DTBS
    return None