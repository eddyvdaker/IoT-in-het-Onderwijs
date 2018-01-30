#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

class Led:
	"""docstring for rgbLed"""

	def __init__(self):
		self.pins = {'pin_R':17, 'pin_G':18, 'pin_B':27}  # pins is a dict
		GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by logical location
		for i in self.pins:
			GPIO.setup(self.pins[i], GPIO.OUT)   # Set pins mode is output
			GPIO.output(self.pins[i], GPIO.LOW)

	def setColor(self,col):
		if int(col[0]):
			GPIO.output(self.pins['pin_R'],GPIO.HIGH)
		else:
			GPIO.output(self.pins['pin_R'],GPIO.LOW)
		if int(col[1]):
			GPIO.output(self.pins['pin_G'],GPIO.HIGH)
		else:
			GPIO.output(self.pins['pin_G'],GPIO.LOW)
		if int(col[2]):
			GPIO.output(self.pins['pin_B'],GPIO.HIGH)
		else:
			GPIO.output(self.pins['pin_B'],GPIO.LOW)

	def off(self):
		for i in self.pins:
			GPIO.output(self.pins[i], GPIO.LOW)    # Turn off all leds
