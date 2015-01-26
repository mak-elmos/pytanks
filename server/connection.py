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
		#self.sock.settimeout(1)

		self.clients_counter       = 0
		self.clients               = []
		self.clients_received_data = []
		self.clients_received_data_last = []
		self.clients_sent_data     = []

	def startServer(self, host, port):
		self.sock.bind((host, port))
		self.sock.listen(0)

	def allClientsDisconnected(self):
		if len(self.clients):
			return False
		return True

	def closeClients(self):
		for client in self.clients:
			client.close()

	def acceptClient(self, mapname, max_score):
		while True:
			client, addr = self.sock.accept()
			#client.settimeout(1)
			self.clients.append(client)
			self.clients_sent_data.append(False)
			self.send(self.clients_counter, str(self.clients_counter) + ' ' + mapname + ' ' + str(max_score))

			self.clients_received_data.append("")
			self.clients_received_data_last.append("")

			self.startRecvThread(self.clients_counter)
			self.clients_counter += 1

	def recv(self, index):
		self.clients_received_data[index] = ""
		while True:
			try:
				msg = self.clients[index].recv(self.recv_size)

				self.clients_received_data[index] += msg
				self.clients_received_data[index] = self.clients_received_data[index].split(self.endChar)
				##if len(self.clients_received_data[index]) > 2:
				##	print len(self.clients_received_data[index])
				lastData = ""
				if len(self.clients_received_data[index]) >= 2:
					lastData = self.clients_received_data[index][-2]
				if len(self.clients_received_data[index]):
					self.clients_received_data[index] = self.clients_received_data[index][-1]
				self.clients_received_data_last[index] = lastData
			except:
				break


	def startAcceptThread(self, mapname, max_score):
		thread.start_new_thread(self.acceptClient, (mapname, max_score, ))

	def startRecvThread(self, index):
		thread.start_new_thread(self.recv, (index, ))

	def sendByThread(self, index, data):
		thread.start_new_thread(self.send, (index, data, ))

	def recvAll(self):
		return self.clients_received_data_last

	def send(self, index, data):
		try:
			self.clients_sent_data[index] = False
			self.clients[index].send(data + self.endChar)
			self.clients_sent_data[index] = True
			return True
		except:
			return False

	def sendAll(self, data):
		for i in range(len(self.clients)):
			if self.clients_sent_data[i]:
				self.sendByThread(i, data)


if __name__ == "__main__":
	import time

	server = Connection()
	server.startServer("localhost", 10000)
	server.acceptClients(1)
	server.startRecvThreads()

	time.sleep(2)
	while True:
		server.sendAll("[]")
		print server.recvAll()
		time.sleep(0.5)

	server.closeClients()
