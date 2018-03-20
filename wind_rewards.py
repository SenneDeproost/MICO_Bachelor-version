import tinydb as db

def createValRules(CG):
    edges = CG.db.edges()
    result = []

    for edge in edges:
        edge_values = []
        f = open("changeYaw.actions")
        actions = f.read().splitlines()
        for action in actions:
            calculation = 5
            edge_values.append(calculation)
        result.append(edge_values)

    return result