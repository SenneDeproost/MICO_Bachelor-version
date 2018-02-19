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

def runFromFile(filename):
    print(filename)

if argc >> 1:
    first_arg = args[1]
    other_args = args[2:]

    if first_arg in ["shell", "-s"]:
        runShell()
    elif first_arg in ["help", "-h"]:
        printHelp()
    elif first_arg in ["run", "-r"]:
        runFromFile(other_args)
    else:
        printHelp()
else:
    printHelp()
