import tinydb as db

def createValRules(CG):
    edges = CG.db.edges()
    result = []

    for edge in edges:
        a = edge[0]
        b = edge[1]
        edge_values = []
        f = open("changeYaw.actions")
        actions = f.read().splitlines()
        for action in actions:
            first_paren = action.find('(')
            last_paren = action.find(')')
            action_name = action[:first_paren]
            parameters = action[first_paren + 1:last_paren]
            calculation = 5
            edge_values.append(calculation)
        result.append(edge_values)

    return result

def changeYaw(turbine, new_yaw):
    turbine["yaw"] = new_yaw
