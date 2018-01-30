#!/usr/bin/python
# -*- coding: utf-8 -*-

from threading import Thread
from sensors import main as sensors
from communication import main as comms
from queue import Queue
import lib.rgb
import time

class controller:
	"""
	Controllerclass to setup sensors and communication classes,
	these are launched in seperate threads and given queues for communication between threads
	"""

	def __init__(self):
		# session globals
		self.recording = False
		self.id = None
		self.led = lib.rgb.Led()

		# creating thread and queues
		self.sensors_in = Queue()
		self.sensors_out = Queue()
		self.sensors_thread = Thread(target=sensors,
		args=(self.sensors_in, self.sensors_out, ))
		self.sensors_thread.daemon = True
		self.sensors_thread.start()

		# creating thread and queues
		self.comms_in = Queue()
		self.comms_out = Queue()
		self.comms_thread = Thread(target=comms,
		args=(self.comms_in, self.comms_out, ))
		self.comms_thread.daemon = True
		self.comms_thread.start()

		self.led.setColor("010")
		self.loop()

	# main loop of the controller to check communication que and act on it
	def loop(self):
		while True:
			cur = self.comms_in.get()
			if cur["status"] == "running" and self.recording == False:

				print("starting sensors, __init__.py")
				self.recording = True
				self.id = cur["id"]
				self.startRec()
			elif cur["status"] == "stopped" and self.recording == True:
				print("stopping sensors, __init__.py")
				self.recording = False
				self.stopRec()
				self.id = None
			else:
				print("Nothing do to...")
			time.sleep(5)

	# start recording of sensor data
	def startRec(self):
		self.led.setColor("100")
		self.sensors_in.put("start")

	# stop recording of sensor data and send it to the comm thread
	def stopRec(self):
		self.led.setColor("001")
		self.sensors_in.put("stop")
		data = self.sensors_out.get()
		temps=[]
		humis=[]
		for dht in data[0]:
			temps.append(dht[0][0])
			humis.append(dht[0][1])
		self.comms_out.put(["temperatuur",temps,self.id])
		self.comms_out.put(["vochtigheid",humis,self.id])
		self.comms_out.put(["geluid",data[1],self.id])
		self.comms_out.put(["light",data[2],self.id])
		self.id = None
		self.led.setColor("010")

if __name__ == '__main__':
	instance = controller()
