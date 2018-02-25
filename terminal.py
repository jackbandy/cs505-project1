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
    '''
    Top-level function, called first
    '''
    print("CS 505 project 1")
    print("----------------\n")
    authenticate()



def authenticate():
    '''
    Allows users to log in
    '''
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

    if operations.isSecurityOfficer(uname):
        print("Welcome, officer {}!\n".format(uname))
    else:
        print("Welcome, {}!\n".format(uname))

    inputLoop(actor=uname)




def inputLoop(actor):
    '''
    Takes user input
    '''
    while True:
        response = input("{}> ".format(actor))
        if len(response) == 0:
            continue 
        elif response == 'exit':
            exit()
        else:
            parseCommandString(command=response, actor=actor)




def parseCommandString(command, actor):
    '''
    Translates an input string into an array of arguments
    '''
    # ex. "GRANT employees TO dexter"
    # ex. "GRANT employees TO dexter WITH GRANT OPTION"
    grant_option = 0
    command_args = command.split()

    if command_args[0] not in command_strings:
        print("Unable to parse your command")
        printHelp()
        return

    if command_args[2] != "TO":
        print("Unable to parse your command")
        printHelp()
        return

    if not operations.isValidUser(command_args[3]):
        print("Error: User {} does not exist".format(command_args[3]))
        return

    if command[-17:] == 'WITH GRANT OPTION':
        grant_option = 1


    confirmed = verifyCommand(action=command_args[0],
            table=command_args[1],
            user=command_args[3],
            grant_option=grant_option)

    if confirmed:
        operations.executeCommand(action=command_args[0],
            table=command_args[1],
            user=command_args[3],
            actor=actor,
            grant_option=grant_option)
    else:
        print("Cancelled!")




def verifyCommand(action, table, user, grant_option=0):
    if action=="GRANT":
        if grant_option == 1:
            print("Are you sure you want to give \'{}\' access to the \'{}\' table AND allow her to grant others access?".format(
                user, table))
        else:
            print("Are you sure you want to give \'{}\' access to the \'{}\' table?".format(
                user, table))
    elif action=="FORBID":
        print("Are you sure you want to forbid \'{}\' access to the \'{}\' table?".format(
            user, table))

    while True:
        conf = input("YES or NO: ")
        if conf == "YES" or conf == "yes":
            return True 
        if conf == "NO" or conf == "no":
            return False




def printHelp():
    print("Valid commands: {}".format(command_strings))
    random_command = random.choice(command_strings)
    print("Example: {} table1 TO user1".format(
        random_command))



if __name__ == "__main__":
    main()
