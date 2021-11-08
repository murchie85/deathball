import pygame
import os
import time
import math
import random
import json
import os
import os, sys


from _gui                   import *
from _gameState             import *
from _input                 import *
from _utils                 import *
from _player                import *


#----------------------------------------
"""
Reusable classes
GUI- it contains width,height,font and userinput








"""
#----------------------------------------

# -----------VARIABLES & FLAGS

white          = (255,255,255)
green          = (0,255,0)
blue           = (176,224,230)
FPS            = 90
width, height  = 1280,720
themeColour    = (128,0,0)
time = 0


# ---------------PYGAME

pygame.init()
pygame.display.set_caption("Fitba")
clock          = pygame.time.Clock()
nextFrame      = pygame.time.get_ticks()
screen         = pygame.display.set_mode((width,height),pygame.DOUBLEBUF)
#phoneScreen    = pygame.display.set_mode((405,544),pygame.DOUBLEBUF)
pygame.time.set_timer(pygame.USEREVENT, 20)

font        = pygame.font.Font('fonts/nokiafc22.ttf', 32)



# ---------------CLASS OBJECTS
gui                   = gui(screen,width,height,font)
user_input            = userInputObject("","",(0.27,0.65,0.45,0.08), gui)
modifyInput           = manageInput()


# -----------game objects


class camera():
    def __init__(self, x, y):
        self.x      = x
        self.y      = y
        self.offx   = -gui.width/2
        self.offy   = -gui.height/2
        self.target = 'player'

camera = camera(gui.width/2,gui.height/2)

footballSpriteList     = impFilesL('ball1.png',tDir = 'sprites/ball/')
footballSprite         = sprite(footballSpriteList,gui.width/2,gui.height/2)
fitba                  = fitbaObject(footballSprite)

playerSSW            = impFilesL('proto1.png',tDir='sprites/players/mech/')
playerSprite         = playerSprite(playerSSW)
player               = playerObject(playerSprite,gui.width/2,gui.height/3,vx=5,vy=5)


snowField           = pygame.image.load('sprites/snowFieldBig.png')
field               = pygame.image.load('sprites/fieldBig.png')



# ****TurnDebug on/off***
gui.debugSwitch = False 

# ---------------setup finished

gui.itercount = 0
while gui.running:
    gui.itercount+=1

    screen.fill((10, 100, 10))
    drawImage(screen,snowField,(0-camera.x,0 -camera.y))
    
    gui.clicked = False
    # Reset the key each round
    user_input.returnedKey=''

    # Did the user click the window close button?
    for event in pygame.event.get():
        pos            = pygame.mouse.get_pos()
        if event.type == pygame.QUIT: gui.running = False
        if event.type == pygame.MOUSEBUTTONDOWN: gui.clicked  = True
        user_input     = modifyInput.manageButtons(event,user_input,gui)

    # Update GUI with dynamic vars
    gui.userInput  = user_input
    gui.mx, gui.my = pygame.mouse.get_pos()


    fitba.updateSprite(gui,camera)
    player.play_selected(gui,fitba,camera)
    
    # update camera
    if(camera.target=='player'):
        camera.x = player.x + camera.offx
        camera.y = player.y + camera.offy

    if(camera.target=='ball'):
        camera.x = fitba.x + camera.offx
        camera.y = fitba.y + camera.offy


        










    # Flip the display
    pygame.display.flip()
    # Tick
    gui.dt           = clock.tick(FPS)
    gui.gameElapsed += gui.dt/1000
    continue

# Done! Time to quit.
pygame.quit()