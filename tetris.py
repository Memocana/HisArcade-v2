#!/usr/bin/env python
#Hisar Tetris
#copyright: Cem Ersoz, Bensu Sicim
#Hisar Schools
import time
import pygame
from pygame.locals import *
from sys import exit
import random
import RPi.GPIO as GPIO
pygame.init()
#GPIO Pins Def
button1=4
button2=0
button3=1

sys.path.insert(0,"/home/pi/Desktop/HisArcade/pins")
import gamePins

gamePins.gameSetup()

scoreboard = gamePins.getScores("Tetris")

screen=pygame.display.set_mode((1024,718),pygame.FULLSCREEN)
pygame.display.set_caption("Hisar Tetris!")
#Creating 4 boxes and Background.
back = pygame.Surface((1024,718))
background = back.convert()
background.fill((0,0,0))
fontSmall = pygame.font.Font("Fonts/ARCADECLASSIC.TTF",30)
red, yellow, green, blue=(235,53,47),(235,230,45),(0,185,10),(73,170,235)
directTurn = fontSmall.render("turn", True,(255,255,255))
directDrop = fontSmall.render("drop", True,(255,255,255))
directLeft = fontSmall.render("left", True,(255,255,255))
directRight = fontSmall.render("right", True,(255,255,255))
directExit = fontSmall.render("exit", True,(255,255,255))
Grid = [[0 for x in xrange(20)]for x in xrange(10)]
left,down,right=1,2,3
Score=0
cShape=1
class box:
    def __init__(self,a,b):
        self.x=a
        self.y=b
    def setXY(self,a,b):
        self.x=a
        self.y=b
    def drawSelf(self,color):
        Grid[self.x][self.y]=color
    def eraseSelf(self):
        Grid[self.x][self.y]=0
    def canMoveUp(self):
        if self.y<1 or Grid[self.x][self.y-1]>0:
            return False
        else:
            return True
    def canMoveDown(self):
        return self.y<19 and Grid[self.x][self.y+1]==0
    def canMoveLeft(self):
        return self.x>0 and Grid[self.x-1][self.y]==0
    def canMoveRight(self):
        return self.x<9 and Grid[self.x+1][self.y]==0
    def canMoveTwoUp(self):
        return self.y>1 and self.canMoveUp() and Grid[self.x][self.y-2]==0
    def canMoveTwoDown(self):
        return self.y<18 and self.canMoveDown() and Grid[self.x][self.y+2]==0
    def canMoveTwoRight(self):
        return self.x<8 and self.canMoveRight() and Grid[self.x+2][self.y]==0
    def canMoveTwoLeft(self):
        return self.x>1 and self.canMoveLeft() and Grid[sel.x-2][self.y]==0
    def move(self,a): #1 for left, 2 for down, r for right
        if a==left:
            self.x-=1
        elif a==down:
            self.y+=1
        elif a==right:
            self.x+=1
class Square:
    def __init__(self,boxa,boxb,boxc,boxd):
        self.BoxA,self.BoxB,self.BoxC,self.BoxD=boxa,boxb,boxc,boxd
    def begin(self):
        self.BoxA.setXY(4,0)
        self.BoxB.setXY(5,0)
        self.BoxC.setXY(4,1)
        self.BoxD.setXY(5,1)
    def canMoveLeft(self):
        return self.BoxA.canMoveLeft() and self.BoxC.canMoveLeft()
    def canMoveRight(self):
        return self.BoxB.canMoveRight() and self.BoxD.canMoveRight()
    def canMoveDown(self):
        return self.BoxC.canMoveDown() and self.BoxD.canMoveDown()
