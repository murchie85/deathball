from _gun import * 





class playerObject():
    """
    takes in playersprite classs from utils
    """
    def __init__(self,playerSprite,x,y,vx,vy):
        self.sprite             = playerSprite
        self.x                  = x
        self.y                  = y
        self.vx                 = vx
        self.vy                 = vy
        self.ballpos            = []
        self.facing             = 'u'
        self.stationary         = True
        self.carryBall          = False
        self.pGun               = pgun()



    def dribble(self,carryBall,fitba,inRange,gui,bounce=1):
        
        # Ball follows player if true
        if(carryBall==True): fitba.x,fitba.y = self.x,self.y

        # Set ball direction if kicked
        if(gui.userInput.kick and carryBall==True):
            self.carryBall='kick'
            if(self.facing=='u'): fitba.kick  ='up'
            if(self.facing=='d'): fitba.kick  ='down'
            if(self.facing=='l'): fitba.kick  ='left'
            if(self.facing=='r'): fitba.kick  ='right'

            if(self.facing=='ur'): fitba.kick  ='ur'
            if(self.facing=='ul'): fitba.kick  ='ul'
            if(self.facing=='dr'): fitba.kick  ='dr'
            if(self.facing=='dl'): fitba.kick  ='dl'





        # After kicking and ball is out of sphere, reset
        if(self.carryBall=='kick' and inRange==False):
            self.carryBall=False

    
        

    def inRange(self,playerPos,otherObj):
        x,y,w,h = otherObj.x,otherObj.y,otherObj.w,otherObj.h
        px,py,pw,ph = playerPos[0],playerPos[1],self.sprite.w,self.sprite.h
        
        playerRightside    = px+pw
        playerLeftSide     = px-pw
        playerBottomSide   = py+1.5*ph
        playerTopSide      = py-0.5*ph
        if x > playerLeftSide and x < playerRightside:
            if y > playerTopSide and y < playerBottomSide:
                return(True)
        return(False)

    def collides(self,playerPos,otherObj):
        x,y,w,h = otherObj.x,otherObj.y,otherObj.w,otherObj.h
        px,py,pw,ph = playerPos[0],playerPos[1],self.sprite.w,self.sprite.h
        
        playerRightside    = px+0.5*pw
        playerLeftSide     = px-0.5*pw
        playerBottomSide   = py+ph
        playerTopSide      = py

        # get ball relative pos
        self.ballpos = []
        if(x>playerRightside): self.ballpos.append('l')
        if(x<playerLeftSide):  self.ballpos.append('r')
        if(y<playerTopSide):   self.ballpos.append('u')
        if(y>playerTopSide):   self.ballpos.append('d')

        # check if collides
        if x > playerLeftSide and x < playerRightside:
            if y > playerTopSide and y < playerBottomSide:
                return(True)
        return(False)

    def fireGun(self,gui,camera):
        # facing != userInput.dir because diagonals
        self.pGun.shoot(self.x,self.y, self.facing,gui,gui.userInput.fire,camera)
    
    def play_selected(self,gui,fitba,camera=None):

        #self.sprite.animate(gui,stop=True)
        self.stationary = (gui.userInput.up==False and gui.userInput.down==False and gui.userInput.left==False and gui.userInput.right==False)
        
        # Set Direction, set  velocity
        self.u,self.d,self.l,self.r = False,False,False,False
        # Manage Velocity
        if(gui.userInput.up):    
            self.y -= self.vy
            self.u = True
            self.facing = 'u'
        if(gui.userInput.down):  
            self.y += self.vy
            self.d = True
            self.facing = 'd'
        if(gui.userInput.left):  
            self.x -= self.vx
            self.l = True
            self.facing = 'l'
        if(gui.userInput.right): 
            self.x += self.vx
            self.r = True
            self.facing = 'r'

        if(gui.userInput.up and gui.userInput.left):    self.facing = 'ul'
        if(gui.userInput.up and gui.userInput.right):   self.facing = 'ur'
        if(gui.userInput.down and gui.userInput.left):  self.facing = 'dl'
        if(gui.userInput.down and gui.userInput.right): self.facing = 'dr'


        # -------check if colliding with ball
        colliding = self.collides((self.x,self.y),fitba)
        if(colliding and self.carryBall==False):
            self.carryBall = True
        
        inRange   = self.inRange((self.x,self.y),fitba)
        
        # ------ dribble ball
        self.dribble(self.carryBall,fitba,inRange,gui)

        self.fireGun(gui,camera)
        
        # -------update position
        self.updateSprite(gui)

        # ------Animate
        self.sprite.animate(gui,self.facing,camera,stop=self.stationary)

    def updateSprite(self,gui):
        self.sprite.x,self.sprite.y = self.x,self.y








class playerSprite():
    def __init__(self,imageFrames):
        self.imageFrames        = imageFrames
        
        self.downF              = self.imageFrames[:6]
        self.upF                = self.imageFrames[6:12]
        self.rightF             = self.imageFrames[12:18]
        self.leftF              = self.imageFrames[18:24]
        self.urF                = self.imageFrames[24:30]
        self.ulF                = self.imageFrames[30:36]
        self.dlF                = self.imageFrames[36:42]
        self.drF                = self.imageFrames[42:]


        self.liveFrames         = self.downF
        self.numFrames          = len(self.downF)

        self.framePos           = 0
        self.x                  = 0
        self.y                  = 0
        self.w                  = self.imageFrames[0].get_rect().w
        self.h                  = self.imageFrames[0].get_rect().h
        self.frameTime          = 0



        self.currentDirection   = None



    

    def getDirection(self,facing):

        direction = None
        if(facing=='u'): self.liveFrames = self.upF
        if(facing=='d'): self.liveFrames = self.downF
        if(facing=='l'): self.liveFrames = self.leftF
        if(facing=='r'): self.liveFrames = self.rightF
        if(facing=='ur'): self.liveFrames = self.urF
        if(facing=='ul'): self.liveFrames = self.ulF
        if(facing=='dr'): self.liveFrames = self.drF
        if(facing=='dl'): self.liveFrames = self.dlF
        


        direction = facing
        return(direction)




    def animate(self,gui,facing,camera,interval=0.2,stop=False):
        """
        animages image every interval (in seconds)
        once image reaches end, it resets to first image
        """

        # Update direction Frames
        direction = self.getDirection(facing)


        # --------change sprite templates
        if(self.currentDirection!=direction):
            self.currentDirection = direction
            self.framePos = 0
            self.numFrames = len(self.liveFrames)


        

        if(stop):
            gui.screen.blit(self.liveFrames[0],(self.x- camera.x,self.y- camera.y))
            return()
        

        #-----------animate
        # incremented timer
        self.frameTime += gui.dt/1000
        
        # increment frame when interval reached
        if(self.frameTime>=interval):
            self.framePos  +=1
            self.frameTime  = 0
        
        # wrap image around
        if(self.framePos>=self.numFrames): 
            self.framePos=0
        
        gui.screen.blit(self.liveFrames[self.framePos],(self.x - camera.x,self.y- camera.y))

