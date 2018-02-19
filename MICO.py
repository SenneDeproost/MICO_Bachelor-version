# ***************************************************************************** #
#            Multi-Agent Infrastructure Configuration Optimizer (MICO)          #
#                               Senne Deproost                                  #
#                            senne.deproost@vub.be                              #
# ***************************************************************************** #

import sys
import globals as g
from shell import *


#import "infrastructure.py"
#import "dependency_graph.py"

args = sys.argv
argc = len(args)

if argc >> 1:
    first_arg = args[1]
    other_args = args[2:]

    modeObjects = g.commands["modes"]
    idx = 0
    for object in modeObjects:
        if first_arg in str(modeObjects[idx]["flags"]):
            exec("%s" % (modeObjects[idx]["procedure"]))
        idx += 1

def runFromFile(filename):
    print(filename)
