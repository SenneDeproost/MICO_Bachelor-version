import json
import time
#commands = json.load(open("commands.json"))
#global_vars = json.load(open("variables.json"))

gamma = 0.9
learningRate = 0.9
discount = 0.9
epsilon = 0.5

logName = str(time.time()) + ".log"



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
