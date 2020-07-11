from managers import CONSTANTS

def centerGraphicsElement(element, axes=(True, True)):
    new_x = element.getX()
    new_y = element.getY()
    if axes[0]:
        screen_width = CONSTANTS.get("screen_size")[0]
        width = element.getWidth()
        new_x = (screen_width // 2) - (width // 2)
    if axes[1]:
        screen_height = CONSTANTS.get("screen_size")[1]
        height = element.getHeight()
        new_y = (screen_height // 2) - (height // 2)
    element.setPosition((new_x, new_y))
