from tinydb import TinyDB, Query
import networkx as nx
import numpy as np
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


# Find the OJA (Optimal Joint Action) in the CG by using variable elimination
def findOJA(valRules, CG):
    graph = CG.copy()
    variables = graph.nodes()
    counter = len(variables)

    while counter > 1:
        neighbors = graph.neighbors()












# A context is an array of objects with a agent and an action field
def insertValueRule(context, payoff, db):
    agents = context["agents"]
    actions = context["actions"]

    db.insert({
    "agents":    agents,
    "actions":   actions,
    "payoff":    payoff
    })


def findInvolvement(agentList, valRules):
    Q = Query()
    return valRules.search(Q.agents.any([agentList]))


def calculateLocalQ(agent, action, valRules):
    involvement = findInvolvement(agent , valRules)
    result = 0

    for rule in involvement:
        if action in rule["actions"]:
            result =+ rule["payoff"] / len(rule["agents"])

    return result


 #def updateValueRule(agent, action, valRule, valRules):
    # agents = valRule["agents"]
    # actions = valRule["actions"]





    # reward =


    # valRule.payoff = newPayoff




    # valRules.write_back(updatedRule)









#def findInvolvement(agent, valueRules)



#def calculateLocalQ(agent, action, valueRules):
#    involvement = findInvolvement(agent, action)





#def updateValueRule(valueRule, reward):
#    contect = valueRule["context"]
#    payoff = valueRule["payoff"]
#    return payoff + g.learningRate


#def findOJA(CG, value_rules):
#    return 5
