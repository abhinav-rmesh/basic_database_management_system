import re

def adding_to_sqldump(database, query):
    location = database + "/" + "sql_dump.sql"
    with open(location, "a") as file:
        file.write("\n")
        file.write(query.upper())

def updating_sql_dump(database, table_name):
    location = database + "/" + "sql_dump.sql"
    with open(location, "r+") as file:
        lines = file.readlines()
        file.seek(0)
        for line in lines:
            if len(line.strip()):
                tablename_re = re.search(r'TABLE .*\(', line).group()
                tablename = tablename_re.replace("TABLE", "").strip()
                tablename = tablename[:tablename.find("(")].strip()
                if tablename != table_name:
                    file.write(line)
        file.truncate()
