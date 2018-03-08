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


def MICO_wind(config, wind):
    infra = i.loadInfrastructure(config)
    CG = cg.createCG(infra, wind)
    #rewards = q.createRewardTable(CG)

    g.printStat("Done!")


MICO_wind("testpark_config.json", 50)
