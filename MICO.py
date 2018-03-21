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

wind = {"angle": 180, "speed": 8.1}

def MICO_wind(config, wind):
    g.printStat("Starting MICO_wind with " + config + " as configuration")
    g.printStat("   Wind blows " + str(wind["angle"]) + " degrees with a speed of " + str(wind["speed"]) + " m/s")
    infra = i.loadInfrastructure(config)
    CG = cg.createCG(infra, wind)

    g.printStat("Done!")

g.printStat("Done loading modules")
MICO_wind("testpark.json", wind)
