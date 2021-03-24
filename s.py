import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from os import path
import os

hostName = ""
hostPort = 80

class MyServer(BaseHTTPRequestHandler):

	#	GET is for clients geting the predi
	def do_GET(self):
		self.send_response(200)
		# self.send_header("Content-type", "image/jpeg")
		# self.end_headers()
		self.wfile.write(open(path.abspath(self.path[1:].replace("%"," ")),'rb').read())
	#	POST is for submitting data.
	def do_POST(self):

		print( "incomming http: ", self.path )

		content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
		post_data = self.rfile.read(content_length) # <--- Gets the data itself
		self.send_response(200)

		client.close()

		#import pdb; pdb.set_trace()


myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
	myServer.serve_forever()
except KeyboardInterrupt:
	pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))