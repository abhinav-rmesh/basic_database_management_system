# represents row of the table
import json
from datastructure.constants import Metadata as META


class Record:
    def __init__(self):
        self.data = {}
        self.parent = None
        self.left = None
        self.right = None

        self.original = None

    def copy(self):
        record = Record()
        record.original = self

        for key in self.data.keys():
            record.data[key] = self.data[key]

        return record

    def updateoriginal(self):
        for key in self.data.keys():
            self.original.data[key] = self.data[key]

    def updatedata(self, data):
        for key in data.keys():
            self.data[key] = data[key]

    def __eq__(self, other):
        if self is None or other is None:
            return False
        return self.data == other.data


# represents metadata of the table
class Metadata:
    def __init__(self,database = None,tablename = None):
        self.columns = {}
        self.primarykeys = []
        self.foreignkeys = {}

        if tablename is not None:
            self.load(database,tablename)

    def load(self,database,tablename):
        directory = database
        ext = ".json"
        file = directory+"/"+tablename+"_meta"+ext
        with open(file) as f:
            data = json.load(f)

            # read columns
            for column in data[META.COLUMNS]:
                self.columns[column[META.COLUMNS_NAME]] = column
                del self.columns[column[META.COLUMNS_NAME]][META.COLUMNS_NAME]

            # read primary keys
            for primarykey in data[META.KEYS][META.KEYS_PRIMARY]:
                self.primarykeys.append(primarykey)

            # read foreign keys
            for foreignkey in data[META.KEYS][META.KEYS_FOREIGN]:
                self.foreignkeys[foreignkey[META.KEYS_FOREIGN_NAME]] = foreignkey
                del self.foreignkeys[foreignkey[META.KEYS_FOREIGN_NAME]][META.KEYS_FOREIGN_NAME]

    def hascolumn(self, column):
        return column in self.columns.keys()

    def columntype(self, column):
        return self.columns[column][META.COLUMNS_TYPE]

    def columnlength(self, column):
        return self.columns[column][META.COLUMNS_LENGTH]

    def hasprimarykey(self,column):
        pass

    def __str__(self):
        string = ""

        string += "COLUMNS: "
        string += str(self.columns)
        string += '\n'
        string += "PRIMARY KEYS: "
        string += str(self.primarykeys)
        string += '\n'
        string += "FOREIGN KEYS: "
        string += str(self.foreignkeys)
        string += '\n'

        return string
