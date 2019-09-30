"""
In this file we define economic transactions.
"""

def merchantTransaction(buyer,seller,item):
    if buyer.buyLogic(item,item.getValue()) and \
    seller.sellLogic(item,item.getValue()):
        buyer.buyItem(item,item.getValue())
        seller.sellItem(item,item.getValue())
    
