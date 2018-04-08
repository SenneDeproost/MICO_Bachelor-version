# *************************************************************************** #
#            Multi-Agent Infrastructure Configuration Optimizer (MICO)        #
#                               Senne Deproost                                #
#                            senne.deproost@vub.be                            #
# *************************************************************************** #

from sys import argv
import globals as g
import infrastructure as i
import coordination_graph as cg
import banner as b

b.printBanner()

args = argv
argc = len(args)

epsilon = 0.1
learningRate = 0.9
discount = 0.9

extension = ".json"

wind = {"angle": 180, "speed": 8.1}

def MICO_wind(config, wind):
    g.printStat("Starting MICO_wind with " + config + " as configuration")
    g.printStat("   Wind blows " + str(wind["angle"]) + " degrees with a speed of " + str(wind["speed"]) + " m/s")

    infra = i.loadInfrastructureDB(config)

    nTurbines = len(infra)
    nActions = range(360*nTurbines)
    nEpisodes = 10

    CG = cg.createCG(infra, nActions, wind)


    for episode in xrange(nEpisodes):
        print episode

        # Find optimal joint action (OJA) using variable elimination

        #cg.findOJA(CG, valueRules)

        # Chose an action ALPHA with epsilon greedy (or a random action)

        # Validate ALPHA in WISDEM and receive the powerproductions

        # Update the value rules


    g.printStat("Done!")

g.printStat("Done loading modules")

MICO_wind("sinpark.json", wind)
