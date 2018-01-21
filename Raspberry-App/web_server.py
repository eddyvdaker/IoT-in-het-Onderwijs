from os import curdir
from os.path import join as pjoin
from http.server import BaseHTTPRequestHandler, HTTPServer

class StoreHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		if self.path == '/':
			with open(self.index, 'rb') as fh:
				self.send_response(200)
				self.send_header('Content-type', self.content_type(self.path))
				self.end_headers()
				self.wfile.write(fh.read())
		elif self.path == '/':
			with open(self.index, 'rb') as fh:
				self.send_response(200)
				self.send_header('Content-type', self.content_type(self.path))
				self.end_headers()
				self.wfile.write(fh.read())

	def do_POST(self):
		if self.path == '/store.json':
			length = self.headers['content-length']
			data = self.rfile.read(int(length))
			with open(self.store_path, 'w') as fh:
				fh.write(data.decode())
			self.send_response(200)

def main():
	server = HTTPServer(('0.0.0.0', 8080), StoreHandler)
	server.serve_forever()
