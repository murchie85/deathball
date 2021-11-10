import pygame
import os
import time
import math
import random
import json
import os
import os, sys


from _game                  import *
from _input                 import *
from _utils                 import *
from _player                import *
from _ball                  import *



# -----------VARIABLES & FLAGS
FPS            = 60
width, height  = 1280,720
themeColour    = (128,0,0)
time = 0


# ---------------PYGAME

pygame.init()
pygame.display.set_caption("Fitba")
clock          = pygame.time.Clock()
nextFrame      = pygame.time.get_ticks()
screen         = pygame.display.set_mode((width,height),pygame.DOUBLEBUF)
#pygame.time.set_timer(pygame.USEREVENT, 20)

# ---------------CLASS OBJECTS
game                  = game(screen,width,height)
user_input            = userInputObject("","",(0.27,0.65,0.45,0.08), game)
modifyInput           = manageInput()
camera                = camera(game.width/2,game.height/2,game)

# -----------game objects

footballSpriteList     = impFilesL('ball1.png',tDir = 'sprites/ball/')
footballSprite         = sprite(footballSpriteList,game.width/2,game.height/2)
fitba                  = fitbaObject(footballSprite)


protoSprite            = impFilesL('proto1.png',tDir='sprites/players/mech/')
squad                  = { 'capt':playerObject('capt',playerSprite(protoSprite),game.width/2,game.height/3,vx=5,vy=5),
                           'fwdr':playerObject('fwdr',playerSprite(protoSprite),0.6*game.width,0.2*game.height,vx=5,vy=5),
                           'fwdl':playerObject('fwdl',playerSprite(protoSprite),0.4*game.width,0.2*game.height,vx=5,vy=5),
                           'midr':playerObject('midr',playerSprite(protoSprite),0.6*game.width,0.5*game.height,vx=5,vy=5),
                           'midl':playerObject('midl',playerSprite(protoSprite),0.4*game.width,0.5*game.height,vx=5,vy=5),

                           }
squad['capt'].selected = True
selectable = ['capt','fwdr','fwdl','midr','midl']

statsBox            = statsBox(0,0,game.smallFont)


# -----Update game object
game.squad  = squad

# ****TurnDebug on/off***
game.debugSwitch = False 

# ---------------setup finished

game.itercount = 0
while game.running:
    game.itercount+=1

    screen.fill((0, 0, 0))
    drawImage(screen,game.snowField,(0-camera.x,0 -camera.y))
    
    game.clicked = False
    # Reset the key each round
    user_input.returnedKey=''

    # Did the user click the window close button?
    for event in pygame.event.get():
        pos            = pygame.mouse.get_pos()
        if event.type == pygame.QUIT: game.running = False
        if event.type == pygame.MOUSEBUTTONDOWN: game.clicked  = True
        user_input     = modifyInput.manageButtons(event,user_input,game)

    # Update game with dynamic vars
    game.userInput  = user_input
    game.mx, game.my = pygame.mouse.get_pos()

    # ------------------------------








    #Update Football 
    fitba.updateSprite(game,camera)



    # Iterate thru players
    for s in game.squad:
        member = game.squad[s]
        if(game.userInput.returnedKey=='y'): member.selected = not member.selected
        
        if(member.selected): 
            player = member
        else:
            member.autoPlay(game,fitba,camera)

    

    # Selected Player
    player.play_selected(game,fitba,camera)
 

     # display debug box
    statsBox.display(['Name ' + str(player.name),
                      'Health ' + str(player.health),
                      'Armour ' + str(player.armour),
                      'Carrying ' + str(player.carryBall),
                      'Facing ' + str(player.facing)],game)
        
   
    
    
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
    game.dt           = clock.tick(FPS)
    game.gameElapsed += game.dt/1000

# Done! Time to quit.
pygame.quit()