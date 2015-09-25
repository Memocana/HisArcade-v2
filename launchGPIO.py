#!/usr/bin/env python
#Hisar Snake
#copyright: Memet
#Hisar Schools
import time, sys
import pygame
from pygame.locals import *
import RPi.GPIO as GPIO

games = ["tetris.py", "snake.py",'pong.py','pacman.py']


sys.path.insert(0,"/home/pi/Desktop/HisArcade/pins")
import gamePins

gamePins.gameSetup()

pygame.init()
screen=pygame.display.set_mode((1024,718),pygame.FULLSCREEN)
pygame.display.set_caption("HisArcade Launcher!")
#creating the background.
back = pygame.Surface((1024,718))
background = back.convert()
background.fill((0,0,0))
font = pygame.font.Font("Fonts/ARCADECLASSIC.TTF",50)
fontSmall = pygame.font.Font("Fonts/ARCADECLASSIC.TTF",30)

facebook = pygame.image.load('Home/facebook.png')
twitter = pygame.image.load('Home/twitter.png')
insta = pygame.image.load('Home/instagram.png')

tetris = font.render("Tetris", True,(255,255,255))
pong = font.render("Pong 2p", True,(255,255,255))
snake = font.render("Snake", True,(255,255,255))
pacman = font.render("Pacman", True,(255,255,255))
red, yellow, green, blue=(235,53,47),(235,230,45),(0,185,10),(73,170,235)
directUp = fontSmall.render("up", True,(255,255,255))
directDown = fontSmall.render("down", True,(255,255,255))
directSelect = fontSmall.render("select", True,(255,255,255))
media = font.render("HisarCS", True,(255,255,255))

selected = 0
while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
    	    if event.key == K_q:
    	        exit()
    up = GPIO.input(gamePins.up)
    down = GPIO.input(gamePins.down)
    select = GPIO.input(gamePins.green)
    screen.blit(background,(0,0))
    screen.blit(tetris,(450.,100.))
    screen.blit(pong,(450.,400.))
    screen.blit(snake,(460.,250.))
    screen.blit(pacman,(450.,550))
    screen.blit(media,(55.,300))
    screen.blit(directDown,(920,340))
    screen.blit(directUp,(920,260))
    screen.blit(directSelect,(920,420))
    screen.blit(facebook, (45,220))
    screen.blit(twitter, (115,220))
    screen.blit(insta, (185,220))
    if not down:
        selected += 1
    elif not up:
	   selected -= 1
    elif not select:
        execfile(games[selected % len(games)])
    time.sleep(.1)
    pygame.draw.polygon(screen,(225,240,229),[[840,335],[880,335],[860,370]],0)
    pygame.draw.polygon(screen,(225,240,229),[[840,290],[880,290],[860,255]],0)
    pygame.draw.circle(screen, (green), (860,435),20,0) 
    pygame.draw.polygon(screen, (255,255,255), [[385,110+selected % len(games) * 150], [400,125+selected % len(games) * 150],[385,140+selected % len(games) * 150],5])
    pygame.draw.polygon(screen, (255,255,255), [[675,110+selected % len(games) * 150], [650,125+selected % len(games) * 150],[675,140+selected % len(games) * 150],5])
    pygame.display.update()