class Line:
    def __init__(self,boxa,boxb,boxc,boxd):
        self.BoxA,self.BoxB,self.BoxC,self.BoxD=boxa,boxb,boxc,boxd
        self.state=1
    def begin(self):
        self.BoxA.setXY(3,0)
        self.BoxB.setXY(4,0)
        self.BoxC.setXY(5,0)
        self.BoxD.setXY(6,0)
        self.state=0
    def turn(self):
        if self.state==0 and self.BoxB.canMoveUp() and self.BoxB.canMoveTwoDown():
            self.BoxA.setXY(self.BoxB.x,self.BoxB.y-1)
            self.BoxC.setXY(self.BoxB.x,self.BoxB.y+1)
            self.BoxD.setXY(self.BoxB.x,self.BoxB.y+2)
            self.state=1
        elif self.state==1 and self.BoxB.canMoveLeft() and self.BoxC.canMoveRight() and self.BoxD.canMoveTwoRight() and self.BoxB.canMoveTwoRight() and self.BoxA.canMoveLeft():
            self.BoxA.setXY(self.BoxB.x-1,self.BoxB.y)
            self.BoxC.setXY(self.BoxB.x+1,self.BoxB.y)
            self.BoxD.setXY(self.BoxB.x+2,self.BoxB.y)
            self.state=0
    def canMoveLeft(self):
        if self.state==1:
            return self.BoxA.canMoveLeft() and self.BoxB.canMoveLeft() and self.BoxC.canMoveLeft() and self.BoxD.canMoveLeft()
        elif self.state==0:
            return self.BoxA.canMoveLeft()
    def canMoveRight(self):
        if self.state==1:
            return self.BoxA.canMoveRight() and self.BoxB.canMoveRight() and self.BoxC.canMoveRight() and self.BoxD.canMoveRight()
        elif self.state==0:
            return self.BoxD.canMoveRight()
    def canMoveDown(self):
        if self.state==0:
            return self.BoxA.canMoveDown() and self.BoxB.canMoveDown() and self.BoxC.canMoveDown() and self.BoxD.canMoveDown()
        elif self.state==1:
            return self.BoxD.canMoveDown()
class lShape:
    def __init__(self,boxa,boxb,boxc,boxd):
        self.BoxA,self.BoxB,self.BoxC,self.BoxD=boxa,boxb,boxc,boxd
        self.state=0
    def begin(self):
        self.BoxA.setXY(5,0)
        self.BoxB.setXY(5,1)
        self.BoxC.setXY(5,2)
        self.BoxD.setXY(6,2)
        self.state=0
    def turn(self):
        if self.state==0 and self.BoxA.canMoveLeft() and self.BoxA.canMoveRight() and self.BoxB.canMoveLeft():
            self.BoxB.setXY(self.BoxA.x+1,self.BoxA.y)
            self.BoxC.setXY(self.BoxA.x-1,self.BoxA.y+1)
            self.BoxD.setXY(self.BoxA.x-1,self.BoxA.y)
            self.state=1
        elif self.state==1 and self.BoxA.canMoveDown() and self.BoxA.canMoveTwoDown():
            self.BoxB.setXY(self.BoxA.x,self.BoxA.y+1)
            self.BoxC.setXY(self.BoxA.x,self.BoxA.y+2)
            self.state=2
        elif self.state==2 and self.BoxB.canMoveLeft() and self.BoxC.canMoveLeft() and self.BoxC.canMoveRight():
            self.BoxA.setXY(self.BoxC.x+1,self.BoxC.y-1)
            self.BoxD.setXY(self.BoxC.x+1,self.BoxC.y)
            self.BoxB.setXY(self.BoxC.x-1,self.BoxC.y)
            self.state=3
        elif self.state==3 and self.BoxA.canMoveLeft() and self.BoxC.canMoveTwoUp() and self.BoxC.canMoveUp():
            self.BoxA.setXY(self.BoxC.x,self.BoxC.y-2)
            self.BoxB.setXY(self.BoxC.x,self.BoxC.y-1)
            self.state=0
    def canMoveLeft(self):
        if self.state==0:
            return self.BoxA.canMoveLeft() and self.BoxC.canMoveLeft() and self.BoxB.canMoveLeft()
        if self.state==1:
            return self.BoxD.canMoveLeft() and self.BoxC.canMoveLeft()
        if self.state==2:
            return self.BoxD.canMoveLeft() and self.BoxC.canMoveLeft() and self.BoxB.canMoveLeft()
        if self.state==3:
            return self.BoxA.canMoveLeft() and self.BoxB.canMoveLeft()
    def canMoveRight(self):
        if self.state==0:
            return self.BoxB.canMoveRight() and self.BoxD.canMoveRight()and self.BoxA.canMoveRight()
        if self.state==1:
            return self.BoxB.canMoveRight() and self.BoxC.canMoveRight()
        if self.state==2:
            return self.BoxB.canMoveRight() and self.BoxC.canMoveRight()and self.BoxA.canMoveRight()
        if self.state==3:
            return self.BoxD.canMoveRight()and self.BoxA.canMoveRight()
    def canMoveDown(self):
        if self.state==0:
            return self.BoxC.canMoveDown() and self.BoxD.canMoveDown() 
        if self.state==1:
            return self.BoxC.canMoveDown() and self.BoxA.canMoveDown() and self.BoxB.canMoveDown()
        if self.state==2:
            return self.BoxC.canMoveDown() and self.BoxD.canMoveDown()
        if self.state==3:
            return self.BoxC.canMoveDown() and self.BoxD.canMoveDown() and self.BoxB.canMoveDown()
