import pygame
from pygame.locals import *
import sys
import time
import random
import numpy as np

pygame.init()

screen = pygame.display.set_mode((720, 480))
pygame.display.set_caption("Girl vs Doggy")

background = pygame.image.load("background.jpg").convert()
background = pygame.transform.scale(background, (720, 480))
echo = pygame.image.load("echo.png").convert_alpha()
echo = pygame.transform.scale(echo, (50, 109))
poop = pygame.image.load("poop.png").convert_alpha()
poop = pygame.transform.scale(poop, (40, 40))
summer_left = pygame.image.load("summer_left.png").convert_alpha()
summer_left = pygame.transform.scale(summer_left, (75, 75))
summer_right = pygame.image.load("summer_right.png").convert_alpha()
summer_right = pygame.transform.scale(summer_right, (75, 75))
life = pygame.image.load("life.png").convert_alpha()
life = pygame.transform.scale(life, (30, 30))
lifebroken = pygame.image.load("lifebroken.png").convert_alpha()
lifebroken = pygame.transform.scale(lifebroken, (30, 30))
cat = pygame.image.load("cat.png").convert_alpha()
cat = pygame.transform.scale(cat, (50, 60))

echoXAxis = 335
echoYAxis = 360
poopXAxis = np.array([])
poopYAxis = np.array([])
catXAxis = np.array([])
catYAxis = np.array([])
catDeleteCounter = np.array([])
summerXAxis = 323
summerYAxis = 50
summerDirection = 1
targetSummerXAxis = random.randint(0,645)
poopCounter = random.randint(100,200)
catCounter = random.randint(500, 1000)
lifeCounter = 5
scoreCounter = 0
font = pygame.font.Font(None, 40)
lifeText = font.render("Girl's Life", True,(0, 0, 0))
scoreText = font.render("Score", True,(0, 0, 0))
hittingText = font.render("Hit Poop!!", True,(0, 0, 0))
catText = font.render("Meow~", True,(0, 0, 0))
messageHittingCounter = 0
messageHittingXAxis = 0
messageHittingYAXis = 0
messageCatCounter = 0
messageCatXAxis = 0
messageCatYAXis = 0

def drawCharactors():
    global messageHittingCounter
    global messageCatCounter
    screen.blit(background, (0, 0))

    if summerDirection == -1:
        screen.blit(summer_right, (summerXAxis, summerYAxis))
    elif summerDirection == 1:
        screen.blit(summer_left, (summerXAxis, summerYAxis))

    for i in range(len(poopXAxis)):
        screen.blit(poop, (poopXAxis[i], poopYAxis[i]))

    for i in range(len(catXAxis)):
        screen.blit(cat, (catXAxis[i], catYAxis[i]))

    screen.blit(echo, (echoXAxis, echoYAxis))

    screen.blit(lifeText, (10, 12))
    for i in range(5):
        if i < lifeCounter:
            screen.blit(life, (170+(35*i), 10))
        else:
            screen.blit(lifebroken, (170+(35*i), 10))

    screen.blit(scoreText, (550, 12))
    scoreDisplay = font.render(str(scoreCounter), True,(0, 0, 0))
    screen.blit(scoreDisplay, (630 , 12))

    if messageHittingCounter > 0:
        messageHittingCounter -= 1
        screen.blit(hittingText, (messageHittingXAxis , messageHittingYAXis))
    if messageCatCounter > 0:
        messageCatCounter -= 1
        screen.blit(catText, (messageCatXAxis , messageCatYAXis))

def moveEcho(moveDistance):
    global echoXAxis
    echoXAxis = echoXAxis + moveDistance
    if echoXAxis > 650:
        echoXAxis = 650
    elif echoXAxis < 20:
        echoXAxis = 20

    for i in range(len(catXAxis)):
        if (echoXAxis > catXAxis[i]) and (echoXAxis-catXAxis[i]) < 50:
            echoXAxis = catXAxis[i] + 50
        elif (echoXAxis < catXAxis[i]) and (catXAxis[i]-echoXAxis) < 50:
            echoXAxis = catXAxis[i] - 50

