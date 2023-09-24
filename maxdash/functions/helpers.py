import pygame

def center(image=None, cordinate=(0,0)):
    imageX, imageY = image.get_size()
    return (cordinate[0] - (imageX/2), cordinate[1] - (imageY/2))

def expandRect(rect, margin):
    return pygame.Rect(rect.x - margin, rect.y - margin, rect.w + 2 * margin, rect.h + 2 * margin)

def drawText(screen, displayText, font, position, color):
    text = font.render(displayText, True, color)
    textRect = text.get_rect()

    textRect.x = position[0]
    textRect.centery = position[1]

    screen.blit(text, textRect)

    return textRect

def formatNumber(num, decimals):
    if type(num) not in [int, float]:
        return "Invalid input: not a number"

    if type(decimals) != int or decimals < 0 or decimals > 500:
        return "Invalid input: decimals must be an integer between 0 and 500"

    format_string = "{:." + str(decimals) + "f}"
    return format_string.format(num)