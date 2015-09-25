#!/usr/bin/env python
#Hisar Leaderboards
#copyright: Memet
#Hisar Schools
import time, sys, string
import pygame
from pygame.locals import *
import RPi.GPIO as GPIO

sys.path.insert(0,"/home/pi/Desktop/HisArcade/pins")
import gamePins

gamePins.gameSetup()

pygame.init()
screen=pygame.display.set_mode((1024,718), pygame.FULLSCREEN)
pygame.display.set_caption("HisArcade")
#creating the background.
back = pygame.Surface((1024,718))
background = back.convert()
background.fill((0,0,0))

congratFont = pygame.font.Font("Fonts/ARCADECLASSIC.TTF",60)
fontSmall = pygame.font.Font("Fonts/ARCADECLASSIC.TTF",30)

color = (255,255,255)

newEntry = open("newEntry", "r")
player = (newEntry.readline()).split()


congrats = congratFont.render("Congratulations New High Score In", True, (255,255,255))
gameName = congratFont.render(str(player[0]), True, (255,255,255))
gamePos  = gameName.get_rect()
gamePos.centerx = background.get_rect().centerx
gamePos.centery = 170
place = str(player[1])
if place == "1":
	place = "1st"
elif place == "2":
	place = "2nd"
elif place == "3":
	place = "3rd"
pos = congratFont.render(place+" Place", True, (255,255,255))
posPos  = pos.get_rect()
posPos.centerx = background.get_rect().centerx
posPos.centery = 250
points = congratFont.render("Score  "+str(player[2]), True, (255,255,255))
pointPos  = points.get_rect()
pointPos.centerx = background.get_rect().centerx
pointPos.centery = 320
names = congratFont.render("Enter Your Name", True, (255,255,255))
namePos = names.get_rect()
namePos.centerx = background.get_rect().centerx
namePos.centery = 440


toBlit = True
selected = 0

name = [0, 0, 0]

done = True
while done:
	row = 0
	column = 0
	for event in pygame.event.get():
		if event.type == KEYDOWN:
			if event.key == K_q:
				done = False
			if event.key == K_SPACE:
				playerName = string.lowercase[name[0]] + string.lowercase[name[1]] + string.lowercase[name[2]]
				file = open(str(player[0]+"/score"),"r")
				allScores = file.readlines()
				file.close()
				file = open(str(player[0]+"/score"),"w")

				addedPlayer = False
				for x in xrange(0,len(allScores)+1):
					if not addedPlayer and x != int(player[1]) - 1:
						file.write(allScores[x])
					elif addedPlayer:
						file.write(allScores[x-1])
					else:
						addedPlayer = True
						file.write(playerName+" "+player[2]+"\n")
				file.close()
				execfile("launchGPIO.py")
			if event.key == K_w:
				name[selected] -= 1
				name[selected] %= 26
			if event.key == K_a:
				selected -= 1
				selected %= 3
			if event.key == K_s:
				name[selected] += 1
				name[selected] %= 26
			if event.key == K_d:
				selected += 1
				selected %= 3
	screen.blit(background,(0,0))
	toBlit = not toBlit
	#letter scroller layout
	for x in xrange(0,3):
		for y in xrange(2,-1,-1):
			bigFont = pygame.font.Font("Fonts/ARCADECLASSIC.TTF",108-y*18)
			toPrint = bigFont.render(string.lowercase[(name[x]+y)%26], True, (255,255,255))
			textSurface = pygame.Surface((bigFont.size(string.lowercase[(name[x]+y)%26])[0], bigFont.size(string.lowercase[(name[x]+y)%26])[1] - 20))
			textSurface.blit(toPrint, (0,0))
			textSurface.set_alpha(255-y*50)
			if not (toBlit and x == selected and y == 0):
				screen.blit(textSurface, (364 + x*125 + y*5, 500 + y*(85-(y-1)*10)))

	screen.blit(congrats, (10,30))
	screen.blit(gameName, gamePos)
	screen.blit(points, pointPos)
	screen.blit(pos, posPos)
	screen.blit(names, namePos)

	time.sleep(.1)
	pygame.display.update()
