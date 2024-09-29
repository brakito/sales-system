from src.auth.account import Account, createAdmin
from src.utils import getStringInput, mainScreenLogo

account = Account()

def verifyLogin (processToDo):
    createAdmin()
    
    while True:
        userName = getStringInput("User Name: ", [mainScreenLogo, "LOGIN"])
        password = getStringInput("Password: ", [mainScreenLogo, "LOGIN", f"User Name: {userName}"])

        #userName = 'admin'
        # password = '4dmin'
        # password = '4dmin*2024'

        # userName = 'jack'
        # password = '-jacky3-'

        # userName = 'sara'
        # password = 'Sara*2024'
        
        if account.login(userName, password):
            break
    
    role = account.getUserData()['role']
    name = account.getUserData()['name']
    processToDo(role, name)