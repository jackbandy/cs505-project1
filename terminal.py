'''
Currently, just a terminal
'''

import random


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
    # ex. "GRANT ON employees TO dexter"
    command_args = command.split()

    if command_args[0] not in command_strings:
        print("Unable to parse your command")
        printHelp()
        return

    if command_args[1] != "ON":
        print("Unable to parse your command")
        printHelp()
        return

    #TODO verify table exists

    if command_args[3] != "TO":
        print("Unable to parse your command")
        printHelp()
        return

    #TODO verify user exists

    confirmed = verifyCommand(action=command_args[0],
            table=command_args[2],
            user=command_args[4])

    if confirmed:
        executeCommand(action=command_args[0],
            table=command_args[2],
            user=command_args[4])
    else:
        print("Cancelled!")




def executeCommand(action, table, user):
    if action=="GRANT":
        print("You are performing a grant, which is not yet implemented")
    elif action=="FORBID":
        print("You are performing a revoke, which is not yet implemented")




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
    print("Example: {} ON table1 TO user1".format(
        random_command))



if __name__ == "__main__":
    main()
