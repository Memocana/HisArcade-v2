#PacMan
#copyright: Mehmet Can Alaca
#Hisar Schools
import time
import pygame
from pygame.locals import *
from sys import exit
import math
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(2,GPIO.IN)# Kirmizi
GPIO.setup(3,GPIO.IN)#	Yesil
GPIO.setup(4,GPIO.IN)# Mavi
GPIO.setup(17,GPIO.IN)# Sari
GPIO.setup(27,GPIO.IN)# Yukari
GPIO.setup(22,GPIO.IN)# Sol
GPIO.setup(10,GPIO.IN)# A;a[i
GPIO.setup(9,GPIO.IN)# Sa[
GPIO.setup(11,GPIO.IN)# Yok

pygame.init()
screen=pygame.display.set_mode((1024,718),pygame.FULLSCREEN)
pygame.display.set_caption("PacMan!")
pygame.font.init()

#Initialize Back Ground
back = pygame.Surface((1024,718))
background = back.convert()
background.fill((0,0,0))

# Initialize Images
myimage = pygame.image.load('PacMan/pacman.png')
scared = pygame.image.load('PacMan/scared.png')
eyes = pygame.image.load('PacMan/eyes.png')
gameOverImage = pygame.image.load('PacMan/gameover.png')
youwin = pygame.image.load('PacMan/youwin.png')

blinkyImages = [None, pygame.image.load('PacMan/blinky1.png'), pygame.image.load('PacMan/blinky2.png'), pygame.image.load('PacMan/blinky-2.png'), pygame.image.load('PacMan/blinky-1.png')]
pinkyImages = [None, pygame.image.load('PacMan/pinky1.png'), pygame.image.load('PacMan/pinky2.png'), pygame.image.load('PacMan/pinky-2.png'), pygame.image.load('PacMan/pinky-1.png')]
inkyImages = [None, pygame.image.load('PacMan/inky1.png'), pygame.image.load('PacMan/inky2.png'), pygame.image.load('PacMan/inky-2.png'), pygame.image.load('PacMan/inky-1.png')]
clydeImages = [None, pygame.image.load('PacMan/clyde1.png'), pygame.image.load('PacMan/clyde2.png'), pygame.image.load('PacMan/clyde-2.png'), pygame.image.load('PacMan/clyde-1.png')]

# Initialize In Game Variables
score = 0
ghost = 0
lives = 3
gameOver = False

grid = [[4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4], # Field for the game
        [4,3,2,2,2,2,2,2,2,4,4,2,2,2,2,2,2,2,3,4], # 0: Blank, 1: Mr. Pac, 2: Food, 3: Power Up!, 4: Wall, 5: Blinky, 6: Pinky, 7: Clyde, 8: Inky, 9: Spawner
        [4,2,4,4,2,4,4,4,2,4,4,2,4,4,4,2,4,4,2,4],
        [4,2,4,4,2,2,2,2,2,2,1,2,2,2,2,2,4,4,2,4],
        [4,2,2,2,2,4,2,4,4,4,4,4,4,2,4,2,2,2,2,4],
        [4,4,4,4,2,4,2,2,2,4,4,2,2,2,4,2,4,4,4,4],
        [0,0,0,4,2,4,4,4,2,4,4,2,4,4,4,2,4,0,0,0],
        [0,0,0,4,2,4,2,2,2,2,2,2,2,2,4,2,4,0,0,0],
        [4,4,4,4,2,4,2,4,4,9,9,4,4,2,4,2,4,4,4,4],
        [2,5,2,2,2,2,2,4,0,0,0,0,4,2,2,2,2,2,6,2],
        [4,4,4,4,2,4,2,4,4,4,4,4,4,2,4,2,4,4,4,4],
        [0,0,0,4,2,4,2,2,2,2,2,2,2,2,4,2,4,0,0,0],
        [0,0,0,4,2,4,2,4,4,4,4,4,4,2,4,2,4,0,0,0],
        [4,4,4,4,2,2,2,2,2,4,4,2,2,2,2,2,4,4,4,4],
        [4,2,2,2,2,4,4,4,2,4,4,2,4,4,4,2,2,2,2,4],
        [4,2,4,4,7,2,2,2,2,2,2,2,2,2,2,8,4,4,2,4],
        [4,2,4,4,2,4,2,4,4,4,4,4,4,2,4,2,4,4,2,4],
        [4,2,4,4,2,4,2,2,2,4,4,2,2,2,4,2,4,4,2,4],
        [4,3,2,2,2,4,4,4,2,2,2,2,4,4,4,2,2,2,3,4],
        [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4]]
