#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

class ky038():
	"""
	detection of highs in sound
	"""

	def __init__(self, pin):
		self.pin = pin
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.pin, GPIO.IN)

	# set a callback function to listen for 'sec' amount of seconds
	def listen(self,sec):
		self.history = []
		self.sec = sec
		initial_time = time.time()
		self.create_callback()
		time.sleep(self.sec)
		GPIO.remove_event_detect(self.pin)
		return self.history

	# GPIO create event function
	def create_callback(self):
		GPIO.add_event_detect(self.pin, GPIO.BOTH, bouncetime=self.sec)  # let us know when the pin goes HIGH or LOW
		GPIO.add_event_callback(self.pin, self.callback)  # assign function to GPIO PIN, Run function on change

	# single read of sound high
	def read(self):
		return GPIO.input(self.pin)

	# callback function
	def callback(self,val):
		self.history.append(1)
