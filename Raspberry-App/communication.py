import httplib
import json

class comm:
	"""docstring for comm."""
	def __init__(self):
		self.conn = httplib.HTTPConnection("ts.guydols.nl:5000")

	def getCommand(self):
		self.conn.request("GET","/check_sessions?id=1")
		res = self.conn.getresponse()
		if res.status == "200":
			data = json.loads(res.read())
			return data
		else:
			return None

	def postData(self):
		self.conn.request("GET","/blabla")
		res = self.conn.getresponse()
		if res.status == "200":
			data = json.load(res.read())
			return data
		else:
			return None

def main(comms_queue):
	comm = comm()
	while True:
		cmd = comm.getCommand()
		if cmd == None:
			pass
		else:
			comms_queue.put(cmd)
		time.sleep(60)
