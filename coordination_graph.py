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
        cg.add_node(entity["id"], qFunction=np.zeros([nActions, nActions]))
        for other in entities:
            if dep.dependsOn(entity, other, parameters) and entity["id"] != other["id"]:
                cg.add_edge(entity["id"], other["id"], productions=np.zeros([nActions, nActions]), valRules=np.zeros([nActions, nActions])) # Row = cur
    #nx.set_node_attributes(cg, 'qFunction', np.zeros([nActions, nActions]))
    #nx.set_edge_attributes(cg, 'productions', np.zeros([nActions, nActions]))
    #nx.set_edge_attributes(cg, 'valRules', np.zeros([nActions, nActions]))
    g.printStat("   Dependencies found: " + str(cg.edges()))
    return cg

# A context is an array of objects with a agent and an action field
def changeValueRule(agents, actions, newVal, cg):
    cg[agents[0]][agents[1]]['valRules'][actions[0]][actions[1]] = newVal

# Needs optimalization
def findInvolvement(agent, cg):
    edges = []
    ins = cg.in_edges(agent)
    outs = cg.out_edges(agent)

    if len(ins) > 0:
        for edge in ins:
            edges.append(ins)
    if len(outs) > 0:
        for edge in outs:
            edges.append(outs)

    return edges[0] # temp solution


def localQVal(agent, action, cg):
    involvement = findInvolvement(agent , cg) # List of edges (a, b)
    valRules = []
    result = 0

    for edge in involvement:
        valRules = cg[edge[0]][edge[1]]['valRules'] #!!!!
        result += np.sum(valRules[:, g.actionIndex(action)])
        result += np.sum(valRules[g.actionIndex(action), :])

    return result / len(involvement)

# Discounted sum for the involvement of two agents
def discountedSum(edge, actions, oja, cg):
    agent1 = edge[0]
    agent2 = edge[1]
    action1 = g.actionIndex(actions[0])
    action2 = g.actionIndex(actions[1])

    productions = cg[agent1][agent2]['productions']

    production1 = productions[:, 0][action1]
    production2 = productions[0, :][action2]

    optiQ1 = localQVal(agent1, oja[agent1 - 1], cg)
    optiQ2 = localQVal(agent2, oja[agent2 - 1], cg)

    localQ1 = localQVal(agent1, action1, cg)
    localQ2 = localQVal(agent2, action2, cg)

    updatedLocalQ1 = production1 + g.gamma*optiQ1 - localQ1
    updatedLocalQ2 = production2 + g.gamma*optiQ2 - localQ2

    # Assign new found Q's
    cg.node[agent1]['qFunction'][action1][action2] = updatedLocalQ1
    cg.node[agent2]['qFunction'][action2][action1] = updatedLocalQ2

    summ = updatedLocalQ1 + updatedLocalQ2

    print "lel"
    print (summ, actions)
    print "lel"

    return g.discount*summ


def argmaxMat(matrix):
    rowmax = []
    for row in matrix:
        rowmax.append(np.argmax(row))
	row = max(rowmax)
	collom = np.argmax(rowmax)
    return (collom, row)

# Find the Optimal Joint Action (at the moment for 3 node involvment max)
def findOJA(cg, nActions):
    graph = cg.copy()
    actions = range(0, nActions)
    counter = len(graph)


    if counter == len(graph):
        outs = list(graph.out_edges(counter))
        ins = list(graph.in_edges(counter))
        ins2 = list(graph.in_edges(counter - 1)) #!!!

        hasInfluenced = None
        hasInfluencer = None
        hasInfluencer2 = None

        if len(outs) > 0:
            hasInfluenced = outs[0][1]

        if len(ins) > 0:
            hasInfluencer = ins[0][0]

        if len(ins) > 0:
            hasInfluencer2 = ins2[0][0]

        optimalRules = []
        valRules = np.transpose(graph[hasInfluencer][counter]['valRules'])
        g.debug(valRules)
        for ownAction in valRules:
            optimalRules.append(np.max(ownAction))
        graph[hasInfluencer2][hasInfluencer]['valRules'] = optimalRules

    counter -= 1

#///////////////////////////////////////////////////////////////////////////////

    while counter > 2: # Process all nodes except one
        outs = list(graph.out_edges(counter))
        ins = list(graph.in_edges(counter))
        ins2 = list(graph.in_edges(counter - 1))

        hasInfluenced = None
        hasInfluencer = None

        if len(outs) > 0:
            hasInfluenced = outs[0][1]

        if len(ins) > 0:
            hasInfluencer = ins[0][0]

        optimalRules = []
        print (hasInfluencer, counter)
        valRules = np.transpose(cg[hasInfluencer][counter]['valRules'])
        internalMax = graph[hasInfluencer][counter]['valRules']
        print valRules
        print internalMax
        for ownAction in valRules:
            print 5


        graph[hasInfluencer2][hasInfluencer]['valRules'] = optimalRules

        # Decrease counter
        counter -= 1

#///////////////////////////////////////////////////////////////////////////////

    g.debug(graph[1][2]['valRules'])
    g.debug(graph[2][3]['valRules'])



    # When all but one of the variables is eliminated, the optmal action of
    # of the only variable left is calculated with max(internalMaxFun(action)).
    # To calculate the optimal actions of the other variables, the algoritme
    # traverses the graph backwards.

    firstQ = graph.node[counter]['qFunction']
    counter = 1
    optimalActions = []
    optimalActions.append(argmaxMat(firstQ)[1])

    #counter += 1

    # !!!!!!!!! Moet anders!
    #g.debug(graph.node[1]['qFunction'])
    #g.debug(graph.node[2]['qFunction'])
    #g.debug(graph.node[3]['qFunction'])

    while counter < len(cg):
        q = graph.node[counter]['qFunction']
        prevAction = optimalActions[counter - 1]
        actions = q[:, prevAction]
        optimalAction = np.argmax(actions)
        optimalActions.append(optimalAction)
        #optimalActions.append(np.array(graph.node[counter]['qFunction']).argmax())
        counter += 1
    return optimalActions
