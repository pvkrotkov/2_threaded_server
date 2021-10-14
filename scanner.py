import threading, socket
counting = 0
ip = input('Введите ip адрес сканируемого существа: ')
num = 4369
ports = []
opens = []

def scaner(rng):
    """
    Принимает список номеров портов в int
    """
    global ports
    global opens
    for i in rng:

        sock = socket.socket()
        sock.settimeout(0.5)
        # sock.setblocking(1)
        try:
            sock.connect((ip, i))
        except ConnectionRefusedError:
            ports.append(1)
            continue
        except:
            # print('open port: ',i)
            ports.append(1)
            opens.append(i)

def create_potok(num):#всего потоков 4369
    f=1
    shag=int(65535/num)

    potoki={}
    for i in range(num):
        spisok=[]
        for port in range(f, f + shag):
            spisok.append(port)

        potoki[f"potok_{i}"] = threading.Thread(target = scaner, args = (spisok,), name=f"potok_{i}")#Создание сокетов по номерам с вызовом функции scaner
        print(f'thread potok_{i} had been created with {spisok} in it')
        f+=15
    for id,_ in potoki.items():
        potoki[id].start()
        print(f'thread {id} had been started ')

def processing():#Заполнение шкалы прогресса
    global counting
    while True:
        procent = len(ports)/65535
        procent *= 100
        round(procent)
        if procent > counting:
            counting += 10
            print('█', end = '')
            if counting >= 100:
                break

def work():
    create_potok(num)
    processing()
    print()
    print(opens)

work()
print('thx for using me')
