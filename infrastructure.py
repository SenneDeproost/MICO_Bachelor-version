import tinydb

db = TinyDB("testpark_config.py")

def loadInfraConfig(path):
    db = TinyDB(path)
    return db
