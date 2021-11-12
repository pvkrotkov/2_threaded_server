import socket
import re
from threading import Thread, Lock
from queue import Queue


# Функция реализовання для получения адреса хоста с клавиатуры
def get_host():
    # Пишем цикл вечного запроса от пользователя ввести адрес, пока не он не введёт правильно
    while True:
        # Получим адрес хоста
        host = input('Enter host IP: ')
        # При помощи регулярки ищем 4 числа через точку от 1 до 3 разрядов каждое из которых присоединено
        # к началу и концу строки, если такое находим, то все хорошо, польователь ввел правильно
        if re.match(r'^(\d{1,3}\.){3}\d{1,3}$', host):
            # Выход из функции, возвращая введенный хост
            return host
        else:
            # Если пользователь ввёл неправильно, скажем об этом и попросим ввести еще раз
            print('Invalid IP, try again!')



def port_scanner(port, host):
    global print_lock, open_ports, locked_ports, forbidden_access_method_ports
    # Создадим объект TCP сокета
    sock = socket.socket()
    # Попытка подключения его к порту
    try:
        sock.connect((host, port))
    except:
        # Если соединение прервано, то порт закрыт и мы не смогли к нему присоединиться
        # Также добавим его в список закрытых портов, заблокировав работу с переменной для других потоков
        with print_lock:
            locked_ports.append(port)


    #10055 слишком много потоков, буфер переполнился все упадет в ошибку
    #10013 не тот метод доступа
    #10060 не получен нужный отклик за требуемое время

    else:
        # Если получилось подключиться, то добавим в список отрытых портов
        with print_lock:
            open_ports.append(port)
    finally:
        # В любом случае закроем созданный сокет
        sock.close()


def scan_thread(host):
    global ports_queue
    # Пишем цикл вечного получения номера портов из очереди
    while True:
        # Если портов в очереди нет, поток ожидает вечно порт в очереди (но он уничтожится с уничтожением основного, так как это демон)
        current_port = ports_queue.get()
        # Запускаем функцию проверки порта
        port_scanner(current_port, host)
        # После проверки порта говорим очереди, что одно задание сделано, чтобы в конечном итоге разблокировать основной поток
        ports_queue.task_done()


def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    # Делаем форматный вывод для количества, обработанного в процентах
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    # Вычисляем сколько символов нужно выводить заполненными (важно целое число)
    filledLength = int(length * iteration // total)
    # Делаем заполнение самой полосы символами заполнения и пустоту символами дефис
    bar = fill * filledLength + '-' * (length - filledLength)
    # Выводим саму строку, правильно форматируя
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Если достигли конца (100%), то переводим на новую строку
    if iteration == total: 
        print()


def progress_bar():
    global PORTS_COUNT, START_PORT, ports_queue
    # Пишем цикл вечного вывода на экран прогресс бар
    while True:
        # Вычислим общее количество портов на основе наших заданных постоянных
        total = PORTS_COUNT-START_PORT
        # Вычислим текущее количество портов методом объекта очереди Queue
        cnt = ports_queue.qsize()
        # Вычислим кол-во обработанных портов
        processed = total - cnt
        # Передадим в функцию, непосредственно печатающую прогресс бар
        printProgressBar(processed, total, ' Scanning:', length = 70)
        # Если количество необработанных 0, то завершим наш цикл, а поток умрет со смертью основного потока
        if not cnt:
            break
    

def scanning(host, ports):
    global ports_queue, TREADS_NUMBER
    # Заполняем нашу очередь номерами портов
    for port_number in ports:
        ports_queue.put(port_number)
    # Создаем поток для прогресс бара и делаем его демоном
    Thread(target=progress_bar, daemon = True).start()
    # Начинаем создавать указанное в постоянной в начале количество потоков с целью - функцией scan_tread
    for _ in range(TREADS_NUMBER):
        Thread(target=scan_thread, args = [host], daemon = True).start()
    # После того, как создали все потоки, блокируем дальнейшее выполнение программы методом объекта Queue
    # В таком случае, он разблокируется когда получит количество .task_done() равное количеству .get()
    ports_queue.join()   



# Получим хост у пользователя
host = get_host()
# При тестировании я искал на своём IP, поэтому просто присваивал переменной, а не получал input
# host = '192.168.1.69'
# Считаем максимальное количество портов (+1 максимального значения номера порта)
PORTS_COUNT = 2**16
# Задаем начальный порт
START_PORT = 1
# Устанавливаем количество потоков (тут главное не переборщить)
TREADS_NUMBER = 15000
# Создаем списочек объектом Queue, чтобы потом работать до тех пор, пока не просканируем все порты
ports_queue = Queue()
# Создаем объект Lock библиотеки treading, чтобы блокировать вывод и доступ к переменным
print_lock = Lock()
# Создаем лист номеров портов
ports_list = [i for i in range(START_PORT,PORTS_COUNT)]
# Сюда будем записывать открытые порты
open_ports = []
# Сюда будем записывать закрытые порты
locked_ports = []
# Запускаем основную функцию сканирования, смотрим в нее
scanning(host, ports_list)
# Выполнение кода после этой строки не продолжится, пока не разблокируем основной поток
# Отсортируем все два списка портов
open_ports.sort()
locked_ports.sort()
# Печатаем только открытые порты
print('Open ports:', '; '.join([str(i) for i in open_ports]))
