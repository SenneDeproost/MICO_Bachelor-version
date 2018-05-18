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
import log as l
import WISDEM.FLORIS_SE.NREL5_calc as f

b.printBanner()

args = argv
argc = len(args)

extension = ".json"

wind = {"angle": 180, "speed": 8.1}

def MICO_wind(config, wind):
    g.printStat("Starting MICO_wind with " + config + " as configuration")
    g.printStat("   Wind blows " + str(wind["angle"]) + " degrees with a speed of " + str(wind["speed"]) + " m/s")

    l.createCSV()

    totalMax = {'production': 0, 'action': None, "OJA": 0}

    infra = i.loadInfrastructureDB(config)

    nTurbines = len(infra)
    nEpisodes = 10000

    CG = cg.createCG(infra, g.nActions, wind)

    g.printStat("Starting learning session: " + str(nEpisodes) + " episodes")

#    CG[1][2]['valRules'][1][1] = 500
#    CG[2][3]['valRules'][2][2] = 500000


    for episode in xrange(1, 1 + nEpisodes):

        g.printStat("   Episode " + str(episode))

        # Find optimal joint action (OJA) using variable elimination

    #    OJA = map(lambda x: g.indexAction(x) ,cg.findOJA(CG, g.nActions))

        OJA = cg.findOJA(CG, g.nActions)

        # Chose the OJA action with a chance of (1 - epsilon) or chose a random
        # action.

        jointAction = None

        if r.random() < (1 - g.epsilon):
            jointAction = OJA
            g.printStat("       Using OJA")
        else:
            jointAction = map(lambda x: r.randint(0, g.nActions - 1), np.zeros(nTurbines))
        # //    jointAction = map(lambda x: x + r.randint(-2, 2), OJA)
        #    jointAction = np.zeros(nTurbines)
        #    counter = 0
        #    for action in jointAction:
        #        exploringStep = 1
        #        rand = r.randint(-exploringStep, exploringStep)
        #        print rand
        #        if OJA[counter] + rand < 0:
        #            jointAction[counter] = OJA[counter] + abs(rand)
        #        elif OJA[counter] + rand > (g.nActions - 1):
        #            jointAction[counter] = OJA[counter] - abs(rand)
        #        else:
        #            jointAction[counter] = OJA[counter] + rand
        #        counter += 1
        #    jointAction = map(lambda x: int(x), jointAction)


            g.printStat("       Using random action")

        g.printStat("       Joint action: " + str(map(lambda x: g.indexAction(x), jointAction)))

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
            turbine['yaw'] = turbine['yaw'] + g.indexAction(jointAction[turbine['id'] - 1])

        powerProductions = f.calcProduction(wind, turbines)
        #powerProductions = np.array([500 + np.random.normal(0, 0.1), 500 + np.random.normal(0, 0.1), 500 + np.random.normal(0, 0.1)])

        total = np.sum(powerProductions)
        if total > totalMax['production']:
            totalMax['production'] = total
            totalMax['action'] = jointAction
            totalMax['OJA'] = OJA


        for edge in CG.edges():
            From = edge[0]
            To = edge[1]
            turbine1 = infra.search(Q.id == From)[0]
            turbine2 = infra.search(Q.id == To)[0]
            actionTurbine1 = jointAction[turbine1['id'] - 1]
            actionTurbine2 = jointAction[turbine2['id'] - 1]
            CG[From][To]['productions'][actionTurbine1][actionTurbine2] = powerProductions[turbine1['id'] - 1] + powerProductions[turbine2['id'] - 1]

            # Update valRules
            discSum = cg.discountedSum(edge, [jointAction[From - 1], jointAction[To - 1]], powerProductions, OJA, CG)
            valRules = CG[edge[0]][edge[1]]['valRules']

            normalizedFrom = jointAction[From - 1]
            normalizedTo = jointAction[To - 1]

            adjustedProduction = valRules[normalizedFrom][normalizedTo] + discSum
            valRules[normalizedFrom][normalizedTo] = adjustedProduction

            print powerProductions
            print valRules



            data = []
            data.append(episode)
            data.append(OJA)
            data.append(jointAction)
            data.append(powerProductions)

        l.appendCSV([[data]])

        g.printStat("       Total power production: " + str(powerProductions.sum()))

        print totalMax
        print "OJA: " + str(OJA)

    g.printStat("Done!")

g.printStat("Done loading modules")

MICO_wind("three_park.json", wind)
