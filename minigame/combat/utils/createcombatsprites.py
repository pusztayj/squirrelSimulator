from .combatsprite import CombatSprite

def createCombatSprites(allies,enemies,font):
    """
    Here we create the combat sprite for each animal of each pack. 
    """
    combatSprites = list()
    y = 200
    for a in allies:
        if allies.isLeader(a):
            c = CombatSprite(a,(228,275),font)
            combatSprites.append(c)
        else:
            if a != None:
                c = CombatSprite(a,(100,y),font)
                combatSprites.append(c)
                y+=150
    y = 200
    for e in enemies:
        if enemies.isLeader(e):
            c = CombatSprite(e,(847,275),font,enemies = True)
            combatSprites.append(c)
        else:
            if e != None:
                c = CombatSprite(e,(972,y),font,enemies = True)
                combatSprites.append(c)
                y+=150

    return combatSprites
