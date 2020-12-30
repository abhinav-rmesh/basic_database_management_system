import os,re


def count_tables_in_database(database):
    tables = []
    for filename in os.listdir(database):
        if filename.find("meta") != -1:
            name = re.search('(.*?)_meta.json', filename)
            tables.append(name)
    return len(tables)