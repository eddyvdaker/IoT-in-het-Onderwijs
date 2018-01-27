import http.client
import json
import time
from queue import Empty

class communication:
	"""docstring for comm."""
	def __init__(self):
		self.conn = http.client.HTTPConnection("ts.guydols.nl:5000")

	def getCommand(self):
		self.conn.request("GET","/check_session?id=1")
		res = self.conn.getresponse()
		if res.status == 200:
			data = json.loads(res.read())
			return data
		else:
			return None

	def postData(self,data):
		headers = {'Content-type': 'application/json'}
		self.conn.request("POST","/upload_data",data,headers)
		res = self.conn.getresponse()
		if res.status == 200:
			return True
		else:
			return False

def main(comms_in, comms_out):
	comm = communication()
	while True:
		cmd = comm.getCommand()
		if cmd == None:
			pass
		else:
			comms_in.put(cmd)
		try:
			data = comms_out.get_nowait()
			json_data = {
			"data_type": data[0],
			"sessiondata": data[1],
			"sessionid":data[2]}
			comm.postData(json.dumps(json_data))
		except Empty:
			pass
		time.sleep(5)