class tShape:
    def __init__(self,boxa,boxb,boxc,boxd):
        self.BoxA,self.BoxB,self.BoxC,self.BoxD=boxa,boxb,boxc,boxd
        self.state=0
    def begin(self):
        self.BoxA.setXY(5,0)
        self.BoxB.setXY(4,1)
        self.BoxC.setXY(5,1)
        self.BoxD.setXY(6,1)
        self.state=0
    def turn(self):
        if self.state==0 and self.BoxC.canMoveDown():
            self.BoxB.setXY(self.BoxC.x,self.BoxC.y+1)
            self.state=1
        elif self.state==1 and self.BoxC.canMoveLeft():
            self.BoxA.setXY(self.BoxC.x-1,self.BoxC.y)
            self.state=2
        elif self.state==2 and self.BoxC.canMoveUp():
            self.BoxD.setXY(self.BoxC.x,self.BoxC.y-1)
            self.state=3
        elif self.state==3 and self.BoxC.canMoveRight():
            self.BoxD.setXY(self.BoxC.x+1,self.BoxC.y)
            self.BoxB.setXY(self.BoxC.x-1,self.BoxC.y)
            self.BoxA.setXY(self.BoxC.x,self.BoxC.y-1)
            self.state=0
    def canMoveLeft(self):
        if self.state==0:
            return self.BoxA.canMoveLeft() and self.BoxB.canMoveLeft()
        if self.state==1:
            return self.BoxA.canMoveLeft() and self.BoxC.canMoveLeft() and self.BoxB.canMoveLeft()
        if self.state==2:
            return self.BoxA.canMoveLeft() and self.BoxB.canMoveLeft()
        if self.state==3:
            return self.BoxA.canMoveLeft() and self.BoxB.canMoveLeft() and self.BoxD.canMoveLeft()
    def canMoveRight(self):
        if self.state==0:
            return self.BoxD.canMoveRight()and self.BoxA.canMoveRight()
        if self.state==1:
            return self.BoxB.canMoveRight() and self.BoxA.canMoveRight() and self.BoxD.canMoveRight()
        if self.state==2:
            return self.BoxB.canMoveRight() and self.BoxD.canMoveRight()
        if self.state==3:
            return self.BoxD.canMoveRight()and self.BoxC.canMoveRight() and self.BoxB.canMoveRight()
    def canMoveDown(self):
        if self.state==0:
            return self.BoxC.canMoveDown() and self.BoxD.canMoveDown() and self.BoxB.canMoveDown()
        if self.state==1:
            return self.BoxD.canMoveDown() and self.BoxB.canMoveDown()
        if self.state==2:
            return self.BoxB.canMoveDown() and self.BoxD.canMoveDown() and self.BoxA.canMoveDown()
        if self.state==3:
            return self.BoxA.canMoveDown() and self.BoxB.canMoveDown()
