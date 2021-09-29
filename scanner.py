import socket
import re
from threading import Thread, Lock
from queue import Queue


# функция получения адреса хоста с клавиатуры
def get_host():
    # будем вечно просить от пользователя ввести адрес, пока не введет правильно
    while True:
        # получаем (возможно верный) адрес хоста
        host = input('Enter host IP: ')
        # с помощью регулярки ищем 4 числа через точку от 1 до 3 разрядов каждое которое присоединено
        # к началу и концу строки, если такое находим, то все хорошо, польователь ввел правильно
        if re.match(r'^(\d{1,3}\.){3}\d{1,3}$', host):
            # выходим из функции возвращая введенный хост
            return host
        else:
            # если ввел неправильно, скажем об этом и попросим ввести еще раз и еще много много раз
            print('Invalid IP, try again!')



def port_scanner(port, host):
    global print_lock, open_ports, locked_ports, forbidden_access_method_ports
    # создаем объект TCP сокета
    sock = socket.socket()
    # пытаемся приконнектить его к порту
    try:
        sock.connect((host, port))
    except:
        # если соединение прервано, то порт закрыт и мы не смогли к нему присоединиться
        # добавим его в список закрытых портов, заблокировав работу с переменной для других потоков
        with print_lock:
            locked_ports.append(port)


    #10055 слишком много потоков, буфер переполнился все упадет в ошибку
    #10013 не тот метод доступа
    #10060 не получен нужный отклик за требуемое время

    else:
        # если получилось подключиться, то добавим в список отрытых портов
        with print_lock:
            open_ports.append(port)
    finally:
        # в любом случае закроем созданный сокет
        sock.close()


def scan_thread(host):
    global ports_queue
    # начинаем бесконечно получать номера портов из очереди
    while True:
        # если портов в очереди нет, поток ожидает вечно порт в очереди (но он уничтожится с уничтожением основного, ведь это демон)
        current_port = ports_queue.get()
        # запускаем функцию проверки порта
        port_scanner(current_port, host)
        # после проверки порта говорим очереди что одно задание сделано, чтобы в конечном итоге разблокировать основной поток
        ports_queue.task_done()


def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    # деламе форматный вывод для количества обработанного в процентах
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    # вычисляем сколько символов выводить заполненными (важно целое число)
    filledLength = int(length * iteration // total)
    # делаем заполнение самой полосы символами заполнения и пустоту символами дефис
    bar = fill * filledLength + '-' * (length - filledLength)
    # выводим саму строку правильно форматируя
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # если достигли конца (100%) то переведем каретку на новую строку
    if iteration == total: 
        print()


def progress_bar():
    global PORTS_COUNT, START_PORT, ports_queue
    # бесконечно будем выводить на экран прогресс бар
    while True:
        # вычисляем общее количество портов на основе наших заданных постоянных
        total = PORTS_COUNT-START_PORT
        # вычисляем текущее количество портов методом объекта очереди Queue
        cnt = ports_queue.qsize()
        # вычисляем кол-во обработанных портов
        processed = total - cnt
        # передаем в функцию, непосредственно печатающую прогресс бар
        printProgressBar(processed, total, ' Scanning:', length = 70)
        # если количество необработанных 0, то завершим наш цикл, а поток умрет со смертью основного потока
        if not cnt:
            break
    

def scanning(host, ports):
    global ports_queue, TREADS_NUMBER
    # заполняем нашу очередь номерами портов
    for port_number in ports:
        ports_queue.put(port_number)
    # создаем поток для прогресс бара и делаем его демоном
    Thread(target=progress_bar, daemon = True).start()
    # начинаем создавать указанное в постоянной в началае количество потоков с целью - функцией scan_tread
    for _ in range(TREADS_NUMBER):
        Thread(target=scan_thread, args = [host], daemon = True).start()
    # после того как создали все потоки блокируем дальнейшее выполнение программы методом объекта Queue
    # в таком случае он разблокируется когда получит количество .task_done() равное количеству .get()
    ports_queue.join()   



# получаем хост у пользователя
host = get_host()
#  при тестировании я искал на своем же IP поэтому просто присваивал переменной, а не получал input
# host = '192.168.1.39'
# считаем макс количество портов (+1 макс значения номера порта)
PORTS_COUNT = 2**16
# задаем начальный порт
START_PORT = 1
# устанавливаем количество потоков (тут главное не переборщить)
TREADS_NUMBER = 15000
# создаем списочек объектом Queue чтобы потом работать до тех пор, пока не просканируем все порты
ports_queue = Queue()
# создаем объект Lock библиотеки treading чтобы блокировать вывод и доступ к переменным, иначе каша
print_lock = Lock()
# создаем лист номеров портов
ports_list = [i for i in range(START_PORT,PORTS_COUNT)]
# сюда будем записывать открытые порты
open_ports = []
# сюда будем записывать закрытые порты
locked_ports = []


# запускаем основную функцию сканирования, смотрим в нее
scanning(host, ports_list)

# выполнение кода после этой строки не продолжится, пока не разблокируем основной поток
# отсортируем все два списка портов
open_ports.sort()
locked_ports.sort()
# напечатаем только открытые порты
print('Open ports:', '; '.join([str(i) for i in open_ports]))