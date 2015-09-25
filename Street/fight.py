#!/usr/bin/env python
#Hisar Tetris
#copyright: Bensu Sicim
#Hisar Schools
import time
import pygame
from pygame.locals import *
from sys import exit
from serial import Serial
pygame.init()
w=1024
h=718
pWidth=100
screen=pygame.display.set_mode((1024,718))
pygame.display.set_caption("Street Fighter!")
font=pygame.font.Font(None,15)
font2=pygame.font.Font("ARCADECLASSIC.TTF",70)
background = pygame.image.load("bg.png")
p1_0 = pygame.image.load("1_0R.png")
p2_0 = pygame.image.load("2_0L.gif")
class player:
    def __init__(self,a):
        self.x=a
        self.x2=(self.x+pWidth)
        self.speed=50
        self.health=100
        self.turbo=0
def turbo(self,opp):
    if self.turbo != 3:
        opp.health-=5
        self.turbo+=1
        opp.turbo=0
    elif self.turbo == 3:
        opp.health-=40
        self.turbo=0
        opp.turbo=0
def moveRight(self):
    self.x+=self.speed
    self.x2+=self.speed
def moveLeft(self):
    self.x-=self.speed
    self.x2-=self.speed
p1=player(40)
p2=player((w-210))
class char1(pygame.sprite.Sprite):
    def __init__(self,image):
        self.velocity=5
        self.image=image
        self.rect=self.image.get_rect()       
player2=char1(p2_0)
player1=char1(p1_0)
def checkButtons():
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == K_d and p1.x<w:
                moveRight(p1)
            elif event.key == K_a and p1.x>0:
                moveLeft(p1)
            elif event.key == K_w and p2.health!=0 and (abs(p2.x2-p1.x)<=120 or abs(p2.x-p1.x2)<=120):
                turbo(p1,p2)
                if p2.health<=0:
                    p2.health=0
            if event.key == K_LEFT and p2.x2>0:
                moveLeft(p2)
            elif event.key == K_RIGHT and p2.x2<w:
                moveRight(p2)
            elif event.key == K_UP and p1.health!=0 and (abs(p2.x2-p1.x)<=120 or abs(p2.x-p1.x2)<=120):
                turbo(p2,p1)
                if p1.health<=0:
                    p1.health=0
while True:
    if p1.health!=0 and p2.health!=0:
        checkButtons()
        screen.blit(background,(0,0))
        """text1 = font.render((str(p1.x)+" "+str(p1.x2)),True,(255,255,255))
        screen.blit(text1,(500,40))
        text2 = font.render((str(p2.x)+" "+str(p2.x2)),True,(255,255,255))
        screen.blit(text2,(500,80))"""
        screen.blit(player1.image,(p1.x,h-350))
        screen.blit(player2.image,(p2.x,h-350)) 
        #pygame.draw.rect(screen,(255,51,204),Rect((p1.x, h-400),(pWidth,400)))
        #pygame.draw.rect(screen,(51,102,255),Rect((w-p2.x-100,h-400),(pWidth,400)))
        pygame.draw.rect(screen,(255,255,255),Rect((40,40),(p1.health*4,50)))
        pygame.draw.rect(screen,(255,255,255),Rect((w-440,40),(p2.health*4,50)))
        pygame.draw.rect(screen,(255,255,255),Rect((40,110),(p1.turbo*(400/3),50)))
        pygame.draw.rect(screen,(255,255,255),Rect((w-440,110),(p2.turbo*(400/3),50)))
    else:
        screen.blit(background,(0,0))
        text1 = font2.render("Player   1   Wins!",True,(255,255,255))
        text2 = font2.render("Player   2   Wins!",True,(255,255,255))
        if p1.health==0:
            screen.blit(text2,(300,300))
        elif p2.health==0:
            screen.blit(text1,(300,300))
    pygame.display.update()    
                    
    
    
