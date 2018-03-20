import networkx as nx
import globals as g
import wind_dependencies as dep
import wind_rewards as rw


def createCG(database, *parameters):
    g.printStat("Creating coordination graph.")
    cg = nx.Graph()
    entities = database.all()
    for entity in entities:
        g.printStat("Processing node " + str(entity["id"]))
        cg.add_node(entity["id"])
        for other in entities:
            if dep.dependsOn(entity, other, parameters) and entity["id"] != other["id"]:
                cg.add_edge(entity["id"], other["id"])
    g.printStat("Dependencies found: " + str(cg.edges()))
    return cg


def createValRules(CG):
    return rw.createValRules(CG)


def computeJointAction(CG):
    nodes = "nodes"
    return 5
