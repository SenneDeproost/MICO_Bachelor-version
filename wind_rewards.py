import tinydb as db
import WISDEM.FLORIS_SE.NREL5_binCalc as bc
import globals as g

def createValRules(CG, infrastructure, parameters):
    wind = parameters[0]
    edges = CG.db.edges()
    result = []

    for edge in edges:
        g.printStat("   Creating value rules for " + str(edge))
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
            q = db.Query()
            turbine_a = infrastructure.search(q.id == a)
            turbine_b = infrastructure.search(q.id == b)
            calculation = bc.CalcProduction(turbine_a, turbine_b, wind)
            edge_values.append(calculation)
        result.append(edge_values)

    return result

def changeYaw(turbine, new_yaw):
    turbine["yaw"] = new_yaw
