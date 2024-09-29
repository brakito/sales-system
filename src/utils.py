import os
from src.db import useDataBase

def clearConsole():
    os.system("cls")

def showTexts(texts):
    for text in texts:
        print(f"{text}\n")

def pause():
    input("Press \"Enter\" to continue...")

def mainScreen():
    return f" _______  _______  ___      _______  _______    _______  __   __  _______  _______  _______  __   __ \n|       ||   _   ||   |    |       ||       |  |       ||  | |  ||       ||       ||       ||  |_|  |\n|  _____||  |_|  ||   |    |    ___||  _____|  |  _____||  |_|  ||  _____||_     _||    ___||       |\n| |_____ |       ||   |    |   |___ | |_____   | |_____ |       || |_____   |   |  |   |___ |       |\n|_____  ||       ||   |___ |    ___||_____  |  |_____  ||_     _||_____  |  |   |  |    ___||       |\n _____| ||   _   ||       ||   |___  _____| |   _____| |  |   |   _____| |  |   |  |   |___ | ||_|| |\n|_______||__| |__||_______||_______||_______|  |_______|  |___|  |_______|  |___|  |_______||_|   |_|"

mainScreenLogo = f" _______  _______  ___      _______  _______    _______  __   __  _______  _______  _______  __   __ \n|       ||   _   ||   |    |       ||       |  |       ||  | |  ||       ||       ||       ||  |_|  |\n|  _____||  |_|  ||   |    |    ___||  _____|  |  _____||  |_|  ||  _____||_     _||    ___||       |\n| |_____ |       ||   |    |   |___ | |_____   | |_____ |       || |_____   |   |  |   |___ |       |\n|_____  ||       ||   |___ |    ___||_____  |  |_____  ||_     _||_____  |  |   |  |    ___||       |\n _____| ||   _   ||       ||   |___  _____| |   _____| |  |   |   _____| |  |   |  |   |___ | ||_|| |\n|_______||__| |__||_______||_______||_______|  |_______|  |___|  |_______|  |___|  |_______||_|   |_|"

def getIntInput(label, showBefore):
    while True:
        clearConsole()
        showTexts(showBefore)
        
        userInput = input(label)

        if not userInput or userInput.lstrip('-').isdigit() == False:
            print("Please enter a valid integer value")
            pause()
        else:
            return int(userInput)

def getFloatInput(label, showBefore):
    while True:
        clearConsole()
        showTexts(showBefore)
        
        userInput = input(label)

        if not userInput or userInput.replace(".", "", 1).isdigit() == False or float(userInput) <= 0:
            print("Please enter a valid decimal value")
            pause()
        else:
            return round(float(userInput), 2)

def getStringInput(label, showBefore):
    while True:
        clearConsole()
        showTexts(showBefore)
        
        userInput = input(label)

        if not userInput:
            print("Please enter a valid string")
            pause()
        else:
            return userInput
        
def verifyProductId(id):
    result = useDataBase('SELECT * FROM product WHERE productId = ?', (id,))
    if len(result) == 0:
        return False
    return True

def notification(type, label):
    if type == "alert":
        content = f"\nALERT:\n{label}\n"
    elif type == "error":
        content = f"\nERROR:\n{label}\n"
    else:
        content = f"\nDEV:\ntype {type} isn't valid\n"
    
    print(content)
    pause()