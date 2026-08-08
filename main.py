import time
import asyncio
import os
from dotenv import load_dotenv
from mihomo_manager import MihomoManager
from config_updater import apply_keys_to_mihomo
from parsing import fetch_content

load_dotenv()

raw_urls = os.getenv("URLS")

urls = raw_urls.split(",")
all_keys = []
if __name__ == "__main__":
    mihomo = MihomoManager()
    if mihomo.start():
        print("Ядро работает 5 сек...")
        for u in urls:
            keys = asyncio.run(fetch_content(u))
            all_keys += keys
        seen = set()
        unique_keys = []
        for item in all_keys:
            seen.add(item['key'])
            unique_keys.append(item)
        apply_keys_to_mihomo(unique_keys)
        time.sleep(5)
        mihomo.stop()
