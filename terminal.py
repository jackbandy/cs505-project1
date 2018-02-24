#! /bin/sh
""":"
exec python $0 ${1+"$@"}
"""


'''
A terminal for interacting with the privileges
Handles login/authentication and input parsing
'''

import random
import time
import operations
from numpy import genfromtxt, savetxt


# constants
command_strings = ["GRANT", "FORBID"]


def main():
    print("CS 505 project 1")
    print("----------------\n")
    authenticate()



def authenticate():
    authenticated = False

    while not authenticated:
        uname = input("username: ")
        if len(uname) == 0:
            break
        else:
            print("Authenticating...")
            if operations.isValidUser(uname):
                authenticated = True
            else:
                print("Authentication failed")
    print("Welcome, {}!\n".format(uname))

    inputLoop(actor=uname)



def inputLoop(actor):
    while True:
        response = input("{}> ".format(actor))
        if len(response) == 0:
            continue 
        elif response == 'exit':
            exit()
        else:
            parseCommandString(command=response, actor=actor)



def parseCommandString(command, actor):
    # ex. "GRANT employees TO dexter"
    command_args = command.split()

    if command_args[0] not in command_strings:
        print("Unable to parse your command")
        printHelp()
        return

    #TODO verify table exists
    

    if command_args[2] != "TO":
        print("Unable to parse your command")
        printHelp()
        return

    #TODO verify user exists

    confirmed = verifyCommand(action=command_args[0],
            table=command_args[1],
            user=command_args[3])

    if confirmed:
        executeCommand(action=command_args[0],
            table=command_args[1],
            user=command_args[3],
            actor=actor)
    else:
        print("Cancelled!")






def verifyCommand(action, table, user):
    if action=="GRANT":
        print("Are you sure you want to give \'{}\' access to the \'{}\' table?".format(
            user, table))
    elif action=="FORBID":
        print("Are you sure you want to forbid \'{}\' access to the \'{}\' table?".format(
            user, table))

    while True:
        conf = input("YES or NO: ")
        if conf == "YES":
            return True 
        if conf == "NO":
            return False









def printHelp():
    print("Valid commands: {}".format(command_strings))
    random_command = random.choice(command_strings)
    print("Example: {} table1 TO user1".format(
        random_command))



if __name__ == "__main__":
    main()
