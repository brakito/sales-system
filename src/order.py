import random
from src.utils import pause
import pandas as pd
from tabulate import tabulate

from src.products import getProducts
from src.db import useDataBase

class Order:
    def __init__ (self, list = None, taxes = 0.25, discount = 0.0):
        if list is None:
            list = []
        self.__list = list
        self.__taxes = taxes
        self.__taxesValue = 0.0
        self.__discount = discount
        self.__discountValue = 0.0
        self.__subTotal = 0.0 # only products price
        self.__total = 0.0

    def addProduct (self, productId, count):
        indexItem = next((i for i, item in enumerate(self.__list) if item[0] == productId), None)

        if indexItem is not None:
            if count >= 0:
                self.updateCount(indexItem, count)
            else:
                self.updateCount(indexItem, abs(count), "substract")
        elif count > 0:
            products = getProducts()
            name = products[productId]["name"]
            actualPrice = products[productId]["price"]

            self.__list.append((productId, name, count, actualPrice, count * actualPrice))
        else:
            print("Something went wrong, the product could not be added")
            pause()
    
    def updateCount (self, indexItem, count, operation = "add"):
        oi = self.__list[indexItem] # Old Item
        newCount = oi[2]

        if operation == "add":
            newCount += count
        elif operation == "substract":
            newCount -= count
        
        if newCount > 0:
            self.__list[indexItem] = (oi[0], oi[1], newCount, oi[3], newCount * oi[3])
        else:
            self.__list.pop(indexItem)
            print("Since the new quantity is smaller than 0, the product was deleted")
            pause()

    def updateValues (self):
        df = pd.DataFrame(self.__list, columns=['ID', 'Name', 'Cuantity', 'Actual_Price', 'Sub_Total'])

        self.__subTotal = round(df['Sub_Total'].sum(), 2)
        self.__discountValue = round(self.__subTotal * self.__discount, 2)
        self.__taxesValue = round((self.__subTotal - self.__discountValue) * self.__taxes, 2)
        self.__total = round(self.__subTotal - self.__discountValue + self.__taxesValue, 2)

    def getValues (self):
        return {
            "total": self.__total,
            "subTotal": self.__subTotal,
            "taxes": self.__taxes,
            "taxesValue": self.__taxesValue,
            "discount": self.__discount,
            "discountValue": self.__discountValue
        }
    
    def updatePreview (self):
        self.updateValues()
        df = pd.DataFrame(self.__list, columns=['ID', 'Name', 'Cuantity', 'Actual_Price', 'Sub_Total'])
        return f"{tabulate(df, headers='keys', tablefmt='pipe', showindex=False)}\n\nSub Total: {self.__subTotal}\nDiscount ({self.__discount * 100}%): {self.__discountValue}\nTaxes ({self.__taxes * 100}%): {self.__taxesValue}\n..................\nTotal: {self.__total}"
    
    def confirmOrder (self):
        try:
            if len(self.__list) > 0:
                saleId = useDataBase('INSERT INTO sale (taxes, discount, total) VALUES (?, ?, ?)', (self.__taxes, self.__discount, self.__total), True)
            
                for product in self.__list:
                    currentStock = useDataBase('SELECT stock FROM product WHERE productId = ?', (product[0],))
                    newStock = currentStock[0][0] - product[2]
                    useDataBase('UPDATE product SET stock = ? WHERE productId = ?', (newStock, product[0]))
                    useDataBase('INSERT INTO productInSale (saleId, productId, count, unitPrice) VALUES (?, ?, ?, ?)', (saleId, product[0], product[2], product[3]))
        
                print("Saved!")
        except:
            print("Something crashed, try again")
    
    def createInvoice (self):
        # fecha, id, productos
        return 0