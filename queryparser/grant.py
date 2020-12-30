import json
from accessuser import authentication
import os


def parse(query,owner):
    database = query.split()[1].upper()
    user = query.split()[2]

    if not authentication.userexist(user):
        print("User {} does not exists".format(user))
        return

    if not os.path.exists("dbms/"+database):
        print("Database {} does not exists".format(database))
        return

    if not authentication.isowner(owner,database):
        print("You are not owner of database {}".format(database))
        return

    path = "dbms/" + database + "/" + "permission.json"
    file = open(path, "r")
    permission = json.load(file)
    file.close()
    permission["users"].append(user)
    with open(path, "w", encoding="utf-8") as file:
        file.write(json.dumps(permission, indent=4, ensure_ascii=False))

    print("{} granted permission of {}".format(user,database))

