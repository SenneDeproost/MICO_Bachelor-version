import networkx as nx
from tinydb import TinyDB, Query

import wind_dependencies as dep


def createCG(database, parameters):
    cg = nx.Graph()
    entities = database.all()

    for entity in entities:
        cg.add_node(entity["id"])
        for other in entities:
            if dep.dependsOn(entity, other, parameters) and entity["id"] != other["id"]:
                cg.add_edge(entity["id"], other["id"])

    print nx.edges(cg)

    return cg



