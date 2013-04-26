#! /usr/bin/env python
import os, sys
from random import randint, choice
from math import sin, cos, radians

import pygame
from pygame.sprite import Sprite

from vec2d import vec2d

class wheel(Sprite):
	def __init__(self, screen, img_array, init_position):
		Sprite.__init__(self)
		self.isSpinning = False
		self.imageNumber = 0
		self.screen = screen
		self.imgArray = img_array
		self.image = img_array[0]
		self.pos = vec2d(init_position)
		self.image_w, self.image_h = self.image.get_size()
		
		self.randomizeImage()
	
	def switchSpin(self):
		self.isSpinning = not self.isSpinning
		# DEBUG STUFF!
		'''
		if self.isSpinning == False:
			self.imageNumber = 1
			self.base_image = self.imgArray[self.imageNumber]
			self.image = self.base_image'''
	
	def randomizeImage(self):
		self.imageNumber = randint(0, len(self.imgArray) - 1)
		# 'normal' way to load an imge as a sprite (already done in main loop with the nice global image array)
		# pygame.image.load(img_filename).convert_alpha()
		self.image = self.imgArray[self.imageNumber]
	
	def update(self, time_passed):
		if self.isSpinning == True:
			self.randomizeImage()
		
	def blitme(self):
		""" 
			Blit the IMG onto the screen that was provided in
			the constructor.
		"""
		draw_pos = (self.pos.x, self.pos.y)
		self.screen.blit(self.image, draw_pos)
		
# TODO: BUTTON is totally messed up, FIX IT!
class Button(Sprite):
	def __init__(self, screen, img_filename, init_position):
		Sprite.__init__(self)
		
		self.screen = screen
		self.speed = 1
		
		# base_image holds the original image, positioned to
		# angle 0.
		# image will be rotated.
		#
		self.base_image = pygame.image.load(img_filename).convert_alpha()
		self.image = self.base_image
		
		# A vector specifying the creep's position on the screen
		#
		self.pos = vec2d(init_position)
		#self.bounds = self.image_w, self.image_h = self.image.get_size()
		self.image_w, self.image_h = self.image.get_size()
		self.bounds_rect = self.screen.get_rect().inflate(-self.image_w, -self.image_h)
		self.sides = (self.image_w + self.pos.x ,self.image_h + self.pos.y)
		self.textSwitch = ['START', 'STOP']
		self.text = self.textSwitch[0]
		
	def printText(self, txtText, Textfont, Textsize , Textx, Texty, Textcolor):
		# pick a font you have and set its size
		myfont = pygame.font.SysFont(Textfont, Textsize)
		# apply it to text on a label
		label = myfont.render(txtText, 1, Textcolor)
		# put the label object on the screen at point Textx, Texty
		self.screen.blit(label, (Textx, Texty))
		
		
	def update(self, time_passed):
		self.image_w, self.image_h = self.image.get_size()

	
	def hitMySpace(self, x, y):
		print x,y,self.pos.x,self.pos.y, self.sides #self.image_w, self.image_h
		if x >= self.pos.x and x <= self.sides[0] and y >= self.pos.y and y <= self.sides[1]:
			if self.textSwitch[0] == self.text:
				self.text = self.textSwitch[1]
			else:
				self.text = self.textSwitch[0]
			return True
		else:
			return False
			
	def blitme(self):
		""" 
			Blit the BUTTON onto the screen that was provided in
			the constructor.
		"""

		draw_pos = (self.pos.x, self.pos.y)
		self.screen.blit(self.image, draw_pos)
		#fnt = pygame.font.SysFont("MS Comic Sans", 30)
		#fntXpos = (self.pos.x + (self.image_w / 2)) - fnt.size(self.text)[0]
		self.printText(self.text, "MS Comic Sans", 30, self.pos.x + (self.image_w / 4), self.pos.y + (self.image_h / 3), (0,0,255))
		#self.printText(self.text, "MS Comic Sans", 30, fntXpos, self.pos.y + (self.image_h / 3), (0,0,255))


