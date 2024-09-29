from src.order import Order
from src.utils import pause, getIntInput, verifyProductId

def newSale ():
    order = Order()

    while (True):
        # productId
        while True:
            productId = getIntInput(
                "Product Id: ", [
                "ADD A NEW PRODUCT\nAdd products by Product Id (Enter 0 in Product Id to finish order)\nIf Cuantity is negative, so this subtract from current product cuantity",
                order.updatePreview(),
            ])

            if productId == 0:
                break
            elif not verifyProductId(productId):
                print("This Product Id is not valid")
                pause()
            else: 
                break

        if productId == 0:
            break
        
        # Cuantity
        while True:
            count = getIntInput("Cuantity: ", [
                "ADD A NEW PRODUCT\nEnter product id (Enter 0 in Product Id to finish order)\nIf Cuantity is negative, so this subtract from current product cuantity",
                order.updatePreview(),
                f"Product Id: {productId}"
            ])

            if count == 0:
                print("cuantity can't be 0")
                pause()
            else:
                break

        order.addProduct(int(productId), int(count))

    order.confirmOrder()