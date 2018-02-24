'''
operations.py
The underbelly of the project
'''

from numpy import genfromtxt, savetxt

def executeCommand(action, table, user, actor):
    if action=="GRANT":
        if isForbidden(table, user):
            # give error
            print("sorry {}, grant of acces to \'{}\' by \'{}\' unacceptable".format(
                actor, table, user))
        else:
            addAssignment(table, user)
            print("Added assignment")
            # add the assignment to the table



    elif action=="FORBID":
        if not isSecurityOfficer(actor):
            print("Hey, {}! You are not a security officer!".format(actor))
            logError(actor=actor, action=action, table=table, user=user)
            return
        else:
            # check the assigned table
            # potentially overwrite assigned table
            # warn the user if it will disrupt anything
            pass



def isForbidden(table, user):
    # load forbidden table
    # check if an entry exists for table,user
    forbidden = genfromtxt('forbidden.csv', delimiter=',', dtype=str, skip_header=True)
    for u,t in forbidden:
        if t==table and u==user:
            # the entry is forbidden
            return True

    return False



def isValidUser(user):
    user_table = genfromtxt('users.csv', dtype=str,delimiter=',',skip_header=True)
    usernames = user_table[:,0]
    if user in usernames:
        return True
        
    return False
    
    
    
def isSecurityOfficer(user):
    user_table = genfromtxt('users.csv', dtype=str,delimiter=',',skip_header=True)
    for name, officer in user_table:
        if name == user:
            if officer == '1':
                return True
            return False
    return False



def isAssigned(table, user):
    pass



def addAssignment(table, user):
    assigned = genfromtxt('assigned.csv', delimiter=',', dtype=str, skip_header=True)
    string_to_append = '\n{},{},1'.format(user,table)
    with open('assigned.csv', 'a') as assignments:
        assignments.write(string_to_append)



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
