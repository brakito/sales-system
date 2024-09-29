from src.utils import clearConsole, showTexts, pause, mainScreen, notification
from src.processes.closeSystem import closeSystem
from src.processes.manageProducts import manageProducts
from src.processes.manageNewSale import newSale
from src.processes.manageHistory import manageHistory
from src.processes.manageUsers import manageUsers
from src.auth.login import verifyLogin

def runSystem(role, name):
    while True:
        clearConsole()
        
        if role == 'admin':
            showTexts([
                mainScreen(),
                f"Welcome admin user {name}",
                f"0. Close Program\n1. Create Invoice\n2. View history\n3. Manage Products\n4. Manage Users"
            ])
            
            switch = {
                0: closeSystem,
                1: newSale,
                2: manageHistory,
                3: manageProducts,
                4: manageUsers
            }
        elif role == 'seller':
            showTexts([
                mainScreen(),
                f"Welcome seller user {name}",
                f"0. Close Program\n1. Create Invoice\n2. View history"
            ])
            
            switch = {
                0: closeSystem,
                1: newSale,
                2: manageHistory,
            }
        elif role == 'analyst':
            showTexts([
                mainScreen(),
                f"Welcome analyst user {name}",
                f"0. Close Program\n1. View history\n2. Generate report (comming soon or not)"
            ])
            
            switch = {
                0: closeSystem,
                1: manageHistory,
                # 2: generateReport
            }
        
        action = input("insert function #: ")

        if not action:
            action = 0
        elif action.isdigit() == False:
            print("Please try input a valid int value")
        else:
            action = int(action)

        clearConsole()
        function = switch.get(action, lambda: notification("error", "This action don't exist"))
        function()

        if (action == 0):
            break

verifyLogin(runSystem)