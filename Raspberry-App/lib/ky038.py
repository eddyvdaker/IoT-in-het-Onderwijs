import RPi.GPIO as GPIO
import time

class ky038():
	"""docstring for ky038"""
	def __init__(self, pin):
		self.pin = pin
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.pin, GPIO.IN)

	def read(self):
		return GPIO.input(self.pin)

# GPIO.add_event_detect(sound, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
# GPIO.add_event_callback(sound, callback)  # assign function to GPIO PIN, Run function on change
