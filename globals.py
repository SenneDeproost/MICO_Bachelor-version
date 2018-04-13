import json
#commands = json.load(open("commands.json"))
#global_vars = json.load(open("variables.json"))

gamma = 0.9
learningRate = 0.9
discount = 0.9
epsilon = 0.9

def printStat(message):
    print("[*] " + message)


def raiseError(function, message):
    print("*" * len(message))
    print("[ERROR] --> " + function)
    print(message)
    print("*" * len(message))
    exit()
