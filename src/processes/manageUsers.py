import pandas as pd
from tabulate import tabulate
import re

from src.utils import showTexts, clearConsole, getStringInput, notification
from src.db import useDataBase
from src.auth.login import account

def manageUsers ():
    while True:
        clearConsole()
        formatedList = createUsersList()
        showTexts([
            formatedList,
            "Chose a procces",
            f"0. Back\n1. Create User\n2. Delete User\n3. Update User Info"
        ])
        
        switch = {
            0: backToHome,
            1: createUser,
            2: deleteUser,
            3: updateUserInfo,
        }

        action = input("Action #: ")

        if not action:
            action = 0
        elif action.isdigit() == False:
            print("Please try input a valid int value")
        else:
            action = int(action)

        function = switch.get(action, lambda _f: print("This action don't exist"))
        function()

        if (action == 0):
            break

def createUsersList ():
    users = useDataBase('SELECT userName, name, role FROM user')
    columns = ['User Name', 'Name', 'Role']
    usersDict = [dict(zip(columns, rows)) for rows in users]

    df = pd.DataFrame(usersDict)
    formatedUsers = tabulate(df, headers='keys', tablefmt='pipe', showindex=False)
    
    return formatedUsers

def backToHome ():
    print("Leaving Managment User...")

def createUser ():
    while True:
        userName = getStringInput("User Name: ", [
            "CREATE A NEW USER",
            "Username must be unique."
        ])

        if userName == "0":
            return
        elif len(useDataBase('SELECT * FROM user WHERE userName = ?', (userName,))) != 0:
            notification("alert", "This User Name alredy exists")
        else:
            break

    while True:
        password = getStringInput("Password: ", [
            "CREATE A NEW USER",
            "userName must be unique.",
            f"User Name: {userName}"
        ])

        if len(password) < 8:
            notification("alert", "Password must be more longer (min 8 characters)")
        elif not (re.search(r'[a-zA-Z]', password) and re.search(r'\d', password) and re.search(r'[_\W]', password)):
            notification("alert", "Password must to have letters, numbers and symbols")
        else:
            break

    name = getStringInput("Name: ", [
        "CREATE A NEW USER",
            "userName must be unique.",
            f"User Name: {userName}\nPassword: {password}"
    ])

    while True:
        role = getStringInput("Role: ", [
            "CREATE A NEW USER",
            "userName must be unique.",
            f"User Name: {userName}\nPassword: {password}\nName: {name}"
        ])

        if role == 'admin':
            notification("alert", "You can't to have more than one admin account")
        elif not (role == 'seller' or role == 'analyst'):
            notification("alert", "Role only can be: seller or analyst")
        else:
            break

    account.register(userName, password, name, role)

def deleteUser ():
    while True:
        userName = getStringInput("User Name: ", [
            createUsersList(),
            "DELETE USER BY USER NAME",
            "Input 0 to cancell"
        ])

        if userName == "0":
            notification("alert", "Cancelling deleting user!")
            return
        elif len(useDataBase('SELECT * FROM user WHERE userName = ?', (userName,))) == 0:
            notification("alert", "This user not exist")
        elif useDataBase("SELECT role FROM user WHERE userName = ?", (userName,))[0][0] == 'admin':
            notification("alert", "Admin user can't be deleted")
        else:
            break

    account.deleteUser(userName)

def updateUserInfo ():
    while True:
        userName = getStringInput("User Name: ", [
            createUsersList(),
            "EDIT INFO FOR THIS USER",
            "Input 0 to cancell"
        ])

        if userName == "0":
            return
        elif len(useDataBase('SELECT * FROM user WHERE userName = ?', (userName,))) == 0:
            notification("alert", "This User don't exist")
        else:
            break

    while True:
        password = getStringInput("Password: ", [
            "EDIT INFO FOR THIS USER\n-----------------------",
            f"CHANGE PASSWORD FOR USER {userName}",
            "Input 0 to mantain old value in this field",
        ])

        if password == "0":
            password = None
            break
        elif len(password) < 8:
            notification("alert", "Password must be more longer (min 8 characters)")
        elif not (re.search(r'[a-zA-Z]', password) and re.search(r'\d', password) and re.search(r'[_\W]', password)):
            notification("alert", "Password must to have letters, numbers and symbols")
        else:
            break

    while True:
        name = getStringInput("Name: ", [
            "EDIT INFO FOR THIS USER\n-----------------------",
            f"CHANGE NAME FOR USER {userName}",
            "Input 0 to mantain old value in this field",
        ])

        if name == "0":
            name = None
            break
        else:
            break
    
    if useDataBase("SELECT role FROM user WHERE userName = ?", (userName,))[0][0] != 'admin':
        while True:
            role = getStringInput("Role: ", [
                "EDIT INFO FOR THIS USER\n-----------------------",
                f"CHANGE ROLE FOR USER {userName}",
                "Input 0 to mantain old value in this field",
            ])

            if role == "0":
                role = None
                break
            elif role == 'admin':
                notification("alert", "You can't to have more than one admin account")
            elif not (role == 'seller' or role == 'analyst'):
                notification("alert", "Role only can be: seller or analyst")
            else:
                break
    else:
        role = None

    account.updateUserInfo(userName, password, name, role)