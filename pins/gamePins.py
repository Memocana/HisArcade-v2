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