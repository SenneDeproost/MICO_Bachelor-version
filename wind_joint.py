import networkx as nx

def findOJA(CG, vr, bins, sins):
    edges = CG.edges()
    nodes = CG.nodes()
    result = []



    #print createLabeledRewards(CG, vr)[0]
#    for node in nodes:
        # Indxs are the indexes in the list edges where the node is involved.
#        indxs = findEdgeIndexes(edges, node)
#        print node
#        for indx in indxs:
#            print edges[indx]
    #        print vr[indx]



    return result


def createLabeledRewards(CG, vr):
    edges = CG.edges()
    nodes = CG.nodes()
    result = []

    for node in nodes:
        edge_res = []
        indxs = findEdgeIndexes(edges, node)
        for indx in indxs:
            edge_res.append((edges[indx], vr[indx]))
        result.append((node, edge_res))

    return result


def findJointRewards(CG, vr, a, b):
    edges = CG.edges()
    edge_indx = False
    if (a, b) in edges:
        edge_indx = edges.index((a, b))
    elif (b, a) in edges:
        edge_indx = edges.index((b, a))
    result = vr[edge_indx]
    return result

def getReward(CG, vr, a, b, action_a, action_b):
    matrix = findJointActions(CG, vr, a, b)
    return matrix[action_a][action_b]

def findEdgeIndexes(edges, node):
    indxs = []
    counter = 0
    for edge in edges:
        if node in edge:
            indxs.append(counter)
        counter += 1
    return indxs
