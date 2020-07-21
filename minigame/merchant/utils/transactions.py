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
    if buyer.buyLogic(item,item.getAttribute("value")) and \
    seller.sellLogic(item,item.getAttribute("value")):
        buyer.buyItem(item,item.getAttribute("value"))
        seller.sellItem(item,item.getAttribute("value"))
        item.setOwner(buyer)
    
