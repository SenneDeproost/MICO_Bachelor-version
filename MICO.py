# *************************************************************************** #
#            Multi-Agent Infrastructure Configuration Optimizer (MICO)        #
#                               Senne Deproost                                #
#                            senne.deproost@vub.be                            #
# *************************************************************************** #

from sys import argv
import random as r
import numpy as np
from tinydb import TinyDB, Query
import globals as g
import infrastructure as i
import coordination_graph as cg
import banner as b
import WISDEM.FLORIS_SE.NREL5_calc as f

b.printBanner()

args = argv
argc = len(args)

extension = ".json"

wind = {"angle": 180, "speed": 8.1}

def MICO_wind(config, wind):
    g.printStat("Starting MICO_wind with " + config + " as configuration")
    g.printStat("   Wind blows " + str(wind["angle"]) + " degrees with a speed of " + str(wind["speed"]) + " m/s")

    infra = i.loadInfrastructureDB(config)

    nTurbines = len(infra)
    nActions = 60
    nEpisodes = 200

    CG = cg.createCG(infra, nActions, wind)

    g.printStat("Starting learning session: " + str(nEpisodes) + " episodes")

    for episode in xrange(1, 1 + nEpisodes):

        g.printStat("   Episode " + str(episode))

        # Find optimal joint action (OJA) using variable elimination

        OJA = cg.findOJA(CG, nActions)

        # Chose the OJA action with a chance of (1 - epsilon) or chose a random
        # action.

        jointAction = None

        if r.random() < (1 - g.epsilon):
            jointAction = OJA
            g.printStat("       Using OJA")
        else:
            jointAction = map(lambda x: r.randint(-30, 30), np.zeros(nTurbines))
            g.printStat("       Using random action")

        g.printStat("       Joint action: " + str(jointAction))

        # Validate jointAction in WISDEM and receive the power productions

        powerProductions = np.zeros([nTurbines, nTurbines])
        Q = Query()

        for edge in CG.edges():
            turbine1 = infra.search(Q.id == edge[0])[0]
            turbine2 = infra.search(Q.id == edge[1])[0]
            originalYaw1 = turbine1["yaw"]
            originalYaw2 = turbine2["yaw"]
            turbine1["yaw"] = originalYaw1 + jointAction[edge[0]]
            turbine2["yaw"] = originalYaw2 + jointAction[edge[1]]

            production = f.calcProduction(wind, [turbine1, turbine2])
            powerProductions[edge[0]][edge[1]] = production

            # Update productions
            productions = CG.edge[edge[0]][edge[1]]["productions"]
            productions[turbine1["yaw"]][turbine2["yaw"]] = production
            #print production

            # Update valRules
            discSum = cg.discountedSum(edge, [jointAction[edge[0]], jointAction[edge[1]]], OJA, CG)
            valRules = CG[edge[0]][edge[1]]['valRules']

            adjustedProduction = valRules[edge[0]][edge[1]] + discSum
            valRules[edge[0], edge[1]] = adjustedProduction



        g.printStat("       Total power production: " + str(powerProductions.sum()))

    g.printStat("Done!")

g.printStat("Done loading modules")

MICO_wind("testpark.json", wind)
