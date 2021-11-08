import os
import pygame

class sprite():
    def __init__(self,imageFrames,x,y):
        self.imageFrames = imageFrames
        self.numFrames   = len(self.imageFrames)
        self.framePos    = 0
        self.x           = x
        self.y           = y
        self.w           = self.imageFrames[0].get_rect().w
        self.h           = self.imageFrames[0].get_rect().h
        self.vx          = 0
        self.vy          = 0
        self.frameTime   = 0

    def animate(self,gui,camera, interval=0.5):
        """
        animages image every interval (in seconds)
        once image reaches end, it resets to first image
        """
        
        # incremented timer
        self.frameTime += gui.dt/1000
        
        # increment frame when interval reached
        if(self.frameTime>=interval):
            self.framePos  +=1
            self.frameTime  = 0
        
        # wrap image around
        if(self.framePos>=self.numFrames): 
            self.framePos=0
        

        gui.screen.blit(self.imageFrames[self.framePos],(self.x-camera.x,self.y-camera.y))


def drawImage(screen,image,pos,trim=False):
    if(trim!=False):
        screen.blit(image,pos,trim)
    else:
        screen.blit(image,pos)

def importFiles(sName,numLetters=3,tDir  = 'sprites/players/'):
    tDir = tDir
    spriteList = [x for x in os.listdir(tDir) if x[:numLetters] == sName]
    spriteList = [pygame.image.load(tDir + x) for x in spriteList]


    return(spriteList)

def impFilesL(sName,tDir = 'pics/assets/mechBox/'):
    """
    Give the example of the first file i.e. bob1.jpg and it will import the rest
    """
    tDir = tDir
    affix       = '.' + str(sName.split('.')[-1])
    prefix      = str(sName.split('.')[0])[:-1]
    numLetters  = len(sName.split(affix)[0])
    numbers     = sorted([int("".join(filter(str.isdigit, x))) for x in os.listdir(tDir) if (prefix in x) and (affix in x)])
    spriteList  = [prefix + str(x) + affix for x in numbers]
    if(len(spriteList) < 1):
        print('spritelist not populated for ' + str(sName))
        exit()
    try:
        spriteList  = [pygame.image.load(tDir + x) for x in spriteList]
    except:
        print('Files can not be found for ' + str(sName))
        exit()
    return(spriteList)



class fitbaObject():
    """
    takes in sprite classs from utils
    """
    def __init__(self,football):
        self.sprite  = football
        self.x       = self.sprite.x
        self.y       = self.sprite.y
        self.w       = self.sprite.w
        self.h       = self.sprite.h
        self.kick    = None
        self.kicked  = False
        self.kickSpd = 10
    
    def kickBall(self,kickDirection,inc=2):
        """
        self.kick is the direction, it needs resetting at the end
        """
        
        #print('self.kicked ' + str(self.kicked))
        #print('self.kick ' + str(self.kick))
        #print('kickDirection ' + str(kickDirection))
        #print('kickSpd ' + str(self.kickSpd))
        #print(' ')


        if(self.kicked):
            if(kickDirection=='down'): 
                self.y+=self.kickSpd
            if(kickDirection=='up'): 
                self.y-=self.kickSpd
            if(kickDirection=='left'): 
                self.x-=self.kickSpd
            if(kickDirection=='right'): 
                self.x+=self.kickSpd

            self.kickSpd -=1
            if(self.kickSpd<0.5):
                self.kicked  = False
                self.kickSpd = 10
                self.kick=None
    


    def updateSprite(self,gui,camera):

        self.sprite.x,self.sprite.y = self.x,self.y
        self.sprite.animate(gui,camera)

        if(self.kick!=None): self.kicked = True 
        
        self.kickBall(self.kick)
