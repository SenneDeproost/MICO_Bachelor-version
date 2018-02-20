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

    modes = g.commands["modes"]
    idx = 0
    for obj in modes:
        flags = modes[idx]["flags"]
        if first_arg in flags:
            exec("%s" % (modes[idx]["procedure"]))
        idx += 1
else:
    printHelp()

def runFromFile(filename):
    print(filename)
