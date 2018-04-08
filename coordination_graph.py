from tinydb import TinyDB, Query
import networkx as nx
import numpy as np
import globals as g
import wind_dependencies as dep
import wind_rewards as rw
import wind_joint as j


def createCG(database, nActions, *parameters):
    g.printStat("Creating coordination graph")
    cg = nx.DiGraph() # Directed graph
    entities = database.all()
    for entity in entities:
        g.printStat("   Adding node " + str(entity["id"]) + " to CG")
        cg.add_node(entity["id"], data=entity, qFunction=np.zeros([nActions]))
        for other in entities:
            if dep.dependsOn(entity, other, parameters) and entity["id"] != other["id"]:
                cg.add_edge(entity["id"], other["id"], valRules=np.zeros([nActions, nActions]))
    g.printStat("   Dependencies found: " + str(cg.edges()))
    return cg

# A context is an array of objects with a agent and an action field
def changeValueRule(agents, actions, newVal, cg):
    cg[agents[0]][agents[1]]['valRules'][actions[0]][actions[1]] = newVal


# Needs optimalization
def findInvolvement(agents, cg):
    edges = cg.edges()
    result = []
    for edge in edges:
        for agent in agents:
            if agent in edge:
                result.append(edge)
    return result


def localQVal(agent, action, cg):
    involvement = findInvolvement(agent , cg) # List of edges (a, b)
    valRules = []
    result = 0

    for edge in involvement:
        valRules = g[edge[0]][edge[1]]['valRules']
        result =+ np.sum(valRules[:, action])
        result =+ np.sum(valRules[action, :])

    return result / len(involvement)





        #if action in rule["actions"]:
        #    result =+ rule["payoff"] / len(rule["agents"])

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
