import json

def loadlocks(database):
    locks = {}
    with open(database+"/locks.json") as file:
        lockfile = json.load(file)

        for lock in lockfile:
            locks[lock["table"]] = lock["type"]

        return locks

def typeoflock(database,table):
    locks = loadlocks(database)

    if not table in locks.keys():
        return None
    return locks[table]

def locktable(database,table,lock):
    with open(database + "/locks.json") as file:
        lockfile = list(json.load(file))
        file = open(database+'/locks.json','w')

        for lock in lockfile:
            if lock["table"]==table and lock["type"]!="X":
                lock["type"] = lock
                json.dump(lockfile,file)
                return

        lockfile.append({"table":table,"type":lock})
        json.dump(lockfile,file)

def unlocktable(database,table):
    with open(database + "/locks.json") as file:
        lockfile = list(json.load(file))

        newlock = []
        for lock in lockfile:
            if lock["table"]!=table:
                newlock.append(lock)

        file = open(database+'/locks.json','w')
        json.dump(newlock,file)
