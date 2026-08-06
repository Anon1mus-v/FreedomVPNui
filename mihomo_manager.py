import subprocess
import os
import sys
import atexit
import time

class MihomoManager:
    def __init__(self):
        #Находим базовую папку проекта
        if getattr(sys, 'frezen', False):
            self.base_dir = sys._MEIPASS
        else:
            self.base_dir(os.path.abspath(__file__))
        