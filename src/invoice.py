class Invoice: 
    def __init__ (self, orderInvoice):
        self.id = orderInvoice["id"]
        self.date = orderInvoice["date"]
        # self.client = orderInvoice["client"]
        self.products = orderInvoice["products"]
    
    def designInvoice (self):
        return 0
    
class InvoiceToPrint(Invoice):
    def __init__ (self, orderInvoice):
        super().__init__ (orderInvoice)

    def print(self):
        return self.designInvoice()