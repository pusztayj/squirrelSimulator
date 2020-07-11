def lootItems(opponents):
    """
    Generates a list of items that can be used
    """
    lootItems = list()
    for x in opponents:
        if x != None:
            ivt = x.getInventory()
            for y in ivt:
                if random.randint(0,100) <= 100:#25: # items can be looted only 25% of time
                # add to spreadsheet
                    lootItems.append(y)
    return lootItems
        
def lootAcorns(opponents):
    """
    Generates the number of acorns you looted.
    """
    acorns = sum([x.getAcorns() for x in opponents if x!=None])
    acornsLooted = acorns*random.uniform(0,0.4) # spreadsheeet 
    return math.floor(acornsLooted)