class jShape:
    def __init__(self,boxa,boxb,boxc,boxd):
        self.BoxA,self.BoxB,self.BoxC,self.BoxD=boxa,boxb,boxc,boxd
        self.state=0
    def begin(self):
        self.BoxA.setXY(5,0)
        self.BoxB.setXY(5,1)
        self.BoxC.setXY(5,2)
        self.BoxD.setXY(4,2)
        self.state=0
    def turn(self):
        if self.state==0 and self.BoxC.canMoveRight() and self.BoxD.canMoveUp():
            self.BoxB.setXY(self.BoxC.x-1,self.BoxC.y-1)
            self.BoxA.setXY(self.BoxC.x+1,self.BoxC.y)
            self.state=1
        elif self.state==1 and self.BoxC.canMoveUp() and self.BoxB.canMoveRight() and self.BoxA.canMoveTwoUp():
            self.BoxB.setXY(self.BoxC.x,self.BoxC.y-1)
            self.BoxA.setXY(self.BoxC.x,self.BoxC.y-2)
            self.BoxD.setXY(self.BoxC.x+1,self.BoxC.y-2)
            self.state=2
        elif self.state==2 and self.BoxA.canMoveLeft() and self.BoxD.canMoveDown():
            self.BoxC.setXY(self.BoxA.x-1,self.BoxA.y)
            self.BoxB.setXY(self.BoxD.x,self.BoxD.y+1)
            self.state=3
        elif self.state==3 and self.BoxA.canMoveDown() and self.BoxA.canMoveTwoDown() and self.BoxC.canMoveTwoDown():
            self.BoxB.setXY(self.BoxA.x,self.BoxA.y+1)
            self.BoxC.setXY(self.BoxA.x,self.BoxA.y+2)
            self.BoxD.setXY(self.BoxA.x-1,self.BoxA.y+2)
            self.state=0
    def canMoveLeft(self):
        if self.state==0:
            return self.BoxA.canMoveLeft() and self.BoxB.canMoveLeft() and self.BoxD.canMoveLeft()
        if self.state==1:
            return self.BoxD.canMoveLeft() and self.BoxB.canMoveLeft()
        if self.state==2:
            return self.BoxA.canMoveLeft() and self.BoxB.canMoveLeft() and self.BoxC.canMoveLeft()
        if self.state==3:
            return self.BoxC.canMoveLeft() and self.BoxB.canMoveLeft()
    def canMoveRight(self):
        if self.state==0:
            return self.BoxB.canMoveRight()and self.BoxA.canMoveRight() and self.BoxC.canMoveRight()
        if self.state==1:
            return self.BoxB.canMoveRight() and self.BoxA.canMoveRight()
        if self.state==2:
            return self.BoxB.canMoveRight() and self.BoxC.canMoveRight() and self.BoxD.canMoveRight()
        if self.state==3:
            return self.BoxD.canMoveRight() and self.BoxB.canMoveRight()
    def canMoveDown(self):
        if self.state==0:
            return self.BoxC.canMoveDown() and self.BoxD.canMoveDown()
        if self.state==1:
            return self.BoxD.canMoveDown() and self.BoxC.canMoveDown() and self.BoxA.canMoveDown()
        if self.state==2:
            return self.BoxC.canMoveDown() and self.BoxD.canMoveDown()
        if self.state==3:
            return self.BoxA.canMoveDown() and self.BoxB.canMoveDown() and self.BoxC.canMoveDown()
class zShape:
    def __init__(self,boxa,boxb,boxc,boxd):
        self.BoxA,self.BoxB,self.BoxC,self.BoxD=boxa,boxb,boxc,boxd
        self.state=0
    def begin(self):
        self.BoxA.setXY(4,0)
        self.BoxB.setXY(5,0)
        self.BoxC.setXY(5,1)
        self.BoxD.setXY(6,1)
        self.state=0
    def turn(self):
        if self.state==0 and self.BoxC.canMoveLeft() and self.BoxA.canMoveTwoDown() and self.BoxD.canMoveUp():
            self.BoxD.setXY(self.BoxC.x-1,self.BoxC.y+1)
            self.BoxA.setXY(self.BoxC.x-1,self.BoxC.y)
            self.state=1
        elif self.state==1 and self.BoxC.canMoveRight() and self.BoxB.canMoveLeft():
            self.BoxA.setXY(self.BoxB.x-1,self.BoxB.y)
            self.BoxD.setXY(self.BoxC.x+1,self.BoxC.y)
            self.state=0
    def canMoveLeft(self):
        if self.state==0:
            return self.BoxA.canMoveLeft() and self.BoxC.canMoveLeft()
        if self.state==1:
            return self.BoxD.canMoveLeft() and self.BoxB.canMoveLeft() and self.BoxA.canMoveLeft()
    def canMoveRight(self):
        if self.state==0:
            return self.BoxB.canMoveRight()and self.BoxD.canMoveRight()
        if self.state==1:
            return self.BoxB.canMoveRight() and self.BoxC.canMoveRight() and self.BoxD.canMoveRight()
    def canMoveDown(self):
        if self.state==0:
            return self.BoxC.canMoveDown() and self.BoxD.canMoveDown() and self.BoxA.canMoveDown()
        if self.state==1:
            return self.BoxD.canMoveDown() and self.BoxC.canMoveDown()
