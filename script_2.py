import socket
import sys

# Создание UNIX-сокета
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

try:
    # Подключение к tmux-сокету
    s.connect("/tmp/tmux-100/default")

    # Отправка команды в сокет
    command = "pwd\n"
    s.sendall(command.encode())

    # Получение ответа
    output = ""
    while True:
        data = s.recv(1024).decode()
        if not data:
            break
        output += data

    # Сохранение вывода в файл
    with open("/tmp/bitcoin_key_output.txt", "w") as f:
        f.write("Command output:\n")
        f.write(output)

except Exception as e:
    with open("/tmp/bitcoin_key_output.txt", "w") as f:
        f.write(f"Error: {e}\n")
    sys.exit(1)

finally:
    s.close()