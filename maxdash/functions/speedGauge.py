import pygame
import math

def drawNeedle(surface, angle, length, centerX, centerY, gap):
    thickness = 6
    startX = centerX + gap * math.sin(math.radians(angle))
    startY = centerY - gap * math.cos(math.radians(angle))
    endX = centerX + (length + gap) * math.sin(math.radians(angle))
    endY = centerY - (length + gap) * math.cos(math.radians(angle))
    pygame.draw.line(surface, (255, 0, 0), (startX, startY), (endX, endY), thickness)

    margin = 20
    x_min = min(startX, endX) - margin
    x_max = max(startX, endX) + margin
    y_min = min(startY, endY) - margin
    y_max = max(startY, endY) + margin

    needleRect = pygame.Rect(x_min, y_min, x_max - x_min, y_max - y_min)

    return needleRect

def mapSpeedToAngle(value):
    minAngle = -135
    maxAngle = 135
    minSpeed=0
    maxSpeed=240
    return minAngle + (maxAngle - minAngle) * (value - minSpeed) / (maxSpeed - minSpeed)

def mapRpmToAngle(value):
    minAngle = -180
    maxAngle = 128
    minRpm=0
    maxRpm=8000
    return minAngle + (maxAngle - minAngle) * (value - minRpm) / (maxRpm - minRpm)

def getFuelColor(fuel):
    green = (10, 245, 10)
    red = (245, 10, 10)
    color = [int(green[i] * fuel + red[i] * (1 - fuel)) for i in range(3)]
    return tuple(color)