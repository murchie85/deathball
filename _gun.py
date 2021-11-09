from _utils                 import *

class _bullet():
	def __init__(self,x,y,v,muzzle,image,impact,direction):
		self.x          = x
		self.y          = y
		self.vx         = v
		self.vy         = v
		self.muzz       = muzzle
		self.image      = image
		self.impact     = impact
		self.state      = None
		self.mc         = 0
		self.direction  = direction

		# angle bullet
		angle = 0
		if(self.direction=='u'): angle=90
		if(self.direction=='d'): angle=270
		if(self.direction=='r'): angle=0
		if(self.direction=='l'): angle=180
		self.image = pygame.transform.rotate(self.image, angle)
		self.muzzle = []
		for m in self.muzz: self.muzzle.append(pygame.transform.rotate(m, angle))
		self.impactS = []
		for i in self.impact: self.impactS.append(pygame.transform.rotate(i, angle))


	def fire(self,gui,camera):

		# -----muzzle flash

		if(self.state==None):
			drawImage(gui.screen,self.muzzle[self.mc],(self.x-camera.x,self.y-camera.y))
			self.mc+=1
			if(self.mc>= len(self.muzzle)):
				self.state='firing'

		# ------Firing
		if(self.state=='firing'):
			if(self.direction=='u'):
				self.y -= self.vy
			if(self.direction=='d'):
				self.y += self.vy
			if(self.direction=='l'):
				self.x -= self.vx
			if(self.direction=='r'):
				self.x += self.vx
			# diagonals
			if(self.direction=='ur'):
				self.y -= self.vy
				self.x += self.vx
			if(self.direction=='ul'):
				self.y -= self.vy
				self.x -= self.vx
			if(self.direction=='dr'):
				self.y += self.vy
				self.x += self.vx
			if(self.direction=='dl'):
				self.y += self.vy
				self.x -= self.vx
			




			drawImage(gui.screen,self.image,(self.x-camera.x,self.y-camera.y))




class pgun():
	def __init__(self):
		self.image       = impFilesL('pBullets1.png',tDir='sprites/bullets/')
		self.x           = None
		self.y           = None
		self.direction   = None
		self.fired       = False
		self.created     = False
		self.timeCreated = None
		self.bullets     = []


	def shoot(self,x,y,direction,gui,shoot,camera):
		
		# Cyclic Firing (bullets need init only once)
		if(self.fired==False and shoot):
			self.fired       = True
			self.timeCreated = gui.gameElapsed
			self.bullets.append(_bullet(x,y,25,self.image[:2],self.image[2],self.image[2:],direction))
			self.bullets = [x for x in self.bullets if x!=None]


		# Clean up bullets
		for i in range(0,len(self.bullets)):
			try:
				if(self.bullets[i]!= None and ((self.bullets[i].x>3000) or (self.bullets[i].x<-3000) or (self.bullets[i].y>3000) or (self.bullets[i].y<-3000))): 
					del self.bullets[i]
			except:
				pass

		# Fire bullets
		for i in range(0,len(self.bullets)): self.bullets[i].fire(gui,camera)
			
		# Reseting to create another
		if((self.fired) and (gui.gameElapsed-self.timeCreated>0.2)):
			self.fired       =False
			self.timeCreated = None
