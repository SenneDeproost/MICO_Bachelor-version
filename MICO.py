# *************************************************************************** #
#            Multi-Agent Infrastructure Configuration Optimizer (MICO)        #
#                               Senne Deproost                                #
#                            senne.deproost@vub.be                            #
# *************************************************************************** #

import sys
import globals as g
import infrastructure as i
import coordination_graph as cg
#import q_learning as q

args = sys.argv
argc = len(args)

wind = {"angle": 5}

def MICO_wind(config, wind):
    g.printStat("Starting MICO_wind with " + config + " as configuration.")
    infra = i.loadInfrastructure(config)
    CG = cg.createCG(infra, wind)
    #rewards = q.createRewardTable(CG)

    print CG.edges()

    g.printStat("Done!")


MICO_wind("testpark_config.json", wind)
