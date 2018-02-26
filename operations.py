'''
operations.py
The underbelly of the project
'''

from numpy import genfromtxt, savetxt
import pickle
import time


ASSIGNED_FILE_NAME = 'assigned.csv'
FORBIDDEN_FILE_NAME = 'forbidden.csv'
USERS_FILE_NAME = 'users.csv'

def executeCommand(action, table, user, actor, grant_option=0):
    '''
    This function is the highest abstraction for performing grant and forbid
    Returns True if successful
    '''

    if isSecurityOfficer(actor):
        return privilegedExecuteCommand(action=action, table=table, user=user,
                actor=actor, grant_option=grant_option)

    if action=="GRANT":
        if isForbidden(table, user):
            # give error
            print("sorry {}, grant of acces to \'{}\' by \'{}\' unacceptable".format(
                actor, table, user))
            return False
        if not isAssignedWithGrantOption(table=table, user=actor):
            print("sorry {}, you do not have privileges to add assignments on table \'{}\'".format(actor, table))
            logError(actor=actor, action='GRANT', table=table, user=user)
        if isAssigned(table=table, user=user):
            # if the assignment already exists, just log it
            logAction(actor=actor, action=action, table=table, user=user)
            print("Assignment already exists")
        else:
            addAssignment(table=table, user=user, actor=actor,
                    grant_option=grant_option)
            print("Added assignment")
            # add the assignment to the table

    elif action=="FORBID":
        print("Hey, {}! You are not a security officer!".format(actor))
        return False

    return True



def privilegedExecuteCommand(action, table, user, actor, grant_option=0):
    '''
    Handle commands executed by the security officer
    '''

    if action=="GRANT":
        if isForbidden(table, user):
            if confirmOverwrite(action,table,user):
                addForbid(actor=actor, table=table, user=user)
                print("Overwrite confirmed!")
                print("Affected users will be notified!")
                return True
            else:
                return False
        else:
            addAssignment(table=table, user=user, actor=actor,
                    grant_option=grant_option)
            print("Added assignment")
            # add the assignment to the table


    elif action=="FORBID":
        if not isSecurityOfficer(actor):
            # one last check just to be safe
            print("Hey, {}! You are not a security officer!".format(actor))
            logError(actor=actor, action=action, table=table, user=user)
            return False
        elif isForbidden(table, user): # do not add a duplicate rule
            print("User \'{}\' is already forbidden access to table \'{}\'".format(
                        user, table))
            return False
        else:
            # check the assigned table
            if isAssigned(table, user):
                if confirmOverwrite(action,table,user):
                    addForbid(actor=actor, table=table, user=user)
                    print("Overwrite confirmed!")
                    print("Affected users will be notified!")
                    pass
                else:
                    print("Overwrite cancelled!")
            else:
                addForbid(actor=actor, table=table, user=user)
                print("Forbidden!")

    return True



def confirmOverwrite(action, table, user):
    print("Are you ABSOLUTELY sure you want to {} access to the \'{}\' table by \'{}\'?".format(
                action, table, user))
    print("This conflicts with existing privileges!")
    while True:
        conf = input("YES or NO: ")
        if conf == "YES" or conf == "yes":
            return True
        else:
            return False



def isForbidden(table, user):
    '''
    A simple utility function to tell if a user is forbidden access to a table
    Returns true if forbidden, false if the entry does not exist
    '''
    forbidden = genfromtxt(FORBIDDEN_FILE_NAME, delimiter=',', dtype=str, skip_header=True)
    for u,t in forbidden:
        # check if an entry exists for table,user
        if t==table and u==user:
            # the entry is forbidden
            return True

    return False



def isValidUser(user):
    '''
    Utility function to tell if a username is in the list of valid users
    '''
    user_table = genfromtxt(USERS_FILE_NAME, dtype=str,delimiter=',',skip_header=True)
    usernames = user_table[:,0]
    if user in usernames:
        return True
        
    return False
    
    
    
def isSecurityOfficer(user):
    '''
    Utility function to tell if a username has security officer rights
    '''
    user_table = genfromtxt(USERS_FILE_NAME, dtype=str,delimiter=',',skip_header=True)
    for name, officer in user_table:
        if name == user:
            if officer == '1':
                return True
            return False
    return False



def isAssigned(table, user):
    '''
    Check if a user has been assigned rights to a given table
    '''
    assigned = genfromtxt(ASSIGNED_FILE_NAME, delimiter=',', dtype=str, skip_header=True)
    for u,t,g in assigned:
        # check if an entry exists for table,user
        if t==table and u==user:
            return True
    return False



def isAssignedWithGrantOption(table, user):
    '''
    Check if a user has rights to assign other users to a given table
    '''
    assigned = genfromtxt(ASSIGNED_FILE_NAME, delimiter=',', dtype=str, skip_header=True)
    for u,t,g in assigned:
        # check if an entry exists for table,user
        if t==table and u==user and g=='1':
            return True

    return False



def addAssignment(table, user, actor, grant_option=0):
    '''
    Add an assignment to the assigned table
    '''
    string_to_append = '\n{},{},{}'.format(user,table,grant_option)
    with open(ASSIGNED_FILE_NAME, 'a') as assignments:
        assignments.write(string_to_append)
    logAction(actor=actor, action='GRANT', table=table, user=user,
            grant_option=grant_option)



def addForbid(table, user, actor):
    '''
    Add an entry to the forbidden table
    '''
    string_to_append = '\n{},{}'.format(user,table)
    with open(FORBIDDEN_FILE_NAME, 'a') as forbidden:
        forbidden.write(string_to_append)
    logAction(actor=actor, action='FORBID', table=table, user=user)



def logAction(actor, action, table, user, grant_option=0):
    '''
    Write an executed action to the log file
    '''
    string_to_append ="{} {} performed {} on {} to {}\n".format(
            time.ctime(time.time()), actor, action, table, user)
    if grant_option == 1:
        string_to_append ="{} {} performed {} on {} to {} WITH GRANT OPTION\n".format(
            time.ctime(time.time()), actor, action, table, user)
    with open('log.txt', 'a') as logfile:
        logfile.write(string_to_append)



def logError(actor, action, table, user):
    '''
    Write an error to the log file
    '''
    string_to_append ="{} {} attempted {} on {} to {}\n".format(
            time.ctime(time.time()), actor, action, table, user)
    with open('log.txt', 'a') as logfile:
        logfile.write(string_to_append)
