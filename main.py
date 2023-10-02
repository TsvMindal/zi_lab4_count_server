import socket

# Порт, на котором будет работать сервер
SERVER_COUNT_PORT = 5000

# Функция для обработки подключения клиента
def handle_connection(conn, choice_counters):
    with conn:
        try:
            # Получение данных от клиента
            data = conn.recv(1024)
            if data:
                msg = data.decode('utf-8')
                # Проверка выбора клиента и увеличение счетчика голосов
                if msg in choice_counters:
                    choice_counters[msg] += 1
                    print(f"Количество голосов за кандидата {msg}: {choice_counters[msg]}")
                else:
                    print("Недопустимый выбор.")
        except ConnectionResetError:
            print("Соединение с клиентом потеряно.")

# Словарь для подсчета голосов за кандидатов
choice_counters = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0}

# Создание сокета и привязка к порту
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('localhost', SERVER_COUNT_PORT))
    s.listen(1)

    try:
        while True:
            conn, addr = s.accept()
            # Обработка подключения клиента
            handle_connection(conn, choice_counters)
    except KeyboardInterrupt:
        print("Сервер завершает работу.")
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