#GPIO connections
pins = [K_RIGHT, K_LEFT, K_UP, K_DOWN, K_d, K_a, K_w, K_s]

class Pac:
	def __init__(self,x,y,direction):
		self.x=x # 10
		self.y=y # 4
		self.direction=direction
		self.open = True
		self.images = [pygame.image.load('PacMan/pacman2.png'), myimage, pygame.transform.rotate(myimage,-90), pygame.transform.rotate(myimage, 90), pygame.transform.rotate(myimage,180)]

	def turns(self): # Checks buttons
		for event in pygame.event.get():
			if event.type == QUIT:
				exit()
			if event.type == KEYDOWN:
				if event.key == K_q:
					exit()
		print(GPIO.input(27)),
		print(GPIO.input(22)),
		print(GPIO.input(10)),  
		print(GPIO.input(9))   
		if GPIO.input(9):
			if self.movable(1):
				self.direction = 1
		elif not GPIO.input(22):
			if self.movable(-1):
				self.direction = -1
		elif not GPIO.input(10):  # Assa
			if self.movable(2):
				self.direction = 2
		elif GPIO.input(27):
			if self.movable(-2):
				self.direction = -2  
	def move(self): # Moves the Ghost a step on his choosen direction
		global score
		global ghost
		if self.direction % 2 == 1:
			if grid[self.y][(self.x+self.direction)] < 4:
				self.x += self.direction
				if grid[self.y][self.x] == 2:
					score += 1
				elif grid[self.y][self.x] == 3:
					score += 5 #invinciblity shizz
					ghost = 15
				grid[self.y][(self.x-self.direction)] = 0
				grid[self.y][self.x] = 1
			elif grid[self.y][(self.x+self.direction)] < 9:
				gameOver = True
		elif self.direction % 2 == 0:
			if grid[self.y+self.direction/2][self.x] < 4:
				self.y += self.direction/2
				if grid[self.y][self.x] == 2:
					score += 1
				elif grid[self.y][self.x] == 3:
					score += 5 #invinciblity shizz
					ghost = 15
				grid[self.y-self.direction/2][self.x] = 0
				grid[self.y][self.x] = 1
			elif grid[self.y+self.direction/2][self.x] < 9:
				gameOver = True

		if self.x == 19:
			self.x = -1
		elif self.x == -1:
			self.x = 19

	def movable(self, look): # Checks if the desired location is available to move
		if look % 2 == 1:
			return grid[self.y][self.x+look] < 4
		return grid[self.y+look / 2][self.x] < 4

	def modifyImage(self): # Modify Ghost costume by its direction.
		global myimage
		if self.open:
			myimage = self.images[self.direction]
		else:
			myimage = self.images[0]
		self.open = not self.open

