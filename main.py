import time
import asyncio
import os
from dotenv import load_dotenv
from mihomo_manager import MihomoManager
from config_updater import apply_keys_to_mihomo
from parsing import fetch_content
from backend_gui import run_server, run_web
load_dotenv()

raw_urls = os.getenv("URLS")

urls = raw_urls.split(",")
all_keys = []
if __name__ == "__main__":
    mihomo = MihomoManager()
    run_web()
