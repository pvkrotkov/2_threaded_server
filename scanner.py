import socket
from sys import *
from threading import *


addr = input('enter address or host name: ')
max = 4
open_ports = []
ports = []
answer = []
to = 1000
fr = 1


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):

    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


class Threads(Thread):

    def __init__(self, name, addr):
        Thread.__init__(self)
        self.name = name
        self.addr = addr

    def run(self):
        for port in range(fr + int(self.name), to, max):
            with socket.socket() as s:
                try:
                    s.connect((self.addr, port))
                    open_ports.append(port)
                except:
                    continue
                finally:
                    ports.append(None)
        answer.append(None)


def prog():
    while True:
        if len(ports) != to - fr:
            printProgressBar(len(ports), (to - fr), prefix='Progress:',
                             suffix='Complete', length=50)
        elif len(ports) == to - fr:
            printProgressBar(len(ports), (to - fr), prefix='Progress:',
                             suffix='Complete', length=50)
            break


for i in range(max):
    thread = Threads(i, addr)
    thread.start()

prog()

while True:
    if len(answer) == 4:
        open_ports = sorted(open_ports) if len(
            open_ports) != 0 else 'Open ports dont exist'
        if type(open_ports) == str:
            print(open_ports)
        else:
            for i in open_ports:
                print(f'Port {i} is opened')
        print(len(ports))
        break
    else:
        continue