class Ghosts: # Default Blinky behaviour, follows pacman where ever he goes
	def __init__(self, x, y, direction, images, name):
		self.x = x
		self.y = y
		self.direction = direction
		self.replacement = 2
		self.name = name
		self.mode = True
		self.fail = 0
		self.dead = False
		self.images = images
		self.image = self.images[direction]

	def checkAlive(self): # Checks collision with PacMan in Scared Mode
		if not self.mode and (grid[self.y][self.x] == 1 or self.replacement == 1) :
			self.dead = True

	def moveFront(self): # Moves the Ghost a step on his choosen direction
		global gameOver
		self.modifyImage()
		if self.direction % 2 == 1: # Make one step (Odds: Left, Right; Evens: Up, Down)
			self.x += self.direction
			if (self.replacement < 4 and self.replacement > 1) or self.replacement == 0:
				grid[self.y][(self.x-self.direction)] = self.replacement
			else:
				grid[self.y][(self.x-self.direction) ] = 2
		elif self.direction % 2 == 0:
			self.y += self.direction/2
			if (self.replacement < 4 and self.replacement > 1) or self.replacement == 0:
				grid[self.y-self.direction/2][self.x] = self.replacement
			else:
				grid[self.y-self.direction/2][self.x] = 2
		self.replacement = grid[self.y][self.x]

		if grid[self.y+1][self.x] == 9: # Respawn from Eye to Ghost
			self.dead = False
			
		if self.replacement == 1 and self.mode and not self.dead: # Checks collision with PacMan in Regular Mode
			self.replacement = 2
			gameOver = True

		if self.dead: #Image in current tile
			grid[self.y][self.x] = -2
		elif self.mode:
			grid[self.y][self.x] = self.name
		else:
			grid[self.y][self.x] = -1
			
		if self.x == 19: #Wrap
			self.x = -1
		elif self.x == -1:
			self.x = 19

	def route(self,target): #Find ideal route by calculating distances from each available move.
		counter = 0
		minDistance = -1
		idealDirection = 0
		for i in self.directionsAvailable():
			dist = 0
			directionToMove = 0
			if i == "1":
				if counter % 2 == 0: # Distance calculation according to possible moves
					dist = self.calculateRoute(self.x - (counter - 1), self.y, target)
					directionToMove = -(counter - 1)
				else:
					dist = self.calculateRoute(self.x, self.y - (counter - 2), target)
					directionToMove = -2 * (counter - 2)
			if directionToMove != 0 and (dist < minDistance or minDistance == -1) and (target != "run"): # Get min on any target
				minDistance = dist
				idealDirection = directionToMove
			elif directionToMove != 0 and dist > minDistance and target == "run": # Get max if running from Mr. Pac
				minDistance = dist
				idealDirection = directionToMove
			counter += 1
		if (idealDirection != 0):
			self.fail = 0
			return idealDirection
		self.fail += 1
		if (self.fail == 3):
			self.fail = 0
			return -self.direction
		return self.direction

	def directionsAvailable(self): # Returns a string of available directions of movement [0] = Right, [1] = Down, [2] = Left, [3] = Up
		directions = ""
		for i in range(4):
			if i % 2 == 0:
				if self.movable(1 - i) and self.direction != (i-1): #Left - Right
					directions += "1"
				else:
					directions += "0"
			else:
				if self.movable(4 - 2*i) and self.direction != (2*i - 4): #Down - Up
					directions += "1"
				else:
					directions += "0"
		return directions

	def calculateRoute(self, x, y, target): #Calculates distance to pacman if not dead. If its dead tries to find his way to home
		if (target != "home"):
			return math.hypot((pacman.x - x * 1.0),(pacman.y - y*1.0))
		return math.hypot((8 - x * 1.0),(8 - y*1.0))

	def movable(self, face): #Checks if the desired location is available to move
		if face % 2 == 1:
			return grid[self.y][(self.x+face)%20] < 4 and grid[self.y][(self.x+face)%20] >= 0
		return grid[self.y+face/ 2][self.x] < 4 and grid[self.y+face/ 2][self.x] >= 0

	def move(self): #Choses movement location according to current status and modify direction accordingly
		if self.dead:
			self.direction = self.route("home")
		elif self.mode:
			self.direction = self.route("pacman")
		else:
			self.direction = self.route("run")
		if self.movable(self.direction):
			self.moveFront()

	def modifyImage(self): # Modify Ghost costume by its direction.
		self.image = self.images[self.direction]

class Pinky(Ghosts): #Pinky predicts the movement of Pacman, She is always exactly 4 tiles ahead of him.

	def calculateRoute(self, x, y, target): # Calculates route to 4 steps ahead of pacman
		if pacman.direction %2 == 1:
			return math.hypot((pacman.x + pacman.direction * 4 - x * 1.0),(pacman.y  - y*1.0))
		return math.hypot((pacman.x  - x * 1.0),(pacman.y + pacman.direction * -2 - y*1.0))

class Clyde(Ghosts): # Clyde is a bit stupid, poor Clyde. He acts like Blinky when he is away from Mr. Pac but moves back to his corner if he is closer than 5 blocks 

	def move(self): # Chooses between moving to the corner or moving towards pac
		if not self.mode or self.dead or self.calculateRoute(self.x, self.y, "pacman") > 5:
			Ghosts.move(self)
		else:
			self.direction = self.route("corner")
			if self.movable(self.direction):
				self.moveFront()
		
	def calculateRoute(self, x, y, target): #Calculates distance to bottom left if target is the corner if not imitates Blinky
		if (target != "corner"):
			return Ghosts.calculateRoute(self, x, y, target)
		return math.hypot((x * 1.0),(20 - y*1.0))

