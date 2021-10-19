import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = input("Enter server's ip-address: ")
port = int(input("Enter server's port number: "))
name = input("Enter your name: ")

sock.connect((host, port))
sock.send(name.encode())
# Прошла ли авторизация
flag = False
# Клиент подключён
connection = True


def authorization(sock, data):
	global flag
	if not flag:
		data = data.split('|')
		print(data[0] + data[2] + data[3])
		if data[1] == "0003":
			passwd = input("Create password: ")
			sock.send(passwd.encode())
			flag = True
		elif data[1] == "0002":
			passwd = input("Enter password: ")
			sock.send(passwd.encode())
		elif data[1] == "0001":
			flag = True


def receive(sock):
	global flag
	global connection
	while True:
		if connection:
			data = sock.recv(1024)
			if not flag:
				authorization(sock, data.decode())
			else:
				print(data.decode())
		else:
			break
	sock.close()


def send_message(sock):
	global flag
	global connection
	msg = ""
	while msg != "exit":
		if flag:
			msg = input('You: ')
			sock.send(msg.encode())
	connection = False


receiveThread = threading.Thread(target=receive, args=[sock])
sendThread = threading.Thread(target=send_message, args=[sock])

receiveThread.start()
sendThread.start()

receiveThread.join()
sendThread.join()

sock.close()