def movePoop():
    global poopCounter
    global poopXAxis
    global poopYAxis
    global scoreCounter
    poopCounter -= 1
    if poopCounter == 0:
        poopXAxis = np.append(poopXAxis, summerXAxis + 37 - 20)
        poopYAxis = np.append(poopYAxis, summerYAxis + 75)
        poopCounter = random.randint(50,100)

    poopYAxis += 1
    for i in range(len(poopXAxis)):
        if poopYAxis[i] == 440:
            poopXAxis = np.delete(poopXAxis, i)
            poopYAxis = np.delete(poopYAxis, i)
            scoreCounter += 100
            break

def moveSummer():
    global summerDirection
    global summerXAxis
    global targetSummerXAxis
    if abs(summerXAxis - targetSummerXAxis) < 2:
        targetSummerXAxis = random.randint(0,645)

    if summerXAxis - targetSummerXAxis > 0:
        summerXAxis = summerXAxis - 2
        summerDirection = 1
    elif summerXAxis - targetSummerXAxis < 0:
        summerXAxis = summerXAxis + 2
        summerDirection = -1


def judgeHitting():
    #echo size = 50 * 109, poop size = 40 * 40
    global poopXAxis
    global poopYAxis
    global lifeCounter
    global messageHittingCounter
    global messageHittingXAxis
    global messageHittingYAXis

    for i in range(len(poopXAxis)):
        if (echoXAxis > poopXAxis[i]) and (echoXAxis - poopXAxis[i]) < 40 and (echoYAxis - poopYAxis[i]) < 40 :
            lifeCounter -= 1
            messageHittingCounter = 200
            messageHittingXAxis = poopXAxis[i]
            messageHittingYAXis = poopYAxis[i]
            poopXAxis = np.delete(poopXAxis, i)
            poopYAxis = np.delete(poopYAxis, i)
            break
        if (poopXAxis[i] > echoXAxis) and (poopXAxis[i] - echoXAxis) < 50 and (echoYAxis - poopYAxis[i]) < 40 :
            messageHittingCounter = 200
            messageHittingXAxis = poopXAxis[i]
            messageHittingYAXis = poopYAxis[i]
            poopXAxis = np.delete(poopXAxis, i)
            poopYAxis = np.delete(poopYAxis, i)
            lifeCounter -= 1
            break

def randomCat():
    global catCounter
    global catXAxis
    global catYAxis
    global catDeleteCounter
    global messageCatCounter
    global messageCatXAxis
    global messageCatYAXis

    catCounter -= 1
    if catCounter == 0:
        catxaxis = random.randint(0,670)
        catXAxis = np.append(catXAxis, catxaxis)
        catYAxis = np.append(catYAxis, 405)
        catDeleteCounter = np.append(catDeleteCounter, random.randint(1000,2000))
        catCounter = random.randint(500,1000)
        messageCatCounter = 100
        messageCatXAxis = catxaxis - 10
        messageCatYAXis = 380

    for i in range(len(catXAxis)):
        catDeleteCounter[i] -= 1
        if catDeleteCounter[i] == 0:
            catXAxis = np.delete(catXAxis, i)
            catYAxis = np.delete(catYAxis, i)
            catDeleteCounter = np.delete(catDeleteCounter, i)
            break

def ending():
    fontEnd = pygame.font.Font(None, 100)
    gameOverText = fontEnd.render("Game Over", True,(0, 0, 0))
    totalScoreText = fontEnd.render("Total Score : " + str(scoreCounter), True,(0, 0, 0))
    screen.blit(gameOverText, (150 , 150))
    screen.blit(totalScoreText, (70 , 250))

while(1):
    if lifeCounter != 0:
        moveSummer()
        movePoop()
        randomCat()
        drawCharactors()
        judgeHitting()
        pressedKey = pygame.key.get_pressed()
        if pressedKey[K_LEFT]:
            moveEcho(-1)
        if pressedKey[K_RIGHT]:
            moveEcho(1)
        pygame.display.update()
        time.sleep(0.005)
    else:
        drawCharactors()
        ending()
        pygame.display.update()
        time.sleep(0.005)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit(0)
