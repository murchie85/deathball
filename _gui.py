import pygame

class gui():
    def __init__(self,screen,width,height):
        self.screen       = screen
        self.width        = width
        self.height       = height
        self.font         = pygame.font.Font('fonts/nokiafc22.ttf', 32)


        self.gameState    = 'ingame'
        self.userInput    = None # Loaded at runtime
        self.running      = True
        self.dt           = 0
        self.gameElapsed  = 0
        self.debugSwitch  = False
        self.mx           = 0
        self.my           = 0


        self.white          = (255,255,255)
        self.green          = (0,255,0)
        self.blue           = (176,224,230)


    def debug(self,debugMessage):
        if(self.debugSwitch):
            print(debugMessage)



class camera():
    def __init__(self, x, y,gui):
        self.x      = x
        self.y      = y
        self.offx   = -gui.width/2
        self.offy   = -gui.height/2
        self.target = 'player'
