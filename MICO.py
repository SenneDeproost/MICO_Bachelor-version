# ***************************************************************************** #
#            Multi-Agent Infrastructure Configuration Optimizer (MICO)          #
#                               Senne Deproost                                  #
#                            senne.deproost@vub.be                              #
# ***************************************************************************** #

import sys
import globals as g
import infrastructure as i
import coordination_graph as cg
from shell import *


#import "infrastructure.py"
#import "dependency_graph.py"

args = sys.argv
argc = len(args)

def MICO_wind(configuration, wind):

    infra = i.loadInfrastructure(configuration)
#    CG = cg.createCG(infra, wind)

    print "done"

MICO_wind("testpark_config.json", 50)
