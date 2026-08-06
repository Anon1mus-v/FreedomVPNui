import subprocess
import os
import sys
import atexit
import time

class MihomoManager:
    def __init__(self):
        # Находим базовую папку проекта
        if getattr(sys, 'frezen', False):
            self.base_dir = sys._MEIPASS
        else:
            self.base_dir = os.path.dirname(os.path.abspath(__file__))

        self.exe_path = os.path.join(self.base_dir, 'bin', 'mihomo.exe')
        self.config_dir = os.path.join(self.base_dir, 'config_dir')
        self.config_file = os.path.join(self.config_dir, 'config.yaml')

        self.process = None
    def start(self):
        # Запускаем процесс mihomo.exe
        if not os.path.exists(self.exe_path):
            print(f'Ошибка: Файл {self.exe_path} не найден.')
            return False
        # Команда запускает mihomo.exe
        cmd = [
            self.exe_path,
            '-d', self.config_dir,
            '-f', self.config_file,
        ]
        
        try:
            # Запускаем в фоновом режиме
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            print(f"Ядро Mihomo запущено!")
            #Завершение процесса при выходе
            atexit.register(self.stop)
            return True
        except Exception as e:
            print(f"Ошибка при запуске Mihomo: {e}")
            return False
    def stop(self):
        #Останавливаем mihomo.exe
        if self.process and self.process.poll() is None:
            print(f"Остановка mihomo...")
            self.process.terminate()
            try:
                self.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.process.kill()
            print(f"Ядро остановлено")