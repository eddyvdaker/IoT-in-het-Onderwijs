from threading import Thread
from sensors import main as sensors
from communication import main as comms
from queue import Queue
import time

class controller:
	"""docstring for ."""
	def __init__(self):
		self.recording = False

		self.sensors_queue = Queue()
		self.sensors_thread = Thread(target=sensors,args=(self.sensors_queue))
		self.sensors_thread.daemon = True
		self.sensors_thread.start()

		self.comms_queue = Queue()
		self.comms_thread = Thread(target=comms,args=(self.comms_queue))
		self.comms_thread.daemon = True
		self.comms_thread.start()

		self.loop()

	def loop(self):
		while True:
			cur = comms_queue.get()
			if cur[] == "x":
				self.recording = True
			elif cur[] == "y":
				self.recording = False
			time.sleep(60)

	def startRec(self):
		pass

	def stopRec(self):
		pass

if __name__ == '__main__':
	instance = controller()
