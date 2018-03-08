from tinydb import TinyDB, Query
from matplotlib import pyplot as plt
import globals as g
import json as j
import os.path


def loadInfrastructure(config):
    extension = ".json"
    suffix = "_TinyDB"
    if not validFormat(config, extension):
        g.raiseError("loadInfrastructure", "File is not in a valid format.")
    else:
        db_name = config[:-5] + suffix
        name = config.strip(extension)
        # TinyDB JSON is given
        if name.endswith(suffix):
            return TinyDB(config)
        # Ordinary JSON is given, but TinyDB equivalent exists
        elif os.path.exists(db_name + extension):
            return TinyDB(db_name + extension)
        # No equivalent TinyDB exists
        else:
            db = convertJsonToDB(config)
            return db


def convertJsonToDB(file):
    extension = ".json"
    if validFormat(file, extension):
        data = j.load(open(file))
        ext_len = len(extension)
        db_name = file[:-ext_len] + "_TinyDB"
        db = TinyDB(db_name + extension)
        counter = 1
        for obj in data:
            obj["id"] = counter
            counter += 1
            db.insert(obj)
        return db
    else:
        g.printStat("ERROR: " + file + "IS NOT A VALID EXTENSION TO CONVERT TO DATABASE.")
        return False


def validFormat(file, extension):
    return file.endswith(extension)
