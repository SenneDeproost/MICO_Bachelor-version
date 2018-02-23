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
    command = input[0]
    possible_commands = g.commands["shell"]
    args = input[1:]
    number_of_args = len(args)

    if command[0] == '!':
        command_string = command[1:] + "(*args)"
        exec("%s" % command_string)

    elif command in possible_commands:
        command_string = "do_" + command + "(*args)"
	exec("%s" % command_string)

    else:
        print("ERROR, %s is an invalid command." % command)


def add(a, b):
    print a + b

def do_help():
    print "haha"

def do_version():
    print(g.VERSION_NUMBER)

def do_exit():
    exit()
