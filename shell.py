from globals import *

SHELL_LOOP = True
PROMPT = '>'

def printBanner():
    print("------------------------------------")
    print("-               MICO               -")
    print("-           VERSION  " + str(VERSION_NUMBER) + "           -")
    print("------------------------------------")
    print("")

def printHelp():
    printBanner()
    print("prompt, -p                  Start in prompt mode.")
    print("help, -h                    Open program help.")
    print("run, -r                     Run program with file.")

def toArray(string):
    return string.split(" ")

def runShell():
    count = 0
    while SHELL_LOOP:
        count += 1
        readShell = raw_input(str(count) + PROMPT)
        shellInput = toArray(readShell)
        evalShell(shellInput)

def evalShell(input):
    if input[0] in ["exit"]:
        exit()
    elif input[0] in ["loadconfig"]:
        print 'dummy'
    elif input[0] in ["optimize"]:
        print 'dummy'
    else:
        print("ERROR: ")
        print(input)
        print("IS NOT A VALID COMMAND.")
