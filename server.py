# -*- coding:utf-8 -*-
from socket import *
import threading,time,os

HOST = ""
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST,PORT)
pid = os.getpid()

def _exit():
	os.popen('taskkill.exe /F /pid:'+str(pid))

def handle(tcp_cli_sock,addr):
	print("connected from :", addr)
	while True:
		data = tcp_cli_sock.recv(BUFSIZ)
		if not data:
			break
		content = '[%s] %s' % (bytes(time.ctime(), "utf-8"), data)
		if data.decode('utf-8') == 'exit':
			tcp_cli_sock.close()
			print('线程退出')
			_exit()
		if data.decode('utf-8') == 'stop':
			break
		tcp_cli_sock.send(content.encode("utf-8"))

	tcp_cli_sock.close()

def main():
	tcp_server = socket(AF_INET,SOCK_STREAM)
	tcp_server.bind(ADDR)
	tcp_server.listen(5)

	while True:
		print("waiting for connection...")  
		tcp_cli_sock, addr = tcp_server.accept()
		t = threading.Thread(target=handle,args=(tcp_cli_sock,addr))
		t.start()

	tcp_server.close()

if __name__ == '__main__':
	main()