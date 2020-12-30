import json
import hashlib

def getmd5(text):
    md5 = hashlib.md5(text.encode())
    return str(md5.hexdigest())

def signup(username, password):
    file = open(r"dbms/user.json", "r")
    userlist = json.load(file)
    new_user = {"name":username, "password":getmd5(password)}
    userlist.append(new_user)
    with open(r"dbms/user.json", "w") as file:
        json.dump(userlist,file)


def userexist(username):
    file = open(r"dbms/user.json", "r")
    userlist = json.load(file)
    file.close()
    for e in userlist:
        if e["name"] == username:
            return True
    return False


def authenticateuser(username, password):
    file = open(r"dbms/user.json", "r")
    userlist = json.load(file)
    file.close()
    for e in userlist:
        if e["name"] == username and e["password"] == getmd5(password):
            return True
    return False


def hasaccess(user,database):
    with open(r"dbms/"+database+"/permission.json", "r") as file:
        file_json = json.load(file)

        if file_json["owner"]==user or user in file_json["users"]:
            return True
        return False

def isowner(user,database):
    with open(r"dbms/" + database + "/permission.json", "r") as file:
        file_json = json.load(file)

        if file_json["owner"] == user:
            return True
        return False