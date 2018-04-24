from tinydb import TinyDB, Query
#from matplotlib import pyplot as plt
import globals as g
import json as j
import os.path


def loadInfrastructureDB(config):
    g.printStat("Loading infrastructure")
    extension = ".json"
    suffix = "_infra_TinyDB"
    if not validFormat(config, extension):
        g.raiseError("loadInfrastructure",
                     "File " + config + " is not in a valid format")
    else:
        name = config[:-len(extension)]
        # TinyDB JSON is given
        if name.endswith(suffix):
            return TinyDB(config)
        # Ordinary JSON is given, but TinyDB equivalent exists
        #elif os.path.exists(db_name + extension):
         #   return TinyDB(db_name + extension)
        # No equivalent TinyDB exists
        else:
            db = convertJsonToDB(config)
            return db


def convertJsonToDB(file):
    g.printStat(file + " needs conversion")
    extension = ".json"
    if validFormat(file, extension):
        data = j.load(open(file))
        ext_len = len(extension)
        db_name = file[:-ext_len] + "_infra_TinyDB"
        db = TinyDB(db_name + extension)
        db.purge()
        g.printStat("   Old database purged")
        counter = 1
        for obj in data:
            obj["id"] = counter
            counter += 1
            db.insert(obj)
        g.printStat("   File converted to database")
        return db
    else:
        g.raiseError("convertJsonToDB",
                     "File " + file + " is not in a valid format")
        return False


def validFormat(file, extension):
    return file.endswith(extension)