class bandit(object):
	def __init__(self):
		self.screen = None
		self.mouseLastLeftDown = False
		self.countWin = 0
		self.countLose = 0
		self.countRound = 0
	
	def mouseKlicked(self, newstateMdown):
		leftKlicked = False
		if self.mouseLastLeftDown == True and newstateMdown == False:
			leftKlicked = True
		else:
			leftKlicked = False
		self.mouseLastLeftDown = newstateMdown
		return leftKlicked
	
	def gameLogic(self, wheels, roundEnded):
		similarWheels = {}
		for whl in wheels:
			if whl.imageNumber in similarWheels:
				similarWheels[whl.imageNumber] +=1
			else:
				similarWheels[whl.imageNumber] = 1

		resultText = ''
		if len(similarWheels) == 1:
			resultText = "!WIN!"
			if roundEnded == True:
				self.countWin += 1
		else:
			resultText = "!LOSE!"
			if roundEnded == True:
				self.countLose += 1
		
		fontSize = 30
		# str.__len__()
		xPos = (self.SCREEN_WIDTH / 2)
		
		# debug-foo
		#self.screen.blit(pygame.font.SysFont("MS Comic Sans", fontSize).render(str(similarWheels), 1, (0,0,255)), (xPos, 250))
		# little too simple!
		#self.screen.blit(pygame.font.SysFont("MS Comic Sans", fontSize).render(resultText, 1, (0,0,255)), (xPos, 250 + fontSize))
		fnt = pygame.font.SysFont("MS Comic Sans", fontSize)
		#print fnt.size(resultText)
		self.screen.blit(fnt.render(resultText, 1, (0,0,255)), (xPos - (fnt.size(resultText)[0] / 2), 250))
		
		winLose = "wins: "+ str(self.countWin) +" loses: "+ str(self.countLose)
		self.screen.blit(fnt.render(winLose, 1, (0,0,255)), (xPos - (fnt.size(winLose)[0] / 2), 250 + fontSize))
	
	def run_game(self):
		# Game parameters
		self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 1024, 600
		BG_COLOR = 238, 238, 238
		
		pygame.init()
		
		# do fancy window stuff
		pygame.display.set_caption("BANDIT")
		pygame.display.set_icon(pygame.image.load('imgs/bandit.jpg'))
		
		self.screen = pygame.display.set_mode(
					(self.SCREEN_WIDTH, self.SCREEN_HEIGHT), 0, 32)
		clock = pygame.time.Clock()

		spriteObjects = []
		spriteObjects.append(Button(self.screen, 'imgs/gbg.jpg', ( (self.SCREEN_WIDTH / 2) - 50, self.SCREEN_HEIGHT - 100 ) ))


		# load all wheelimages into an "globaL" array
		# only pass the "reference" to the wheel-class, so we load each image ONCE and NOT all for each wheel
		WHEELIMAGES = []
		for i in range(1, 6):
			#transform.scale(background, (1200,800))
			img_filename = 'imgs/s'+str(i)+'.png'
			# transform for the sprite!
			#WHEELIMAGES.append(  pygame.transform.scale(pygame.image.load('imgs/s'+str(i)+'.png'), (150,150)) )
			WHEELIMAGES.append( pygame.transform.scale(pygame.image.load(img_filename).convert_alpha(), (150,150)) )
		
		wheels = []
		for i in range(0, 5):
			wheels.append( wheel(self.screen, WHEELIMAGES, (i * 180,0) ) )


		# some vars only for the game loop
		mouseX = 0
		mouseY = 0
		LEFT = 1
		spinWheels = False
		redrawWheelsCount = 0
		
		# The main game loop
		#
		while True:
			# Limit frame speed to 50 FPS
			#
			time_passed = clock.tick(50)
			redrawWheelsCount += time_passed
			
			roundEnded = False
			mouseKlickedLeft = False
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.exit_game()
				elif event.type == pygame.MOUSEMOTION:
					mouseX, mouseY = event.pos
				elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
					mouseKlickedLeft = self.mouseKlicked(True)
				elif event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
					mouseKlickedLeft = self.mouseKlicked(False)
			
			if mouseKlickedLeft:
				print "klicked at:", mouseX, mouseY
				
			# limit the refreshrate further!
			if redrawWheelsCount >= 59 or mouseKlickedLeft:
				# Redraw the background
				self.screen.fill(BG_COLOR)
			
				# Update and redraw
				for sprt in spriteObjects:
					if mouseKlickedLeft and sprt.hitMySpace(mouseX, mouseY):
						print 'hited'
						spinWheels = not spinWheels
						if spinWheels == True:
							self.countRound += 1
							roundEnded = False
						else:
							roundEnded = True
						
						for whl in wheels:
							whl.switchSpin()
									
					sprt.update(time_passed)
					sprt.blitme()

				redrawWheelsCount = 0
				
				for whl in wheels:
					whl.update(time_passed)
					whl.blitme()
				
				
				if spinWheels == False and self.countRound > 0:
					self.gameLogic(wheels, roundEnded)

				pygame.display.flip()

	def exit_game(self):
		sys.exit()

bnd = bandit()
bnd.run_game()

