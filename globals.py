import json
commands = json.load(open("commands.json"))
global_vars = json.load(open("variables.json"))

def printStat(message):
    print(message)

def raiseError(function, message):
    print("*" * len(message))
    print("[ERROR] --> " + function)
    print(message)
    print("*" * len(message))
    exit()
