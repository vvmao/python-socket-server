# -*- coding:utf-8 -*-
from socket import *
HOST = "127.0.0.1"
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST,PORT)

tcp_cli_sock = socket(AF_INET,SOCK_STREAM)
tcp_cli_sock.connect(ADDR)

while True:
	data = input("> ")
	if not data:
		break
	
	tcp_cli_sock.send(data.encode('utf-8'))
	data = tcp_cli_sock.recv(BUFSIZ)
	if not data:
		break
	print(data.decode('utf-8'))


