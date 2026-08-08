import asyncio
import time
import re
from urllib.parse import urlparse
from aiohttp import ClientSession

output_file = 'valid_keys.txt'  # файл для сохранения результатов

valid_keys = []     # список для сохранения рабочих ключей (строки)
valid_results = []  # список объектов {'key':..., 'ping':...}
url = ""  # URL страницы

async def fetch_content(page_url):
    found_keys = []
    try:
        async with ClientSession() as session:
            async with session.get(page_url, timeout=10) as resp:
                if resp.status != 200:
                    raise RuntimeError(f"Не удалось загрузить страницу, статус {resp.status}")
                text = await resp.text()
    except Exception as e:
        # логируем ошибку в файл для exe-версии
        try:
            with open('error.log', 'a', encoding='utf-8') as lf:
                lf.write(f"Ошибка загрузки страницы: {e}\n")
        except Exception:
            pass
        return

    # Собираем vless ключи (без кавычек/<>/пробелов)
    pattern = r"vless://[^\s'\"<>]+"
    found_keys = re.findall(pattern, text)

    async def key_check(key):
        try:
            address = urlparse(key)
            host = address.hostname
            port = address.port if address.port else 443

            start = time.perf_counter()
            reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout=3)
            end = time.perf_counter()

            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass

            ping_ms = int((end - start) * 1000)
            valid_keys.append(key)
            valid_results.append({'key': key, 'ping': ping_ms})
        except Exception:
            return

    tasks = [key_check(k) for k in found_keys]
    if tasks:
        await asyncio.gather(*tasks)

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for k in valid_keys:
                f.write(k + '\n')
    except Exception:
        pass

    return valid_results

if __name__ == '__main__':
    asyncio.run(fetch_content(url))