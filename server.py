import socket
from threading import *

max = 100
list_thread = []


class ClientSock(Thread):

    def __init__(self, name, connector):
        Thread.__init__(self)
        self.name = name
        self.connector = connector

    def n(self):
        return self.name

    def run(self):
        while True:
            data = self.connector.recv(1024)
            if not data:
                break
            print(data.decode())
            self.connector.send(data)


sock = socket.socket()
sock.bind(('', 10000))
sock.listen(4)
while True:
    conn, addr = sock.accept()
    thread = ClientSock(len(list_thread), conn)
    list_thread.append(thread if len(list_thread) <= max else Exception)
    thread.start()
