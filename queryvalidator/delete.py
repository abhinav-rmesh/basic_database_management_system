import queryvalidator.common_methods as validator


def validate(parsetree):
    validator.validatetable(parsetree)
    if parsetree.condition is not None:
        validator.validatecondition(parsetree)