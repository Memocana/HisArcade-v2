import RPi.GPIO as GPIO

right = 9
left = 22
up = 10
down = 15

red = 4
blue = 12
green = 17
yellow = 14

def gameSetup():
	GPIO.setmode(GPIO.BCM)

	GPIO.setup(blue, GPIO.IN, pull_up_down = GPIO.PUD_UP) #BLUE
	GPIO.setup(yellow, GPIO.IN, pull_up_down = GPIO.PUD_UP) #YELLOW
	GPIO.setup(green, GPIO.IN, pull_up_down = GPIO.PUD_UP) #GREEN
	GPIO.setup(red, GPIO.IN, pull_up_down = GPIO.PUD_UP) #RED

	GPIO.setup(down, GPIO.IN, pull_up_down = GPIO.PUD_UP) #DOWN
	GPIO.setup(up, GPIO.IN, pull_up_down = GPIO.PUD_UP) #UP
	GPIO.setup(right, GPIO.IN, pull_up_down = GPIO.PUD_UP) #RIGHT
	GPIO.setup(left, GPIO.IN, pull_up_down = GPIO.PUD_UP) #LEFT

def getScores(gameName): #gameName = folder of score file, returns top three players
	fileName = gameName+"/score"
	file = open(fileName, "r")
	bests = []
	x = 0
	for line in file:
		if line != "\n" and line != "":
			bests.append(line[:-1])
		x+=1
	file.close()
	return bests

def isHighScore(gameName, point):
	fileName = gameName+"/score"
	file = open(fileName, "r")
	bests = ["","",""]
	x = 0
	for line in file:
		if line != "\n" and line != "":
			bests[x] = line[:-1].split()[1]
			x+=1
	file.close()


	if bests[0] == "" or point > int(bests[0]):
		return 1
	if bests[1] == "" or point > int(bests[1]):
		return 2
	if bests[2] == "" or point > int(bests[2]):
		return 3

	file.close()
	return False

def newEntry(gameName, points):
	file = open("newEntry", "w")
	pos = isHighScore(gameName, points)
	file.write(gameName +" " +str(pos) +" " +str(points))

	
