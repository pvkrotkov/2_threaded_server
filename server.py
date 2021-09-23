import socket, threading,sys

def acceptance(conn, addr):

	while True:
		try:
			data = conn.recv(1024)
		except (ConnectionResetError, ConnectionAbortedError):
			print(f'Client {addr} aborted connection')
			raise

		if not data:
			break
		print(f'accepted from {addr}:$ {data.decode()}')
		conn.send(data)
	conn.close()


sys.tracebacklimit = 0
sock = socket.socket()
sock.bind(('', 9090))
sock.listen(0)

while True:
	conn, addr = sock.accept()
	print(f'connected {addr}')
	threading.Thread(target = acceptance, args = (conn, addr), daemon = True).start()