class sShape:
    def __init__(self,boxa,boxb,boxc,boxd):
        self.BoxA,self.BoxB,self.BoxC,self.BoxD=boxa,boxb,boxc,boxd
        self.state=0
    def begin(self):
        self.BoxA.setXY(6,0)
        self.BoxB.setXY(5,0)
        self.BoxC.setXY(5,1)
        self.BoxD.setXY(4,1)
        self.state=0
    def turn(self):
        if self.state==0 and self.BoxA.canMoveTwoDown() and self.BoxD.canMoveUp():
            self.BoxD.setXY(self.BoxC.x+1,self.BoxC.y+1)
            self.BoxA.setXY(self.BoxC.x+1,self.BoxC.y)
            self.state=1
        elif self.state==1 and self.BoxC.canMoveLeft() and self.BoxA.canMoveUp() and self.BoxD.canMoveLeft():
            self.BoxA.setXY(self.BoxB.x+1,self.BoxB.y)
            self.BoxD.setXY(self.BoxC.x-1,self.BoxC.y)
            self.state=0
    def canMoveLeft(self):
        if self.state==0:
            return self.BoxB.canMoveLeft() and self.BoxD.canMoveLeft()
        if self.state==1:
            return self.BoxD.canMoveLeft() and self.BoxB.canMoveLeft() and self.BoxC.canMoveLeft()
    def canMoveRight(self):
        if self.state==0:
            return self.BoxC.canMoveRight()and self.BoxA.canMoveRight()
        if self.state==1:
            return self.BoxB.canMoveRight() and self.BoxA.canMoveRight() and self.BoxD.canMoveRight()
    def canMoveDown(self):
        if self.state==0:
            return self.BoxC.canMoveDown() and self.BoxD.canMoveDown() and self.BoxA.canMoveDown()
        if self.state==1:
            return self.BoxD.canMoveDown() and self.BoxC.canMoveDown()
#________________________________________________________________
#main game methods:
def eraseAll():
    box1.eraseSelf()
    box2.eraseSelf()
    box3.eraseSelf()
    box4.eraseSelf()    
def drawAll(cShape):
    box1.drawSelf(cShape)
    box2.drawSelf(cShape)
    box3.drawSelf(cShape)
    box4.drawSelf(cShape)
def moveAll(a):
    if a==right:
        box1.move(right)
        box2.move(right)
        box3.move(right)
        box4.move(right)
    elif a==left:
        box1.move(left)
        box2.move(left)
        box3.move(left)
        box4.move(left)
    elif a==down:
        box1.move(down)
        box2.move(down)
        box3.move(down)
        box4.move(down)
def turnShape(cShape):
    if cShape==2:
        Line1.turn()
    elif cShape==3:
        tShape1.turn()
    elif cShape==4:
        lShape1.turn()
    elif cShape==5:
        zShape1.turn()
    elif cShape==6:
        sShape1.turn()
    elif cShape==7:
        jShape1.turn()
def movesLeft(a):
    if(a==1):
        return Square1.canMoveLeft()
    elif a==2:
        return Line1.canMoveLeft()
    elif a==3:
        return tShape1.canMoveLeft()
    elif a==4:
        return lShape1.canMoveLeft()
    elif a==5:
        return zShape1.canMoveLeft()
    elif a==6:
        return sShape1.canMoveLeft()
    elif a==7:
        return jShape1.canMoveLeft()
def movesRight(a):
    if(a==1):
        return Square1.canMoveRight()
    elif a==2:
        return Line1.canMoveRight()
    elif a==3:
        return tShape1.canMoveRight()
    elif a==4:
        return lShape1.canMoveRight()
    elif a==5:
        return zShape1.canMoveRight()
    elif a==6:
        return sShape1.canMoveRight()
    elif a==7:
        return jShape1.canMoveRight()
def movesDown(a):
    if a==1:
        return Square1.canMoveDown()
    elif a==2:
        return Line1.canMoveDown()
    elif a==3:
        return tShape1.canMoveDown()
    elif a==4:
        return lShape1.canMoveDown()
    elif a==5:
        return zShape1.canMoveDown()
    elif a==6:
        return sShape1.canMoveDown()
    elif a==7:
        return jShape1.canMoveDown()
