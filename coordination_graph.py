import networkx as nx

import wind_dependencies as dep
import wind_rewards as rw


def createCG(database, *parameters):
    cg = nx.Graph()
    entities = database.all()

    for entity in entities:
        cg.add_node(entity["id"])
        for other in entities:
            if dep.dependsOn(entity, other, parameters) and entity["id"] != other["id"]:
                cg.add_edge(entity["id"], other["id"])

    return cg


def createValRules(CG):
    return rw.createValRules(CG)


def computeJointAction(CG):
    nodes = "nodes"
    return 5
