import pygame
import time
import math
from DataCollection.canbusTest import CanBusDataCollector
from DataCollection.misc import MiscDataCollector
from functions.helpers import *
from functions.speedGauge import *

def mainLoop():
    canBusDataCollector = CanBusDataCollector()
    miscDataCollector = MiscDataCollector()
    canBusDataCollector.startUpdateThread(frequency=60.0)
    miscDataCollector.startUpdateThread(frequency=60.0)

    # Colors
    BLACK = (10, 10, 10)
    WHITE = (245, 245, 245)
    RED = (245, 10, 10)
    GREEN = (10, 245, 10)


    # Positions
    CENTER = (1920, 550)
    SPEED_GAUGE = (1920, 550)
    SPEED_TEXT = (1920, 625)

    RPM_GAUGE = (3200, 550)
    RPM_TEXT = (3200, 625)

    FUEL_GAUGE = (200, 575)
    FUEL_SLIDER_START = (135, 235)
    FUEL_SLIDER_MAX_SIZE = (125, 810)


    textDistance = 380
    TPS_TEXT = (400, 1050)
    IAT_TEXT = (TPS_TEXT[0] + textDistance,1050)
    V_TEXT = (TPS_TEXT[0] + (textDistance * 2), 1050)
    MAP_TEXT = (TPS_TEXT[0] + (textDistance * 3), 1050)

    
    pygame.init()
    screen = pygame.display.set_mode((3840, 1100))
    staticSurface = pygame.Surface((3840, 1100))
    pygame.display.set_caption("Car Digital Dashboard")
    clock = pygame.time.Clock()

    # Load images
    images = {}
    images["speedGauge"] = pygame.image.load("sprites/SpeedGauge.png")
    images["rpmGauge"] = pygame.image.load("sprites/RpmGauge.png")
    images["fuelGauge"] = pygame.image.load("sprites/FuelGauge.png")
    images["tpsFrame"] = pygame.image.load("sprites/TPSFrame.png")
    images["iatFrame"] = pygame.image.load("sprites/IATFrame.png")
    images["vFrame"] = pygame.image.load("sprites/VFrame.png")
    images["mapFrame"] = pygame.image.load("sprites/MAPFrame.png")

    # Draw static elements
    staticSurface.blit(images["speedGauge"], center(images["speedGauge"], SPEED_GAUGE))
    staticSurface.blit(images["rpmGauge"], center(images["rpmGauge"], RPM_GAUGE))
    staticSurface.blit(images["fuelGauge"], center(images["fuelGauge"], FUEL_GAUGE))

    staticSurface.blit(images["tpsFrame"], center(images["tpsFrame"], TPS_TEXT))
    staticSurface.blit(images["iatFrame"], center(images["iatFrame"], IAT_TEXT))
    staticSurface.blit(images["vFrame"], center(images["vFrame"], V_TEXT))
    staticSurface.blit(images["mapFrame"], center(images["mapFrame"], MAP_TEXT))

    # Initialize custom font
    font90 = pygame.font.Font("fonts/orbitron.ttf", 90)
    font72 = pygame.font.Font("fonts/orbitron.ttf", 72)
    font60 = pygame.font.Font("fonts/orbitron.ttf", 60)
    
    # Variables
    fpsCounter = 0
    FPS_PRINT_FREQUENCY = 60
    staticSurfaceDrawn = False
    revSoftLimit = 6500
    revHardLimit = 7000

    lastColorChange = time.time()
    blinkInterval = 0.5

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                canBusDataCollector.stopUpdateThread()
                miscDataCollector.stopUpdateThread()
                pygame.quit()
                return
        
        rectList = []

        #Reset screen
        screen.blit(staticSurface, (0, 0))
                
        miscData = miscDataCollector.getData()
        speed = miscData["KMH"]
        fuel = miscData["FUEL"]

        canData = canBusDataCollector.getData()
        rpm = canData["RPM"]
        tps = canData["TPS"]
        iat = canData["IAT"]
        v = canData["V"]
        map = canData["MAP"]
        
        # Render speed text
        speedText = font90.render(str(speed), True, WHITE)
        speedTextRect = speedText.get_rect(center=SPEED_TEXT)
        screen.blit(speedText, speedTextRect)
        rectList.append(expandRect(speedTextRect, 20))

        # Render Needle
        speedAngle = mapSpeedToAngle(speed)
        speedNeedle = drawNeedle(screen, speedAngle, 80, SPEED_GAUGE[0], SPEED_GAUGE[1], 380)
        rectList.append(speedNeedle)

        # Render RPM text
        rpmTextColor = WHITE
        currentTime = time.time()
        
        if rpm > revSoftLimit:
            rpmTextColor = RED

        if rpm > revHardLimit:
            if currentTime - lastColorChange > blinkInterval:
                lastColorChange = currentTime
                rpmTextColor = WHITE if rpmTextColor == RED else RED

        rpmText = font72.render(str(rpm), True, rpmTextColor)
        rpmTextRect = rpmText.get_rect(center=RPM_TEXT)
        screen.blit(rpmText, rpmTextRect)
        rectList.append(expandRect(rpmTextRect, 20))

        # Render RPM Needle
        rpmAngle = mapRpmToAngle(rpm)
        rpmNeedle = drawNeedle(screen, rpmAngle, 60, RPM_GAUGE[0], RPM_GAUGE[1], 290)
        rectList.append(rpmNeedle)

        # Render FUEL GAUGE
        fuelRect = int(fuel * FUEL_SLIDER_MAX_SIZE[1])
        fuelColor = getFuelColor(fuel)
        fuelRectStart = (FUEL_SLIDER_START[0], FUEL_SLIDER_START[1] + FUEL_SLIDER_MAX_SIZE[1] - fuelRect)
        fuelDrawnRect = pygame.draw.rect(screen, fuelColor, (*fuelRectStart, FUEL_SLIDER_MAX_SIZE[0], fuelRect))
        rectList.append(expandRect(fuelDrawnRect, 10))
        
        # Render data texts
        textMarginal = 20

        tpsTextColor = WHITE
        tpsText = formatNumber(tps, 1) + "%"
        tpsTextRect = drawText(screen, tpsText, font60, TPS_TEXT, tpsTextColor)
        rectList.append(expandRect(tpsTextRect, textMarginal))
    

        iatTextColor = WHITE
        iatText = formatNumber(iat, 1) + "°C"
        iatTextRect = drawText(screen, iatText, font60, IAT_TEXT, iatTextColor)
        rectList.append(expandRect(iatTextRect, textMarginal))

        vTextColor = WHITE
        vText = formatNumber(v, 2) + "V"
        vTextRect = drawText(screen, vText, font60, V_TEXT, vTextColor)
        rectList.append(expandRect(vTextRect, textMarginal))

        mapTextColor = WHITE
        mapText = formatNumber(map, 1) + "kpa"
        mapTextRect = drawText(screen, mapText, font60, MAP_TEXT, mapTextColor)
        rectList.append(expandRect(mapTextRect, textMarginal))


        



        if not staticSurfaceDrawn:
            pygame.display.update()
            staticSurfaceDrawn = True
        else:
            pygame.display.update(rectList)

        # Print FPS in console
        if fpsCounter % FPS_PRINT_FREQUENCY == 0:
            fps = clock.get_fps()
            print(f"FPS: {fps}")
        fpsCounter += 1

        clock.tick(60)

if __name__ == "__main__":
    mainLoop()