def newShape():#initializes a random shape
    global cShape
    cShape=random.randint(1,7)
    if cShape==1:
        Square1.begin()
    elif cShape==2:
        Line1.begin()
    elif cShape==3:
        tShape1.begin()
    elif cShape==4:
        lShape1.begin()
    elif cShape==5:
        zShape1.begin()
    elif cShape==6:
        sShape1.begin()
    elif cShape==7:
        jShape1.begin()
    drawAll(cShape)
def lineFilled(a):#returns if the line at y=a is filled
    b=True
    for x in xrange(10):
        if Grid[x][a]==0:
            b=False
    return b
def checkGrid():
    global Score
    for y in xrange(20):
        if lineFilled(y):#checks if a line is full
            Score+=100#if a line is filled, increases score by 100
            for q in xrange(y):#for every line above the line filled
                for z in xrange(10):#each cell
                    Grid[z][y-q]=Grid[z][y-q-1]#moves every line above downward                 
def gameOver():
    screen.blit(background,(0,0))
    screen.blit(text2,(350.,300.))
    screen.blit(text3,(370.,670.))
    pygame.draw.circle(screen, (red), (550,555),20,0) 
    screen.blit(directExit,(420,540))
    pygame.mixer.music.stop()
        
        
def clearGrid():
    for x in xrange(10):
        for y in xrange(20):
            Grid[x][y]=0
def tryDown():
    global doAll
    global Score
    if movesDown(cShape):
        eraseAll()
        box1.move(down)
        box2.move(down)
        box3.move(down)
        box4.move(down)
        drawAll(cShape)
    else: 
       checkGrid()
       newShape()
       Score+=30
       if (not movesDown(cShape)) and (Grid[4][0]>0 or Grid[5][0]>0 or Grid[4][1]>0 or Grid[5][1]>0):
           doAll=False
