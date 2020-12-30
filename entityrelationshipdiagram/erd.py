import json, os, re
import logger.querylogging as logger


def generating_erd(database):

    table_attributes = []
    erd_file = database + "/erd.txt"
    file = open(erd_file, "w")
    try:
        for filename in os.listdir(database):
            if filename.find("meta") != -1:
                name = re.search('(.*?)_meta.json', filename)
                file.write(f"\nThe name of the table is : {name.group(1).strip()}")
                with open(database + "/" + filename) as f:
                    file_content = json.load(f)
                columns = file_content['columns']
                for column in columns:
                    table_attributes.append(column['name'])
                file.write(f"\nThe Attributes of the table are : {table_attributes}")
                keys = file_content['keys']
                primary_key =  keys['primary']
                file.write(f"\nThe Primary key is : {primary_key}")
                foreign_key_details = keys['foreign']
                for foreign_key_detail in foreign_key_details:
                    foreign_key_name = foreign_key_detail['name']
                    foreign_key_table = foreign_key_detail['ref_table']
                    file.write(f"\nThe Foreign key is : {foreign_key_name}. It is the primary key for the table : {foreign_key_table}")
                    if foreign_key_name in primary_key:
                        file.write(f"\nThe Cardinality between the \"{name.group(1).strip()}\" table and \"{foreign_key_table}\" table is : 1 to 1")
                    else:
                        file.write(f"\nThe Cardinality between the \"{name.group(1).strip()}\" table and \"{foreign_key_table}\" table is : 1 to Many")
                file.write("\n")
                file.write(" -"*35)
        file.close()
        logger.get_event_logger().info(f"Generated ERD")
        return
    except Exception as e:
        print(e)
