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

    totalMax = {'production': 0, 'action': None}

    infra = i.loadInfrastructureDB(config)

    nTurbines = len(infra)
    nEpisodes = 200

    CG = cg.createCG(infra, g.nActions, wind)

    g.printStat("Starting learning session: " + str(nEpisodes) + " episodes")

    for episode in xrange(1, 1 + nEpisodes):

        g.printStat("   Episode " + str(episode))

        # Find optimal joint action (OJA) using variable elimination

        OJA = cg.findOJA(CG, g.nActions)

        # Chose the OJA action with a chance of (1 - epsilon) or chose a random
        # action.

        jointAction = None

        if r.random() < (1 - g.epsilon):
            jointAction = OJA
            g.printStat("       Using OJA")
        else:
            jointAction = map(lambda x: r.randint(-((g.nActions - 1) / 2), ((g.nActions - 1) / 2)) * g.step, np.zeros(nTurbines)) # Actions are plurality of 5
            g.printStat("       Using random action")

        g.printStat("       Joint action: " + str(jointAction))

        #test
    #    for edge in CG.edges():
    #        CG[edge[0]][edge[1]]['valRules'][1][0] = np.random.random() * 1000
    #        CG[edge[0]][edge[1]]['valRules'][1][5] = np.random.random() * 1000
    #        CG[edge[0]][edge[1]]['valRules'][4][6] = np.random.random() * 1000
    #        CG[edge[0]][edge[1]]['valRules'][6][6] = np.random.random() * 1000
            #valRules[edge[0]][edge[1]] = np.random.random()
    #        print edge
            #print valRules
    #        print "haha"

        # Validate jointAction in WISDEM and receive the power productions

        Q = Query()

        turbines = infra.all()

        for turbine in turbines:
            turbine['yaw'] = turbine['yaw'] + jointAction[turbine['id'] - 1]

        powerProductions = f.calcProduction(wind, turbines)

        total = np.sum(powerProductions)
        if total > totalMax['production']:
            totalMax['production'] = total
            totalMax['action'] = jointAction


        for edge in CG.edges():
            From = edge[0]
            To = edge[1]
            turbine1 = infra.search(Q.id == From)[0]
            turbine2 = infra.search(Q.id == To)[0]
            actionTurbine1 = jointAction[turbine1['id']]
            actionTurbine2 = jointAction[turbine1['id']]
            CG[From][To]['productions'][g.actionIndex(actionTurbine1)][g.actionIndex(actionTurbine2)] = powerProductions[turbine1['id'] - 1] + powerProductions[turbine2['id'] - 1]

            # Update valRules
            discSum = cg.discountedSum(edge, [jointAction[0], jointAction[0]], OJA, CG)
            valRules = CG[edge[0]][edge[1]]['valRules']

            normalizedFrom = g.actionIndex(jointAction[From - 1])
            normalizedTo = g.actionIndex(jointAction[To - 1])

            adjustedProduction = valRules[normalizedFrom][normalizedTo] + discSum
            valRules[normalizedFrom][normalizedTo] = adjustedProduction


        g.printStat("       Total power production: " + str(powerProductions.sum()))

    print totalMax
    g.printStat("Done!")

g.printStat("Done loading modules")

MICO_wind("three_park.json", wind)
