import pandas as pd
from tabulate import tabulate

from src.utils import showTexts, pause
from src.db import useDataBase

def manageHistory ():
    sales = formatSale()
    
    for sale in sales:
        # if len(sale['products']) > 0: # if bad rows crash the system
        df = pd.DataFrame(sale['products'])
        subTotal = round(df['Sub Total'].sum(), 2)
        discountValue = round(subTotal * sale['discount'], 2)
        taxesValue = round((subTotal - discountValue) * sale['taxes'], 2)
        total = round((subTotal - discountValue) + taxesValue, 2)

        showTexts([
            f"Sale Id: {sale['id']}\nDate: {sale['date']}",
            tabulate(df, headers='keys', tablefmt='pipe', showindex=False),
            f"Sub Total: {subTotal}\nDiscount ({sale['discount']}%): {discountValue}\nTaxes ({sale['taxes']}%): {taxesValue}\n..................\nTotal: {total}",
            f"............................................................................"
        ])

    pause()

def formatSale ():
    sales = useDataBase("SELECT * FROM sale")

    salesList = []

    for sale in sales:
        saleId = sale[0]
        products = useDataBase('''
            SELECT productInSale.productId, product.name, productInSale.count, productInsale.unitPrice, productInSale.count * productInsale.unitPrice as subTotal
            FROM productInSale
            INNER JOIN product ON productInSale.productId = product.productId
            WHERE saleId = ?''',
            (saleId,)
        )
        columns = ['Id', 'Name', 'Count', 'Unit Price', 'Sub Total']

        saleInfo = {
            'id': saleId,
            'date': sale[1],
            'products': [dict(zip(columns, row)) for row in products],
            'taxes': sale[2],
            'discount': sale[3],
            'total': sale[4],
        }

        salesList.append(saleInfo)
    
    return salesList