class Inky(Ghosts): # Currently a Blinky clone, will face the direction blinky is facing
	def __init__(self,x,y,direction,image,name):
		Ghosts.__init__(self,x,y,direction,image,name) #Missing stuff here

#________________________________________________________________
#main game methods:
def modifyGrid(): # Creates and fills in the game area
	screen.blit(background,(0,0)) 
	pygame.draw.rect(screen,(255,255,255),Rect(192,39,640,640),3) #draws outer frame
	for x in xrange(20):
		for y in xrange(20):
			if (grid[y][x] == 1):	# Mr. Pac
				screen.blit(myimage, Rect(192+x*32+2,39+y*32+2,28,28))
			elif (grid[y][x] == 2):	# Food
				pygame.draw.circle(screen,(243, 180, 147),(192+x*32+16, 39+y*32+16),3)
			elif (grid[y][x] == 3):	# Power Up
				pygame.draw.circle(screen,(102, 40, 40),(192+x*32+16, 39+y*32+16),10)
			elif (grid[y][x] == 4): # Wall
				pygame.draw.rect(screen,(31, 68, 245),Rect(192+x*32,39+y*32,32,32),3)
			elif (grid[y][x] == 9): # Respawn
				pygame.draw.rect(screen,(25, 25, 25),Rect(192+x*32,39+y*32,32,32),3)
			elif (grid[y][x] >= 5): # Ghosts
				screen.blit(ghosts[grid[y][x] - 5].image, Rect(190+x*32+2,38+y*32+2,28,28))
			elif (grid[y][x] == -1): # Ghosts Scared
				screen.blit(scared, Rect(190+x*32+2,38+y*32+2,28,28))
			elif (grid[y][x] == -2): # Ghosts eaten by Mr. Pac
				screen.blit(eyes, Rect(190+x*32+2,38+y*32+2,28,28))
	for i in range(lives): #Shows how many lives the player has
		screen.blit(myimage, Rect(20 + 30*i,20,28,28))

def resetGame(): # Readies game for re-play, resets characters
	global ghosts

	grid[pacman.y][pacman.x] = 0

	for i in ghosts:
		grid[i.y][i.x] = i.replacement

	pacman.x, pacman.y = 10, 3
	pacman.direction = 1

	ghosts = [Ghosts(1,9,1, blinkyImages, 5), Pinky(18,9,-1, pinkyImages, 6), Clyde(4,15,-2, clydeImages, 7), Inky(15,15,-2, inkyImages, 8)]

def isGridEmpty(): #Checks if any food is left on the field 
	for i in grid:
		if i.count(2) > 0:
			return True
	return False
	
#________________________________________________________________________________
#initialization: clock and characters

clock = pygame.time.Clock()
initial_time=time.time()
old_time=0
pacman = Pac(10,3,1)#10,3

ghosts = [Ghosts(1,9,1, blinkyImages, 5), Pinky(18,9,-1, pinkyImages, 6), Clyde(4,15,-2, clydeImages, 7), Inky(15,15,-2, inkyImages, 8)]

modifyGrid()

while True:
    if lives > 0 and isGridEmpty(): #Checks if player still has lives or if and more food is left on the field.
        multiplier=8.5 #must be odd
        current_time=int((time.time()-initial_time)*multiplier)
        if current_time  > old_time:
        	if current_time % 2 == 0:
        		pacman.turns()
   	       		pacman.modifyImage()
   	       		pacman.move()
   	       		for i in ghosts:
   	       			i.checkAlive()

   	       	if current_time % 3 == 0:
   	       		for i in ghosts:
   	       			i.mode = (ghost == 0)
   	       			i.move()
   	       		if ghost != 0:
   	       			ghost -= 1

        	modifyGrid()
        	old_time=current_time
        	if gameOver:
        		resetGame()
        		lives -= 1
        		gameOver = False
    else:
    	multiplier=3 #must be odd
        current_time=int((time.time()-initial_time)*multiplier)
        modifyGrid()
        pacman.turns()
        if current_time % 2 == 0:
        	if lives == 0:
        		screen.blit(gameOverImage, (192,220))
        	elif not isGridEmpty():
        		screen.blit(youwin, (192,220))

    pygame.display.update()

    

            
    
