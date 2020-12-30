# this object will hold result of the parse tree which can be used later for query execution
class ParseTree:
    def __init__(self):
        self.database = None
        self.table = None
        self.columns = None
        self.columnvaluepair = {} # {column:value, column:value,column:value}
        self.condition = None # {column : value}
        self.conditiontype = None
