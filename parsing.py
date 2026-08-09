import asyncio
import time
import re
from urllib.parse import urlparse
from aiohttp import ClientSession

output_file = 'valid_keys.txt'  # файл для сохранения результатов

valid_keys = []     # список для сохранения рабочих ключей (строки)
valid_results = []  # список объектов {'key':..., 'ping':...}
url = ""  # URL страницы


def reset_valid_data():
    global valid_keys, valid_results
    valid_keys = []
    valid_results = []


def normalize_urls(raw_urls):
    if not raw_urls:
        return []

    if isinstance(raw_urls, str):
        raw_urls = [raw_urls]

    normalized = []
    for item in raw_urls:
        if item is None:
            continue
        for part in str(item).split(','):
            candidate = part.strip()
            if candidate:
                normalized.append(candidate)
    return normalized


async def fetch_content(page_url):
    if not page_url:
        return

    try:
        async with ClientSession() as session:
            async with session.get(page_url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'}) as resp:
                if resp.status != 200:
                    raise RuntimeError(f"Не удалось загрузить страницу, статус {resp.status}")
                text = await resp.text()
    except Exception as e:
        try:
            with open('error.log', 'a', encoding='utf-8') as lf:
                lf.write(f"Ошибка загрузки страницы {page_url}: {e}\n")
        except Exception:
            pass
        return

    pattern = r"vless://[^\s'\"<>]+"
    found_keys = re.findall(pattern, text)

    for key in found_keys:
        try:
            address = urlparse(key)
            host = address.hostname
            port = address.port if address.port else 443

            start = time.perf_counter()
            _, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout=3)
            end = time.perf_counter()

            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass

            ping_ms = int((end - start) * 1000)
            if key not in valid_keys:
                valid_keys.append(key)
                valid_results.append({'key': key, 'ping': ping_ms})
        except Exception:
            continue


async def parse_all(urls):
    reset_valid_data()
    normalized_urls = normalize_urls(urls)
    if not normalized_urls:
        return []

    tasks = [fetch_content(url) for url in normalized_urls]
    if tasks:
        await asyncio.gather(*tasks)

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for k in valid_keys:
                f.write(k + '\n')
    except Exception:
        pass

    return valid_results
