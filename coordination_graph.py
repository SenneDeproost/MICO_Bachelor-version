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
        cg.add_node(entity["id"], qFunction=5555)
        #cg[entity["id"]]['qFunctiiiiiion'] = np.zeros([nActions, nActions])
        for other in entities:
            if dep.dependsOn(entity, other, parameters) and entity["id"] != other["id"]:
                cg.add_edge(entity["id"], other["id"],) # Row = cur
    nx.set_node_attributes(cg, 'qFunction', np.zeros([nActions, nActions]))
    nx.set_edge_attributes(cg, 'productions', np.zeros([nActions, nActions]))
    nx.set_edge_attributes(cg, 'valRules', np.zeros([nActions, nActions]))
    g.printStat("   Dependencies found: " + str(cg.edges()))
    return cg

# A context is an array of objects with a agent and an action field
def changeValueRule(agents, actions, newVal, cg):
    cg[agents[0]][agents[1]]['valRules'][actions[0]][actions[1]] = newVal


# Needs optimalization
def findInvolvement(agent, cg):
    edges = cg.edges()
    result = []
    for edge in edges:
        if agent in edge:
            result.append(edge)
    return result


def localQVal(agent, action, cg):
    involvement = findInvolvement(agent , cg) # List of edges (a, b)
    valRules = []
    result = 0

    for edge in involvement:
        valRules = cg[edge[0]][edge[1]]['valRules']
        result += np.sum(valRules[:, action])
        result += np.sum(valRules[action, :])

    return result / len(involvement)

# Discounted sum for the involvement of two agents
def discountedSum(edge, actions, oja, cg):
    agent1 = edge[0]
    agent2 = edge[1]
    action1 = actions[0]
    action2 = actions[1]
    productions = cg[agent1][agent2]['productions']

    production1 = productions[:, 0][action1]
    production2 = productions[0, :][action2]

    optiQ1 = localQVal(agent1, oja[agent1], cg)
    optiQ2 = localQVal(agent2, oja[agent2], cg)

    localQ1 = localQVal(agent1, action1, cg)
    localQ2 = localQVal(agent2, action2, cg)

    updatedLocalQ1 = production1 + g.gamma*optiQ1 - localQ1
    updatedLocalQ2 = production2 + g.gamma*optiQ2 - localQ2

    # Assign new found Q's
    cg.node[agent1]['qFunction'][action1][action2] = updatedLocalQ1
    cg.node[agent2]['qFunction'][action2][action1] = updatedLocalQ2

    summ = updatedLocalQ1 + updatedLocalQ2

    return g.discount*summ


# Find the Optimal Joint Action (at the moment for 3 node involvment max)
def findOJA(cg, nActions):
    graph = cg.copy()
    nx.set_node_attributes(graph, 'internalMaxFun', np.zeros([nActions]))
    actions = range(0, nActions)

    counter = len(graph)

    while counter > 1: # Process all nodes except one
        outs = cg.out_edges(counter)
        ins = cg.in_edges(counter)

        hasInfluenced = None
        hasInfluencer = None

        if len(outs) > 0:
            hasInfluenced = outs[0][1]

        if len(ins) > 0:
            hasInfluencer = ins[0][0]


        # Check if the variable has a influencer. If not, it is a Independent
        # Learner (IL).
        if not hasInfluencer:
            if hasInfluenced:
                graph.remove_edge(counter, hasInfluenced)
            #graph.remove_node(counter)

        # The multi-agent approach
        if hasInfluencer:
            influencerActions = graph.node[hasInfluencer]['qFunction']
            influencedActions = np.zeros([nActions, nActions])
            if hasInfluenced:
                influencedActions = graph.node[hasInfluencer]['qFunction']

            # For every action of the influenced en the influencer, the
            # internalMaxFun returns the maximum of the sum of the Q values from
            # the local Q function of the influenced variable and the Q function
            # of the eliminated one.
                for a1 in actions:
                    for a2 in actions:
                        result = max(np.add(influencedActions[a1],
                                            influencerActions[a2]))
                        graph.node[hasInfluenced]['internalMaxFun'][a1] = result


                # Eliminate the variable and it's edges
                graph.remove_edge(hasInfluencer, counter)
                graph.remove_edge(counter, hasInfluenced)
                #graph.remove_node(counter)

                                            # Decrease counter
        counter -= 1

    # When all but one of the variables is eliminated, the optmal action of
    # of the only variable left is calculated with max(internalMaxFun(action)).
    # To calculate the optimal actions of the other variables, the algoritme
    # traverses the graph backwards.
    counter = len(cg)
    optimalActions = []

    while counter > 0:
        optimalActions.append(np.array(graph.node[counter]['internalMaxFun']).argmax())
        counter -= 1
    return optimalActions
