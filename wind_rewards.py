import tinydb as db
import WISDEM.FLORIS_SE.NREL5_binCalc as bc
import globals as g

def createValRules(CG, infrastructure, parameters):
    wind = parameters[0]
    edges = CG.edges()
    result = []

    for edge in edges:
        g.printStat("   Creating value rules for " + str(edge))
        a = edge[0]
        b = edge[1]
        edge_values = []
        f = open("changeYaw.actions")
        actions = f.read().splitlines()
        q = db.Query()
        for action in actions:
            productions_a = []
            turbine_a = infrastructure.search(q.id == a)[0]
            act_a = splitActPars(action)
            turbine_a["yaw"] = int(act_a["parameters"])
            g.printStat("       Turbine " + str(a) + ": " + str(action))
            for action in actions:
                turbine_b = infrastructure.search(q.id == b)[0]
                act_b = splitActPars(action)
                turbine_b["yaw"] = int(act_b["parameters"])
                g.printStat("         Turbine " + str(b) + ": " + str(action))
                calculation = bc.calcProduction(turbine_a, turbine_b, wind)
                productions_a.append(calculation)
            edge_values.append(productions_a)
        result.append(edge_values)

    return result

def splitActPars(string):
    first_paren = string.find('(')
    last_paren = string.find(')')
    action_name = string[:first_paren]
    parameters = string[first_paren + 1:last_paren]
    return {"action": action_name, "parameters": parameters}



def changeYaw(turbine, new_yaw):
    turbine["yaw"] = new_yaw