#________________________________________________________________________________
#initialization:
#clock and font objects
clock = pygame.time.Clock()
font = pygame.font.Font("Fonts/ka1.ttf",60)
initial_time=time.time()
box1,box2,box3,box4=box(0,0),box(0,0),box(0,0),box(0,0)
Square1=Square(box1,box2,box3,box4)
Line1=Line(box1,box2,box3,box4)
tShape1=tShape(box1,box2,box3,box4)
lShape1=lShape(box1,box2,box3,box4)
jShape1=jShape(box1,box2,box3,box4)
sShape1=sShape(box1,box2,box3,box4)
zShape1=zShape(box1,box2,box3,box4)
pygame.mixer.music.load("Sounds/Tetris.mp3")
pygame.mixer.music.play(-1)
all_fonts = pygame.font.get_fonts()
font1 = pygame.font.Font("Fonts/ARCADECLASSIC.TTF",50)
font2 = pygame.font.Font("Fonts/ARCADECLASSIC.TTF",20)
font4 = pygame.font.Font("Fonts/ARCADECLASSIC.TTF",36)
font3 = pygame.font.Font("Fonts/ARCADECLASSIC.TTF",90)
text1 = font.render("HISAR", True,(255,255,255))
text5 = font.render("TETRIS", True, (255,255,255))
text2 = font1.render("Score    "+str(Score), True,(255,255,255))
text6 = font1.render("Level    "+ str(Score/500+1), True, (255,255,255))
highScores = font1.render("High Scores", True,(255,255,255))
text3 = font2.render("by    Bensu  Sicim    Cem  Ersoz", True,(255,255,255))
text4 = font3.render("GAME OVER", True,(255,255,255))
reset = font4.render("Press the red button to exit", True,(255,255,255))
newShape()
old_time=0
Score=0
doAll=True
godown=False
while True:
    if not GPIO.input(gamePins.red):
	execfile('launchGPIO.py')
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == KEYDOWN:
	    if event.key == K_q:
	        exit()
	    if doAll:
		if event.key == K_d and movesRight(cShape):
            	    eraseAll()
            	    moveAll(right)
            	    drawAll(cShape)
	    	    time.sleep(.05)
        	elif event.key == K_a and movesLeft(cShape):
            	    eraseAll()
	    	    moveAll(left)
	    	    drawAll(cShape)    
	    	    time.sleep(.05)    
        	elif event.key == K_s :
	    	    old_time-=.5
        	elif event.key == K_w :
	    	    eraseAll()
	    	    turnShape(cShape)
	    	    drawAll(cShape)
	    	    time.sleep(.1)
    if doAll:
        if not GPIO.input(gamePins.right) and movesRight(cShape):
            eraseAll()
            moveAll(right)
            drawAll(cShape)
	    time.sleep(.05)
        elif not GPIO.input(gamePins.left) and movesLeft(cShape):
            eraseAll()
            moveAll(left)
            drawAll(cShape)    
	    time.sleep(.05)    
        elif not GPIO.input(gamePins.down):
            old_time-=.5
        elif not GPIO.input(gamePins.green):
            eraseAll()
            turnShape(cShape)
            drawAll(cShape)
	    time.sleep(.1)
        screen.blit(background,(0,0))
        for x in xrange(10):
            for y in xrange(20):
                pygame.draw.rect(screen,(30,30,30),Rect((275+32*x,20+32*y),(32,32)),1)#draws reference rectangles
        frame = pygame.draw.rect(screen,(255,255,255),Rect((273,18),(324,644)),2)#draws outer frame
        
        for x in xrange(10):#checks the grid
            for y in xrange(20):#to find where the boxes are
                if Grid[x][y]>0:#if cell has a box, colors it                
                    if Grid[x][y]==1: #square
                        pygame.draw.rect(screen,(255,51,204),Rect((275+32*x,20+32*y),(32,32)))#pink
                    elif Grid[x][y]==2: #line
                        pygame.draw.rect(screen,(102,255,51),Rect((275+32*x,20+32*y),(32,32)))#green
                    elif Grid[x][y]==3: #tShape
                        pygame.draw.rect(screen,(255,255,51),Rect((275+32*x,20+32*y),(32,32)))#yellow
                    elif Grid[x][y]==4:#Lshape
                        pygame.draw.rect(screen,(51,102,255),Rect((275+32*x,20+32*y),(32,32)))#cyan
                    elif Grid[x][y]==5:#zShape
                        pygame.draw.rect(screen,(255,51,51),Rect((275+32*x,20+32*y),(32,32)))#blue
                    elif Grid[x][y]==6:#sShape
                        pygame.draw.rect(screen,(51,204,255),Rect((275+32*x,20+32*y),(32,32)))#red
                    elif Grid[x][y]==7:#jShape
                        pygame.draw.rect(screen,(92,0,184),Rect((275+32*x,20+32*y),(32,32)))#purple
                    pygame.draw.rect(screen,(0,0,0),Rect((275+32*x,20+32*y),(32,32)),1)#outline
        
        text2 = font1.render("Score    "+str(Score), True,(255,255,255))
        
	screen.blit(text1,(670.,40.))
        screen.blit(text5, (650.,125))
        screen.blit(text2,(650.,250.))
        screen.blit(text6, (650.,300.))
	screen.blit(highScores,(650.,360.))
        screen.blit(text3,(650.,660.))
	screen.blit(directDrop,(120,220))
	screen.blit(directTurn,(120,300))
	screen.blit(directRight,(120,380))
	screen.blit(directLeft,(120,460))
	pygame.draw.polygon(screen,(225,240,229),[[50,215],[90,215],[70,250]],0)
        pygame.draw.circle(screen, (green), (70,310),20,0) 
        pygame.draw.polygon(screen,(225,240,229),[[50,375],[50,420],[90,398]],0)
        pygame.draw.polygon(screen,(225,240,229),[[90,455],[90,500],[50,478]],0)
	pygame.draw.circle(screen, (red), (70,560),20,0) 
	screen.blit(directExit,(120,540))

	line = 0
	for player in scoreboard:
		line+=1
		winners = font4.render(str(line)+"  "+str(player), True, (255,255,255))
		screen.blit(winners, (650, 380+line*45))

        level=Score/500
        multiplier=(level+2)/10+2
        current_time=int((time.time()-initial_time)*multiplier)
        if current_time>old_time:
            tryDown()
            old_time=current_time
        #print current_time
    elif(not doAll):
        gameOver()
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    clearGrid()
                    doAll=True
	    elif event.key == K_SPACE:
		if gamePins.isHighScore("Tetris", Score):
		    gamePins.newEntry("Tetris", Score)
		    execfile("leaderboards.py")
		else:
		    execfile("launchGPIO.py")
        if not GPIO.input(gamePins.red):
            clearGrid()
            execfile("launchGPIO.py")
    pygame.display.update()
           
