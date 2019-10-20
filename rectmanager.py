import copy, pygame

def getRects(image):
    image = copy.copy(image)
    pxa = pygame.PixelArray(image)
    topCorner = pxa[0,0]
    scale = 1
    rects, flag, count = [], False, 0

    for w in range(pxa.shape[0]):
        for h in range(pxa.shape[1]):
            if pxa[w,h] != topCorner:
                if not flag:
                    leftBound, flag = (w,h), True
                else: count += 1
            elif pxa[w,h] == topCorner and flag:
                rects.append(pygame.Rect(leftBound[0],leftBound[1],
                                         scale,scale*count))
                flag, count = False, 0
                
    return rects

def moveRects(rects, pos):
    return [rect.move(pos[0],pos[1]) for rect in rects]
                    
