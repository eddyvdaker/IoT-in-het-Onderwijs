import RPi.GPIO as GPIO
import time
import os


class ky018:
	"""
	light sensor lib
	"""

	def __init__(self, pin):
		self.pin = pin
		GPIO.setmode(GPIO.BCM)

	# check the amount of light comming in
	def read(self):
		self.count = 0
		GPIO.setup(self.pin, GPIO.OUT)
		GPIO.output(self.pin, GPIO.LOW)
		time.sleep(0.1)
		GPIO.setup(self.pin, GPIO.IN)
		while (GPIO.input(self.pin) == GPIO.LOW):
			self.count += 1
		return self.count
