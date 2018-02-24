#! /bin/sh
""":"
exec python $0 ${1+"$@"}
"""


'''
Currently, just a terminal
'''

import random
import csv
import time
from numpy import genfromtxt, savetxt


# constants
command_strings = ["GRANT", "FORBID"]
valid_users = ["jack", "seif"]



def main():
    print("CS 505 project 1")
    print("----------------\n")
    authenticate()



def authenticate():
    authenticated = False

    while not authenticated:
        officer = False
        uname = input("username: ")
        if len(uname) == 0:
            break
        else:
            print("Authenticating...")
            if uname == 'securityofficer':
                authenticated = True
                officer = True
            elif uname in valid_users:
                authenticated = True
            else:
                print("Authentication failed")
    print("Welcome, {}!\n".format(uname))

    inputLoop(user=uname, officer=officer)



def inputLoop(user="", officer=False):
    while True:
        response = input("{}> ".format(user))
        if len(response) == 0:
            break
        elif response == 'exit':
            exit()
        else:
            parseCommandString(response)



def parseCommandString(command):
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
            user=command_args[3])
    else:
        print("Cancelled!")




def executeCommand(action, table, user):
    if action=="GRANT":
        if isForbidden(table, user):
            # give error
            print("grant of acces to \'{}\' by \'{}\' unacceptable".format(
                table, user))
        else:
            addAssignment(table, user)
            print("Added assignment")
            # add the assignment to the table



    elif action=="FORBID":
        # make sure it's the security officer
        # check the assigned table
        # potentially overwrite assigned table
        # warn the user if it will disrupt anything
        print("You are performing a revoke, which is not yet implemented")



def isForbidden(table, user):
    # load forbidden table
    # check if an entry exists for table,user
    forbidden = genfromtxt('forbidden.csv', delimiter=',', dtype=str, skip_header=True)
    for u,t in forbidden:
        if t==table and u==user:
            # the entry is forbidden
            return True

    return False



def isAssigned(table, user):
    pass



def addAssignment(table, user):
    assigned = genfromtxt('assigned.csv', delimiter=',', dtype=str, skip_header=True)
    string_to_append = '\n{},{},1'.format(user,table)
    with open('assigned.csv', 'a') as assignments:
        assignments.write(string_to_append)




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




def logAction(actor, action, table, user):
    string_to_append ="{} {} performed {} on {} to {}\n".format(
            time.ctime(time.time()), actor, action, table, user)
    with open('log.txt', 'a') as logfile:
        logfile.write(string_to_append)



def logError(actor, action, table, user):
    string_to_append ="{} {} attempted {} on {} to {}\n".format(
            time.ctime(time.time()), actor, action, table, user)
    with open('log.txt', 'a') as logfile:
        logfile.write(string_to_append)




def printHelp():
    print("Valid commands: {}".format(command_strings))
    random_command = random.choice(command_strings)
    print("Example: {} table1 TO user1".format(
        random_command))



if __name__ == "__main__":
    main()
