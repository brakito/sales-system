import pandas as pd
from tabulate import tabulate

from src.db import getAllProducts, initDB

initDB()

def getProducts():
    result = getAllProducts()
    columns = ['productId', 'name', 'price', 'stock']
    productsListDB = [dict(zip(columns, row)) for row in result]
    return {product["productId"]: product for product in productsListDB}


def createProductsList():
    result = getAllProducts()
    columns = ['productId', 'name', 'price', 'stock']
    productsListDB = [dict(zip(columns, row)) for row in result]
    
    df = pd.DataFrame(productsListDB)
    return tabulate(df, headers='keys', tablefmt='pipe', showindex=False)