from tinydb import TinyDB, Query
from matplotlib import pyplot as plt
import globals as g
import json as j
import os.path

def loadInfrastructure(config):
    extension = ".json"
    if os.path.isfile(config) and "_TinyDB" in config:
        db_name = file[:-5] + "_TinyDB"
        db = TinyDB(db_name + extension)
        g.printStat("Loaded " + config + " into infrastructure database.")
        return db
    else:
        db = convertJsonToDB(config)
        if db:
            g.printStat("Loaded " + config + " into infrastructure database.")
            return db
        else: g.printStat("ERROR: " + file + "IS NOT A VALID EXTENSION TO CONVERT TO DATABASE.")



def convertJsonToDB(file):
    extension = ".json"
    if validFormat(file, extension):
        data = j.load(open(file))
        db_name = file[:-5] + "_TinyDB"
        db = TinyDB(db_name + extension)
        for obj in data:
            db.insert(obj)
        return db
    else:
        g.printStat("ERROR: " + file + "IS NOT A VALID EXTENSION TO CONVERT TO DATABASE.")
        return False



def validFormat(file, extension):
    return extension in file
