# -*- coding:utf-8 -*-
from socket import *
import threading,time,os,signal,sys

HOST = ""
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST,PORT)
pid = os.getpid()

def _exit(tcp_cli_sock):
	tcp_cli_sock.shutdown(2)
	tcp_cli_sock.close()	
	sys.exit(0)
def handle(tcp_cli_sock,addr):
	# print("connected from :", addr)
	while True:
		data = tcp_cli_sock.recv(BUFSIZ)
		if not data or data.decode('utf-8') == 'exit' or data.decode('utf-8') == 'stop':
			break
		content = '[%s] %s' % (bytes(time.ctime(), "utf-8"), data.decode("utf-8"))
		tcp_cli_sock.send(content.encode("utf-8"))
	_exit(tcp_cli_sock)

def main():
	tcp_server = socket(AF_INET,SOCK_STREAM)
	tcp_server.bind(ADDR)
	tcp_server.listen(5)

	while True:
		# print("waiting for connection...")  
		tcp_cli_sock, addr = tcp_server.accept()
		pid = os.fork()
		if pid == 0:
			handle(tcp_cli_sock,addr)
			break
		else:
			pass
		# t = threading.Thread(target=handle,args=(tcp_cli_sock,addr))
		# t.start()

	tcp_server.close()

def wait_child(signum,frame):
	# while True:
		# -1 表示任意子进程
		# os.WNOHANG 表示如果没有可用的需要 wait 退出状态的子进程，立即返回不阻塞
	cpid, status = os.waitpid(-1, os.WNOHANG)
		# if cpid == 0:
		# 	print('no child process was immediately available')
		# 	break
	exitcode = status >> 8
	print('child process %s exit with exitcode %s', cpid, exitcode)
	# except OSError as e:
		# if e.errno == errno.ECHILD:
			# logging.error('current process has no existing unwaited-for child processes.')
		# else:
		# raise


if __name__ == '__main__':
	signal.signal(signal.SIGCHLD, wait_child)
	main()
