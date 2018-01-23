from threading import Thread
from sensors import main as sensors
from communication import main as comms
from queue import Queue
import time

def main():

	sensors_queue = Queue()
	sensors_thread = Thread(target=sensors,args=(sensors_queue))
	sensors_thread.daemon = True
	sensors_thread.start()

	comms_queue = Queue()
	comms_thread = Thread(target=comms,args=(comms_queue))
	comms_thread.daemon = True
	comms_thread.start()

	while True:
		comms_queue.get()
		time.sleep(60)


if __name__ == '__main__':
	main()
