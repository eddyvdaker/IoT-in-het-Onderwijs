from queue import Empty
from queue import Queue
from threading import Thread
import RPi.GPIO as GPIO
import lib.dht11 as dht11
import lib.ky038 as ky038
import lib.ky018 as ky018
import time



class runDHT11:
	def __init__(self,cin,cout,interval):
		self.cin = cin
		self.cout = cout
		self.interval = interval
		self.dht11Instance = dht11.DHT11(pin=4)
		self.data = []
		self.running = True
		self.main()

	def getData(self,interval):
		initial_time = time.time()
		data = []
		while time.time()-initial_time < interval:
			if data == []:
				self.dht11Result = self.dht11Instance.read()
				if self.dht11Result.is_valid():
					data.append([[self.dht11Result.temperature,time.time()],
					[self.dht11Result.humidity,time.time()]])
				else:
					pass
			else:
				pass
		return data

	def main(self):
		while self.running == True:
			try:
				cmd = self.cin.get_nowait()
				if cmd == "stop":
					self.cout.put(self.data)
					self.running = False
			except Empty:
				pass
			self.data.append(self.getData(self.interval))



class runKY038:
	def __init__(self,cin,cout,interval):
		self.cin = cin
		self.cout = cout
		self.interval = interval
		self.ky038Instance = ky038.ky038(pin=24)
		self.data = []
		self.running = True
		self.main()

	def getData(self,interval):
		return self.ky038Instance.listen(interval)

	def main(self):
		while self.running == True:
			try:
				cmd = self.cin.get_nowait()
				if cmd == "stop":
					self.cout.put(self.data)
					self.running = False
			except Empty:
				pass
			self.data.append([self.getData(self.interval),time.time()])



class runKY018:
	def __init__(self,cin,cout,interval):
		self.cin = cin
		self.cout = cout
		self.interval = interval
		self.ky018Instance = ky018.ky018(pin=3)
		self.data = []
		self.running = True
		self.main()

	def getData(self):
		return self.ky018Instance.read()

	def main(self):
		while self.running == True:
			try:
				cmd = self.cin.get_nowait()
				if cmd == "stop":
					self.cout.put(self.data)
					self.running = False
			except Empty:
				pass
			self.data.append([self.getData(),time.time()])
			if self.running:
				time.sleep(self.interval)



def main(sensors_in,sensors_out):
	interval = 60
	while True:
		try:
			cmd = sensors_in.get_nowait()
			if cmd == "start":

				dht11in = Queue()
				ky038in = Queue()
				ky018in = Queue()
				dht11out = Queue()
				ky038out = Queue()
				ky018out = Queue()

				dht11_thread = Thread(target=runDHT11,
				name="dht11_thread",args=(dht11in, dht11out, interval, ))
				ky038_thread = Thread(target=runKY038,
				name="ky038_thread",args=(ky038in, ky038out, interval, ))
				ky018_thread = Thread(target=runKY018,
				name="ky018_thread",args=(ky018in, ky018out, interval, ))

				dht11_thread.start()
				ky038_thread.start()
				ky018_thread.start()

			elif cmd == "stop":

				dht11in.put("stop")
				ky038in.put("stop")
				ky018in.put("stop")

				dht11_thread.join()
				ky038_thread.join()
				ky018_thread.join()

				dht11data = dht11out.get()
				ky038data = ky038out.get()
				ky018data = ky018out.get()

				sensors_out.put([dht11data,ky038data,ky018data])

		except Empty:
			pass
		time.sleep(5)
