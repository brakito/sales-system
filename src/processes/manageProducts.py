from src.utils import showTexts, pause, getIntInput, getFloatInput, getStringInput, verifyProductId, clearConsole
from src.db import addProduct, delProduct, getPrice, uptPrice, getStock, uptStock
from src.products import createProductsList

# Main process
def manageProducts():
    while True:
        clearConsole()
        formatedList = createProductsList()
        showTexts([
            formatedList,
            "Chose a procces",
            f"0. Back\n1. Create Product\n2. Delete Product\n3. Update Price\n4. Update Stock"
        ])
        
        switch = {
            0: backToHome,
            1: createProduct,
            2: deleteProduct,
            3: updatePrice,
            4: updateStock
        }

        action = input("Action #: ")

        if not action:
            action = 0
        elif action.isdigit() == False:
            print("Please try input a valid int value")
        else:
            action = int(action)

        function = switch.get(action, lambda _f: print("This action don't exist"))
        function(formatedList)

        if (action == 0):
            break
        else:
            pause()

# Subprocesses
def backToHome(formatedList):
    print("Leaving Managment Products...")

def createProduct(formatedList):
    name = getStringInput("Name: ", ["ADD A NEW PRODUCT"])
    price = getFloatInput("Price: ", ["ADD A NEW PRODUCT", f"Name: {name}"])
    stock = getIntInput("Stock: ", ["ADD A NEW PRODUCT", f"Name: {name}", f"Price: {price}"])

    try:
        addProduct((name, price, stock))
    except:
        print("Error: There was an error adding the product, try Again.")

    print("Product Added")

def deleteProduct(formatedList):
    while True:
        id = getIntInput(
            "Product Id: ", 
            ["DELETE A PRODUCT", formatedList, "Enter the id of the product you wanna delete (Enter 0 to cancell)"]
        )

        if id == 0:
            break
        elif not verifyProductId(id):
            print("This Product Id is not valid")
            pause()
        else: 
            break

    if id == 0:
        print("Process cancelled!")
    else:
        try:
            delProduct(id)
            print("Product Deleted")
        except:
            print("Product Was not deleted")

def updatePrice(formatedList):
    # Get a valid id
    while True:
        id = getIntInput(
            "Product Id: ", 
            ["UPDATE A PRODUCT PRICE", formatedList, "Enter the id of the product you wanna change (Enter 0 to cancell)"]
        )

        if id == 0:
            break
        elif not verifyProductId(id):
            print("This Product Id is not valid")
            pause()
        else: 
            break
    
    # Close or get actual id
    if id == 0:
        print("Process cancelled!")
        return 0
    else:
        result = getPrice(id)

    # Get a valid new float value for replace the current price
    newPrice = getFloatInput(
        "New Price: ",
        [f"The {result[0]}'s current price is {result[1]}", "Enter the new price for this product"]
    )

    # Update price
    uptPrice(id, newPrice)
    print(f"\nThe {result[0]}'s price was updated from {result[1]} to {newPrice}")

def updateStock(formatedList):
    while True:
        id = getIntInput(
            "Product Id: ", 
            ["UPDATE A PRODUCT STOCK", formatedList, "Enter the id of the product you wanna change (Enter 0 to cancell)"]
        )

        if id == 0:
            break
        elif not verifyProductId(id):
            print("This Product Id is not valid")
            pause()
        else: 
            break

    if id == 0:
        print("Process cancelled!")
        return 0
    else:
        (productName, currentStock) = getStock(id)

    switch = {
        1: lambda stock, newStock: stock + newStock,
        2: lambda stock, newStock: stock - newStock,
        3: lambda stock, newStock: newStock
    }

    while True:
        operation = getIntInput("Operation #: ", [
            f"The {productName}'s current stock is {currentStock}",
            "Enter an operation & the new stock for this product",
            "OPERATIONS\n1. Add\n2. Subtract\n3. Replace"
        ])

        if switch.get(operation, "invalid") == "invalid":
            print("This actión is invalid")
            pause()
        else:
            break

    newStock = getIntInput("New Stock: ", [
        f"The {productName}'s current stock is {currentStock}",
        "Enter an operation & the new stock for this product",
        "OPERATION CAN BE\n1. Add\n2. Subtract\n3. Replace",
        f"Operation #: {operation}"
    ])

    function = switch.get(operation, lambda: print("This action is undefined"))
    newStock = function(currentStock, newStock)

    uptStock(id, newStock)
    print(f"The {productName}'s stock was updated from {currentStock} to {newStock}")

