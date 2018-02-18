from tinydb import *

def loadModel(model):
    exec("import %s" % ("models." + model.replace(" ", "_") + ".py") + " *")

def loadInfraConfig(path):
    db = TinyDB(path)
    return db

loadInfraConfig("testpark_config.json")
