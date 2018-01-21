import RPi.GPIO as GPIO
import lib.dht11 as dht11
import lib.ky038 as ky038
import time


class sensors():
	"""Sensors"""
	def __init__(self):
		self.dht11Instance = dht11.DHT11(pin=4)
		self.ky038Instance = ky038.ky038(pin=24)

	def refresh(self):
		self.ky038Result = self.ky038Instance.read()
		self.dht11Result = self.dht11Instance.read()

	def getTemp(self):
		if self.dht11Result.is_valid():
		# temperature in degrees celcius
			return self.dht11Result.temperature
		else:
			# return error if read failed
			return self.dht11Result.error_code

	def getHum(self):
		if self.dht11Result.is_valid():
			# humidity in percentage
			return self.dht11Result.humidity
		else:
			# return error if read failed
			return self.dht11Result.error_code

	def getSound(self):
		# todo get avaerage loudness over time
		return self.ky038Result

	def loop(self):
		self.ky038Instance.listen(60)
		while True:
			# self.refresh()
			# print(self.getTemp())
			# print(self.getHum())
			# print(self.getSound())
			time.sleep(1)

s = sensors()
s.loop()
