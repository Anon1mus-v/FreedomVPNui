import time
from mihomo_manager import MihomoManager

if __name__ == "__main__":
    mihomo = MihomoManager()
    if mihomo.start():
        print("Ядро работает 5 сек...")
        time.sleep(5)
        mihomo.stop()