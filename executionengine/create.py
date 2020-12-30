from queryparser import create
import sqldump.sqldumpcreation as sqldump


def execute(database,query,user):
    try:
        create.parse(database,query,user)
        sqldump.adding_to_sqldump(database, query)
    except Exception as e:
        print(e)
        return None



#execute("create database group")
#execute("create table emp (id int, name varchar(45))")
