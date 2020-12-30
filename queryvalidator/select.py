import queryvalidator.common_methods as validator


def validate(parsetree):
    validator.validatetable(parsetree)
    validator.validatecolumns(parsetree)
    validator.validatecondition(parsetree)

# try:
# pt = select.parse("select firstname from EMP where id = 1")
# validate(pt)
# except Exception as e:
#     print(e)