import os
import subprocess
import shutil
import zipfile
import configparser
from datetime import datetime
import calendar

# Функция для выполнения команды в командной строке
def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return str(e)

# Функция для создания виртуальной файловой системы из zip-архива
def create_virtual_fs(zip_path):
    extract_path = "/tmp/virtual_fs"
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    return extract_path

def display_calendar():
    return calendar.month(2024, 12)

# Функция для выполнения стартового скрипта
def run_startup_script(script_path):
    if os.path.exists(script_path):
        with open(script_path, 'r') as script_file:
            commands = script_file.read().split("\n")
            for command in commands:
                if command == "cal":
                    print(display_calendar())
                elif command == "ls":
                    print("\n".join(os.listdir(current_path)))

# Загрузка конфигурации
config = configparser.ConfigParser()
config.read('C:/Users/Pro10/Desktop/dz1/config.ini')

username = config['settings']['username']
hostname = config['settings']['hostname']
virtual_fs_zip = config['settings']['virtual_fs_zip']
startup_script_path = config['settings']['startup_script']

# Создание виртуальной файловой системы
current_path = create_virtual_fs(virtual_fs_zip)

# Выполнение стартового скрипта
run_startup_script(startup_script_path)

# Основной цикл для обработки команд
while True:
    command = input(f"{username}@{hostname}:{current_path}> ")
    
    if command == "exit":
        break
    elif command.startswith("cd "):
        new_path = os.path.join(current_path, command[3:].strip())
        if os.path.isdir(new_path):
            current_path = new_path
        else:
            print("Directory not found")
    elif command == "ls":
        print("\n".join(os.listdir(current_path)))
    elif command == "cal":
        print(display_calendar())
    elif command.startswith("touch "):
        filename = command[6:].strip()
        open(os.path.join(current_path, filename), 'a').close()
        print(f"File '{filename}' created.")
    else:
        print("Unknown command")