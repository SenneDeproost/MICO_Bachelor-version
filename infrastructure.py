from tinydb import *
from matplotlib import pyplot as plt
import globals as g

def loadInfrastructure(config):
    g.printStat("Loaded " + config + " into infrastructure database.")

    db = TinyDB("config")

    infra = ["number", "dimensions", db]

    return infra

def mapInfrastructre(infra):
    return "haha"
