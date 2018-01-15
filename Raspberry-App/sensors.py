import RPi.GPIO as GPIO
import lib.dht11 as dht11
import lib.ky038 as ky038


class sensors():
	"""Sensors"""
	def __init__(self):
		self.dht11Instance = dht11.DHT11(pin = 4)
		self.ky038Instance = ky038(pin = 24)
		self.refresh()

	def refresh(self):
		self.ky038Result = ky038Instance.read()
		self.dht11Result = dht11Instance.read()

	def getTemp(self):
		if dht11Result.is_valid():
		# temperature in degrees celcius
			return self.dht11Result.temperature
		else:
			# return error if read failed
			return dht11Result.error_code

	def getHum(self):
		if dht11Result.is_valid():
			# humidity in percentage
			return self.dht11Result.humidity
		else:
			# return error if read failed
			return dht11Result.error_code

	def getSound(self):
		# todo get avaerage loudness over time
		return self.ky038Result
