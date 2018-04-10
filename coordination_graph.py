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
        cg.add_node(entity["id"],
                    data=entity,
                    qFunction=np.zeros([nActions, nActions]))
        for other in entities:
            if dep.dependsOn(entity, other, parameters)
            and entity["id"] != other["id"]:
                cg.add_edge(entity["id"], other["id"],
                            valRules=np.zeros([nActions, nActions])) # Row = cur
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


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def localQVal(agent, action,  cg):
    involvement = findInvolvement(agent , cg) # List of edges (a, b)
    valRules = []
    result = 0

    for edge in involvement:
        valRules = g[edge[0]][edge[1]]['valRules']
        result =+ np.sum(valRules[:, action])
        result =+ np.sum(valRules[action, :])

    return result / len(involvement)


# Find the Optimal Joint Action (at the moment for 3 node involvment)
def findOJA(cg):
    graph = cg.copy()
    counter = len(graph)

    while counter > 1:
        node = graph[counter]
        neighbors = neighbors(counter)
        neighborQFuncs = map(lambda x: graph[x]['qFunction'] , neighbors)

        influenced = graph[graph.out_edges(counter)[0][1]]
        influencer = graph[graph.in_edges(counter)[0][0]]

        influencedActions = range(0, len(influenced['qFunction']))
        influencerActions = range(0, len(influencer['qFunction']))

        nActions = len(influencedActions * influencerActions)

        internalMaxFun = np.zeros([len(influencedActions), len(influencerActions)])

        # For every action of the influenced en the influencer, the internalMaxFun
        # returns the maximum of the sum of the Q values from the local Q function
        # of the influenced variable and the Q function of the eliminated one.
        for a1 in influencedActions:
            for a2 in inflerAction:
                result = max(np.add((influencedActions[a1],
                                    (influencerActions[a2]))))
                internalMaxFun[inflcedAction][inflencerAction] = result

        # Eliminate the variable
        graph.add_edge(
        graph.in_edges(counter)[0][0],
        graph.outedges(counter)[0][1]
        )

        graph.remove_edge(graph.in_edges[0])
        graph.remove_edge(graph.out_edges[0])

        graph.remove_node(counter)

        counter -= 1

    # When all but one of the variables is eliminated, the optmal action of
    # of the only variable left is calculated with max(internalMaxFun(action)).
    # To calculate the optimal actions of the other variables, the algoritme
    # traverses the graph backwards.
    counter = len(graph)
    optimalActions = []

    for counter > 0:
        optimalActions.append(graph[counter]['internalMaxFun'])
        counter -= 1

    return optimalActions
