"""
@author: Justin Pusztay

In this file we define economic transactions.
"""

def merchantTransaction(buyer,seller,item):
    """
    This function takes a buyer, seller, and an item. It checks the
    buyer/seller logic and if those are both are true than it executes
    the transacton.
    """
    if buyer.buyLogic(item,item.getValue()) and \
    seller.sellLogic(item,item.getValue()):
        buyer.buyItem(item,item.getValue())
        seller.sellItem(item,item.getValue())
        item.setOwner(buyer)
    
