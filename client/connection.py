#! /usr/bin/python

__author__ = 'Amin'

import socket
import thread

import constvars

class Connection:
	recv_size = constvars.connection_recv_size
	endChar   = constvars.connection_endChar

	def __init__(self):
		self.sock = socket.socket()
		connected = False
		self.received_data = ""
		self.lastData = ""

	def connect(self, host, port):
		try:
			self.sock.connect((host, port))
			self.connected = True
			first_data = self.sock.recv(self.recv_size).split(self.endChar)[0]
			return first_data
		except:
			self.connected = False
			return None

	def disconnect(self):
		#self.send("<DISCONNECT>")
		self.connected = False
		self.sock.close()

	def startRecvThread(self):
		thread.start_new_thread(self.recv_thread, ())

	def recv_thread(self):
		while self.connected:
			try:
				self.received_data += self.sock.recv(self.recv_size)
				self.received_data = self.received_data.split(self.endChar)
				##if len(self.received_data) > 2:
				##	print len(self.received_data)
				if len(self.received_data) >= 2:
					self.lastData = self.received_data[-2]
				if len(self.received_data):
					self.received_data = self.received_data[-1]
			except:
				break

	def recv(self):
		return self.lastData

	def send(self, data):
		try:
			self.sock.send(data + self.endChar)
			return True
		except:
			return False


if __name__ == "__main__":
	client = Connection()
	print client.connect("localhost", 10000)
	print "id = ", client.recv()

	while True:
		print client.recv()
		msg = "msggggggggG"
		if not client.send(msg):
			break

	client.disconnect()
