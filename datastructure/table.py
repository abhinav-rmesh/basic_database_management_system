from datastructure.supporting_structures import Record, Metadata
import datastructure.constants as constant
import json


class Table:

    # essential methods
    def __init__(self,database=None, tablename=None, columns=None):
        self.root = None
        self.sort_col = None
        self.tablename = tablename
        self.database = database
        self.columns = columns

        if tablename is None:
            self.metadata = Metadata()
        else:
            self.load(database,tablename)
        pass

    # load the datastructure with the table data
    # tablename = name of the table
    # columns (optional) = list of columns to load
    def load(self, database,tablename):

        self.metadata = Metadata(database,tablename)

        directory = database
        ext = ".json"
        file = directory+"/"+tablename+ext

        with open(file) as f:
            tabledata = json.load(f)

            for data in tabledata:
                record = Record()
                record.data = data

                self.insert(record)

    # filter the table records and return new table object
    # column = column to use for filtering
    # value = value of column to use for filtering
    # option = comparison operator =,<,>,<=,>= , default is =
    def filter(self, column, value, option=constant.Compare.EQ):
        table = Table()
        table.metadata = self.metadata

        # self.__filter(table,self.root,column,value,option)

        for node in self.iterator():
            if (option==constant.Compare.EQ or option==constant.Compare.LE or option==constant.Compare.GE) and node.data[column]==value:
                table.insert(node.copy())

            if (option==constant.Compare.LT or option==constant.Compare.LE) and node.data[column]<value:
                table.insert(node.copy())

            if (option==constant.Compare.GT or option==constant.Compare.GE) and node.data[column]>value:
                table.insert(node.copy())

        return table

    # under development
    # the idea was to use for update
    # it will filter the table using the condition in the update query
    # filter method will give new table with only records that follow condition
    # those filtered records will be updated according to query
    # now the filtered table will be merged with the actual table to update the original table
    def update(self, columnvaluepairs,column,value,option):

        filteredtable = self.filter(column,value,option)

        for node in filteredtable.iterator():
            node.updatedata(columnvaluepairs)
            node.updateoriginal()

        return len(filteredtable.iterator())
    # delete the records that satisfy given condition
    # column = column given in condition
    # value = value of column
    # option = comparison operator =,<,>,<=,>= , default is =
    def delete(self, column, value, option=constant.Compare.EQ):

        for node in self.iterator():
            if (option == constant.Compare.EQ or option == constant.Compare.LE or option == constant.Compare.GE) and \
                    node.data[column] == value:
                self.__deletenode(node)

            if (option == constant.Compare.LT or option == constant.Compare.LE) and node.data[column] < value:
                self.__deletenode(node)

            if (option == constant.Compare.GT or option == constant.Compare.GE) and node.data[column] > value:
                self.__deletenode(node)

    # Deleting the complete table
    def deletetable(self):
        if self.root is not None:
            self.root = None

    # insert new record in the table
    # record = object of type Record
    def insert(self, record):
        if self.root is None:
            self.root = record
            return
        self.__insertrecord(record, self.root)
        self.__balance(self.root)

    def __deletenode(self, searchednode):

        if searchednode is None:
            return None

        if searchednode.left is None and searchednode.right is None and searchednode == self.root:
            self.root = None
            return

        replacementnode = self.__getbiggest(searchednode.left)

        if replacementnode is None:
            if searchednode.right != None:
                searchednode.right.parent = searchednode.parent

            if searchednode !=self.root and searchednode.parent.right == searchednode:
                searchednode.parent.right = searchednode.right
            elif searchednode !=self.root and searchednode.parent.left == searchednode:
                searchednode.parent.left = searchednode.right

            if searchednode==self.root:
                self.root = searchednode.right
            return

        self.__swap(searchednode, replacementnode)

    def __swap(self, node1, node2):

        if node2==None and node1!=self.root:
            if node1.parent.right == node1:
                node1.parent.right = None

            if node1.parent.left == node1:
                node1.parent.left = None
            return

        if node2.parent.right == node2:
            node2.parent.right = node2.left

        elif node2.parent.left == node2:
            node2.parent.left = node2.left

        if node1!=self.root and node1.parent.right == node1:
            node1.parent.right = node2

        elif node1!=self.root and node1.parent.left == node1:
            node1.parent.left = node2

        node2.parent = node1.parent
        node2.left = node1.left
        node2.right = node1.right

        if node2.left!=None:
            node2.left.parent = node2

        if node2.right != None:
            node2.right.parent = node2

        if node1==self.root:
            self.root = node2
    def __swapparent(self, node1, node2):

        if node1 is None or node2 is None:
            return
        if self.root == node1:
            self.root = node2
            node2.parent = None
            return

        if node1.parent.right == node1:
            node1.parent.right = node2
        else:
            node1.parent.left = node2

        node2.parent = node1.parent

    def __insertrecord(self, record, node):
        nodevalue = self.__keyvalues(node)
        recordvalue = self.__keyvalues(record)

        if nodevalue == recordvalue:
            raise Exception("Primary key constraint violation")

        if recordvalue < nodevalue:
            if node.left is None:
                node.left = record
                record.parent = node
                return
            self.__insertrecord(record, node.left)
            return

        if node.right is None:
            node.right = record
            record.parent = node
            return
        self.__insertrecord(record, node.right)
        return

    def __balance(self, node):
        if node is None:
            return

        self.__balance(node.left)
        self.__balance(node.right)

        depthleft = self.__depth(node.left)
        depthright = self.__depth(node.right)

        if depthleft - depthright > 1:
            self.__leftrotate(node)
            return

        if depthright - depthleft > 1:
            self.__rightrotate(node)

    def __depth(self, node):
        if node is None:
            return 0
        return 1 + max(self.__depth(node.left), self.__depth(node.right))

    def __leftrotate(self, node):
        if node.left.right is not None:
            self.__rightrotate(node.left)

        if node.parent is not None:
            if self.__keyvalues(node) < self.__keyvalues(node.parent):
                node.parent.left = node.left
            else:
                node.parent.right = node.left

        else:
            self.root = node.left

        node.left.parent = node.parent
        node.parent = node.left

        node.left = node.left.right

        if node.left is not None:
            node.left.parent = node

        node.parent.right = node

    def __rightrotate(self, node):

        if node.right.left is not None:
            self.__leftrotate(node.right)
        if node.parent is not None:
            if self.__keyvalues(node) < self.__keyvalues(node.parent):
                node.parent.left = node.right
            else:
                node.parent.right = node.right

        else:
            self.root = node.right

        node.right.parent = node.parent
        node.parent = node.right

        node.right = node.right.left

        if node.right is not None:
            node.right.parent = node

        node.parent.left = node

    def __getbiggest(self, node):
        if node is None:
            return None
        if node.right is None:
            return node

        return self.__getbiggest(node.right)

    def __getsmallest(self, node):
        if node is None:
            return None
        if node.left is None:
            return node

        return self.__getsmallest(node.left)

    def __keyvalues(self, record, keys=None):
        value = ""

        if keys is None:
            keys = self.metadata.primarykeys

        if record is None:
            return value

        for key in keys:
            value += str(record.data[key])

        return value

    # save the table in the json file
    def save(self):
        jsonlist = []
        self.getjsonlist(jsonlist,self.root)

        directory = self.database
        ext = ".json"
        file = directory +"/"+ self.tablename + ext

        with open(file,'w') as f:
            json.dump(jsonlist,f)

    def getjsonlist(self,list, node):
        if node is None: return

        self.getjsonlist(list,node.left)
        list.append(node.data)
        self.getjsonlist(list,node.right)

    def traverse(self, node):
        if node is None: return

        self.traverse(node.left)
        if self.columns is not None:
            for col in self.columns:
                print(node.data[col])
        else:
            for col in self.metadata.columns:
                print(node.data[col])

        print("---------------")
        self.traverse(node.right)

    def __traverse(self,list, node):
        if node is None: return

        self.__traverse(list,node.left)
        list.append(node)
        self.__traverse(list,node.right)

    def iterator(self):
        nodes = []

        self.__traverse(nodes,self.root)

        return nodes

