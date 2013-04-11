import pygame, sys
from pygame.locals import *
from random import randrange
import math

FPS = 60
WINDOWWIDTH = 640
WINDOWHEIGHT = 480

WHITE = (255, 255, 255)
BLACK = ( 0, 0, 0)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
DARKGREEN = ( 0, 155, 0)
DARKGRAY = ( 40, 40, 40)

emptybox = pygame.image.load('art/empty-box.png')
perfectbox = pygame.image.load('art/green-box.png')
goodbox = pygame.image.load('art/yellow-box.png')
failbox = pygame.image.load('art/red-box.png')
musicbox = pygame.image.load('art/music-box.png')

scoreHeading = "Score: "
accuracyHeading= "Accuracy: "

pygame.font.init()
scoreFont = pygame.font.Font('freesansbold.ttf', 32)


UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

def main():
	global FPSCLOCK, DISPLAYSURF, BASICFONT
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT),0,32)	
	BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
	pygame.display.set_caption('Blockdodge')
	#showStartScreen()
	while True:
		runGame()
		showGameOverScreen()

def runGame():
	score=0
	errorMargin= {"perfect": 20, "good": 50}
	scores={"perfect": 20, "good": 10}
	blockXcoord=WINDOWWIDTH-90
	blockCoords = (blockXcoord, 20)	
	xcoord = 0   
	blockPresent=True
	lastBlockSent=pygame.time.get_ticks()
	intervalRange=(20,1500)
	interval=randrange(intervalRange[0],intervalRange[1])
	speedRange=(1,5)
	currBox= emptybox
	accuracy=0.00
	boxesPassed=1
	scoreCoords= (20,100)
	scoreSurface=getScoreSurface(score)
	accuracySurface= getAccuracySurface(accuracy)
	accuracyCoords=(20,160)
	while True: #main game loop	
		if blockPresent:
			if xcoord>blockXcoord:
				repaint([
					{"surface": currBox, "coords": blockCoords},
					{"surface": scoreSurface, "coords": scoreCoords},
					{"surface": accuracySurface, "coords": accuracyCoords}
				])
				blockPresent=False
				lastBlockSent=pygame.time.get_ticks()
			else:
				xcoord+=float(randrange(speedRange[0],speedRange[1]))/10
				mblockCoords = (xcoord,20) 
				repaint([
					{"surface": currBox, "coords": blockCoords},
					{"surface": musicbox, "coords": mblockCoords},
					{"surface": scoreSurface, "coords": scoreCoords},
					{"surface": accuracySurface, "coords": accuracyCoords}
				])
		else:			
			if(pygame.time.get_ticks()-lastBlockSent==interval):
				blockPresent=True
				xcoord=0
				interval=randrange(intervalRange[0],intervalRange[1])
				repaint([
					{"surface": currBox, "coords": blockCoords},
					{"surface": scoreSurface, "coords": scoreCoords},
					{"surface": accuracySurface, "coords": accuracyCoords}
				])
				boxesPassed+=1
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
			elif event.type == KEYDOWN:
				if (event.key == K_SPACE):
					diff=math.fabs(xcoord-blockXcoord)
					if diff<=errorMargin["perfect"]:
						score+=scores["perfect"]						
						currBox=perfectbox
					elif diff<errorMargin["good"]:
						score+=scores["good"]
						currBox=goodbox
					else:
						currBox=failbox					
					accuracy=calcAccuracy(score,boxesPassed,scores["perfect"])
					scoreSurface=getScoreSurface(score)
					accuracySurface=getAccuracySurface(accuracy)
				elif event.key == K_ESCAPE:
					terminate()
		keys= pygame.key.get_pressed() 	
		if not keys[pygame.K_SPACE]:
			currBox=emptybox
				
		pygame.display.update()
    	fpsClock.tick(FPS)

def calcAccuracy(score,boxes,max):
	return (float(score)/(boxes*max))*100

def repaint(items):
	DISPLAYSURF.fill(WHITE)
	for i in items:
		DISPLAYSURF.blit(i["surface"], i["coords"])

def getScoreSurface(score):
	string="%s %i"% (scoreHeading, score)
	scoreFontSurface = scoreFont.render(string, True, BLACK)
	return scoreFontSurface

def getAccuracySurface(accuracy):
	string="%s %.2f%%"% (accuracyHeading, accuracy)
	accuracyFontSurface = scoreFont.render(string, True, BLACK)
	return accuracyFontSurface

def drawPressKeyMsg():
	pressKeySurf = BASICFONT.render('Press a key to play.', True, 
DARKGRAY)
	pressKeyRect = pressKeySurf.get_rect()
	pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
	DISPLAYSURF.blit(pressKeySurf, pressKeyRect)
 
def checkForKeyPress():
	if len(pygame.event.get(QUIT)) > 0:
		terminate()

	keyUpEvents = pygame.event.get(KEYUP)
	if len(keyUpEvents) == 0:
		return None
	if keyUpEvents[0].key == K_ESCAPE:
		terminate()
	return keyUpEvents[0].key

def showStartScreen():
	titleFont = pygame.font.Font('freesansbold.ttf', 100)
	titleSurf1 = titleFont.render('Block Dodge!', True, WHITE, DARKGREEN)
	titleSurf2 = titleFont.render('Block Dodge!', True, GREEN)

	degrees1 = 0
	degrees2 = 0
	while True:
		DISPLAYSURF.fill(WHITE)
		rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
		rotatedRect1 = rotatedSurf1.get_rect()
		rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
		DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)
	
		rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
		rotatedRect2 = rotatedSurf2.get_rect()
		rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
		DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)
	
		drawPressKeyMsg()

		if checkForKeyPress():
			pygame.event.get()
			return
		pygame.display.update()
		FPSCLOCK.tick(FPS)
		degrees1 += 3
		degrees2 += 7
def terminate():
	pygame.quit()
	sys.exit()
main()
