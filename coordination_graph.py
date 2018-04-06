import networkx as nx
from tinydb import TinyDB, Query
import globals as g
import wind_dependencies as dep
import wind_rewards as rw
import wind_joint as j


def createCG(database, *parameters):
    g.printStat("Creating coordination graph")
    cg = nx.DiGraph()
    entities = database.all()
    for entity in entities:
        g.printStat("   Adding node " + str(entity["id"]) + " to CG")
        cg.add_node(entity["id"])
        for other in entities:
            if dep.dependsOn(entity, other, parameters) and entity["id"] != other["id"]:
                cg.add_edge(entity["id"], other["id"])
    g.printStat("   Dependencies found: " + str(cg.edges()))
    return cg


def createValueRulesDB(config):
    print config
    g.printStat("Creating value rules database")
    extension = ".json"
    suffix = "_valRules_TinyDB"
    if not validFormat(config, extension):
        g.raiseError("loadValueRules",
                     "File " + config + " is not in a valid format")
    else:
        return TinyDB(config[:-len(extension)] + suffix + extension)


def validFormat(file, extension):
    return file.endswith(extension)


# A context is an array of objects with a agent and an action field
def insertValueRule(context, payoff, db):
    agents = context["agents"]
    actions = context["actions"]

    db.insert({
    "agents":    agents,
    "actions":   actions,
    "payoff":    payoff
    })












#def findInvolvement(agent, valueRules)



#def calculateLocalQ(agent, action, valueRules):
#    involvement = findInvolvement(agent, action)





#def updateValueRule(valueRule, reward):
#    contect = valueRule["context"]
#    payoff = valueRule["payoff"]
#    return payoff + g.learningRate


#def findOJA(CG, value_rules):
#    return 5
