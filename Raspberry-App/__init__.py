from threading import Thread
from sensors import main as sensors
from web_server import main as web_server
from queue import Queue

def main():

	sensors_queue = Queue()
	sensors_thread = Thread(target=sensors,args=(sensors_queue))
	sensors_thread.daemon = True
	sensors_thread.start()

	web_server_queue = Queue()
	web_server_thread = Thread(target=web_server,args=(web_server_queue))
	web_server_thread.daemon = True
	web_server_thread.start()

if __name__ == '__main__':
	main()
