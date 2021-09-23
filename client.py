import socket
from time import sleep

sock = socket.socket()
sock.setblocking(1)
sock.connect(('192.168.1.39', 9090))


while True:
    msg = input()
    sock.send(msg.encode())
    if msg == 'exit':
        break
    data = sock.recv(1024)
    print(f'accepted from server:$ {data.decode()}')

sock.close()
