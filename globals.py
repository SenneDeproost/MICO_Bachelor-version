import json
import time
#commands = json.load(open("commands.json"))
#global_vars = json.load(open("variables.json"))

gamma = 0
learningRate = 0.95
discount = 0.99
epsilon = 0.1

step = 5
nActions = 7 # Don't forget about 0

logName = str(time.time()) + ".log"

def actionIndex(action):
    normalized = action / step
    return normalized + ((nActions - 1) / 2)

def indexAction(index):
    normalized = index*step
    return normalized - step * ((nActions - 1) / 2)


def printStat(message):
    print("[*] " + message)
    #file = open("logs/" + logName, 'a')
    #file.write("[*] " + message + "\n")
    #file.close()


def raiseError(function, message):
    print("*" * len(message))
    print("[ERROR] --> " + function)
    print(message)
    print("*" * len(message))
    exit()

def debug(msg):
        print "/////DEBUG//////"
        print msg
        print "////////////////"
