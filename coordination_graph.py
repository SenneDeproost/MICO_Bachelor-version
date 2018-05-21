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
    result = 0

    for edge in involvement:
        valRules = cg[edge[0]][edge[1]]['valRules'] #!!!!
        result += np.sum(valRules[action]) / 2
        #result += np.sum(valRules[:, g.actionIndex(action)]) / len(valRules)
        #result += np.sum(valRules[g.actionIndex(action), :]) / len(valRules)
    return result

def qVal(agent, action, cg):

    ins = cg.in_edges(agent)
    outs = cg.out_edges(agent)

    result = 0

    for IN in ins:
        valRules = cg[IN[0]][agent]['valRules']
        result += sum(valRules[:, action]) / 2

    for OUT in outs:
        valRules = cg[agent][OUT[1]]['valRules']
        result += sum(valRules[action, :]) / 2

    return result


# Discounted sum for the involvement of two agents
def discountedSum(edge, actions, rewards, oja, cg):
    agent1 = edge[0]
    agent2 = edge[1]
    action1 = actions[0]
    action2 = actions[1]

    productions = cg[agent1][agent2]['productions']

    production1 = rewards[agent1 - 1]
    production2 = rewards[agent2 - 1]

    print max(productions[action1])

    production = productions[action1]
    valRules = cg[agent1][agent2]['valRules']

#    production1 = productions[:, 0][action1]
#    production2 = productions[0, :][action2]

    optiQ1 = qVal(agent1, int(np.argmax(productions[action1])), cg)
    optiQ2 = qVal(agent2, int(np.argmax(productions[action1])), cg)

    localQ1 = qVal(agent1, action1, cg)
    localQ2 = qVal(agent2, action2, cg)

    print""
    print "QVAL"
    print "production: " + str(production1)
    print "optiQ: " + str(optiQ1)
    print "localQ: " + str(localQ1)
    print "div of Q1s: " + str(g.gamma*optiQ1 - localQ1)
    print "div of Q2s: " + str(g.gamma*optiQ2 - localQ2)

    updatedLocalQ1 = production1 + g.gamma*optiQ1 - localQ1
    updatedLocalQ2 = production2 + g.gamma*optiQ2 - localQ2

    # Assign new found Q's
    #cg.node[agent1]['qFunction'][action1][action2] = updatedLocalQ1
    #cg.node[agent2]['qFunction'][action2][action1] = updatedLocalQ2

    #summ = updatedLocalQ1 + updatedLocalQ2
    res = g.discount*(updatedLocalQ1 + updatedLocalQ2)
    res2 = g.discount*production1

    return res


def argmaxMat(matrix):
    rowmax = []
    for row in matrix:
        rowmax.append(np.argmax(row))
	row = max(rowmax)
	collom = np.argmax(rowmax)
    return (collom, row)

# Find the Optimal Joint Action (at the moment for 3 node involvment max)
def findOJA2(cg, nActions):
    graph = cg.copy()
    actions = range(0, nActions)
    counter = 1
    local = [np.zeros([nActions])]


    while counter < len(graph):
        outs = list(graph.out_edges(counter))
        ins = list(graph.in_edges(counter))
    #    ins2 = list(graph.in_edges(counter - 1)) #!!!

        hasInfluenced = None
        hasInfluencer = None
        hasInfluencer2 = None

        if len(outs) > 0:
            hasInfluenced = outs[0][1]

        if len(ins) > 0:
            hasInfluencer = ins[0][0]

    #    if len(ins) > 0:
    #        hasInfluencer2 = ins2[0][0]

        optimalRules = []
        valRules = graph[counter][hasInfluenced]['valRules']

        # Add previous founded rules
        for action in actions:
            valRules[action] = valRules[action] + local[-1][action]

        # Find maxes
        for ownAction in valRules:
            optimalRules.append(np.max(ownAction))
    #    graph[hasInfluencer2][hasInfluencer]['valRules'] = optimalRules

        local.append(optimalRules)
        counter += 1


#///////////////////////////////////////////////////////////////////////////////


#    g.debug(graph[1][2]['valRules'])
#    g.debug(graph[2][3]['valRules'])

    # When all but one of the variables is eliminated, the optmal action of
    # of the only variable left is calculated with max(internalMaxFun(action)).
    # To calculate the optimal actions of the other variables, the algoritme
    # traverses the graph backwards.

    #local[-2][1] = 500000000
    #local[-2][0] = 0
    #local[-3][3] = 55

    firstVals = local[-1]
    optimalActions = []
    optimalActions.append(np.argmax(firstVals))

    counter -= 1

    # !!!!!!!!! Moet anders!
    #g.debug(graph.node[1]['qFunction'])
    #g.debug(graph.node[2]['qFunction'])
    #g.debug(graph.node[3]['qFunction'])

    while counter > 0:
        val = graph[counter][counter + 1]['valRules']
        prevAction = optimalActions[-1]
        valPrevAction = val[:, prevAction]
        maxVal = np.argmax(valPrevAction)
        optimalActions.insert(0, maxVal)


        #prevAction = optimalActions[counter - 1]
        #actions = q[:, prevAction]
        #optimalAction = np.argmax(actions)
        #optimalActions.append(optimalAction)
        #optimalActions.append(np.array(graph.node[counter]['qFunction']).argmax())
        counter -= 1

    return optimalActions



def findOJA(cg, nActions):
    local = [np.zeros(nActions)]

    mats = [cg[1][2]['valRules']]
    mats.append(cg[2][3]['valRules'])

    for mat in mats:
	       res = []
	       mat = np.array(mat) + local[-1]
	       for row in mat:
		      res.append(np.max(row))
	       local.append(res)

    result = []


    result.append(np.argmax(local[-1]))
    for mat in reversed(mats):
	       result.append(np.argmax(mat[:, result[-1]]))

    #result = list(reversed(result))
    print "HAHAHAHAHAHA"
    print ""
    print map(lambda x: g.indexAction(x), result)
    print ""
    print "HAHAHAHAHAHA"

    return result

def findOJAProd(cg, nActions):
    local = [np.zeros(nActions)]

    mats = [cg[1][2]['productions']]
    mats.append(cg[2][3]['productions'])

    for mat in mats:
	       res = []
	       mat = np.array(mat) + local[-1]
	       for row in mat:
		      res.append(np.max(row))
	       local.append(res)

    result = []


    result.append(np.argmax(local[-1]))
    for mat in reversed(mats):
	       result.append(np.argmax(mat[:, result[-1]]))

    result = list(reversed(result))

    return result
