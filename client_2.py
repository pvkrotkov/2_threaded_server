import socket


sock = socket.socket()

sock.connect(('localhost', 6555))
while True:
    #msg = input()
    msg = input('...')
    sock.send(msg.encode())

    data = sock.recv(1024)

    print(data.decode())
