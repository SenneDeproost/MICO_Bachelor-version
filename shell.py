import globals as g

SHELL_LOOP = False
PROMPT = '>'

def printBanner():
    print("------------------------------------")
    print("-               MICO               -")
    print("-           VERSION  " + str(g.VERSION_NUMBER) + "           -")
    print("------------------------------------")
    print("")

def printHelp():
    if SHELL_LOOP:
        printShellHelp()
    else:
        printModeHelp()

def printModeHelp():
    printBanner()
    modes = g.commands["modes"]

    for mode in modes:
        flags = mode["flags"]
        print("%s                   %s" % (flags, mode["instruction"]))


def printShellHelp():
    printBanner()

def toArray(string):
    return string.split(" ")

def runShell():
    SHELL_LOOP = True
    printBanner()
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
        print('dummy')
    elif input[0] in ["optimize"]:
        print('dummy')
    else:
        print("ERROR: ")
        print(input)
        print("IS NOT A VALID COMMAND.")
