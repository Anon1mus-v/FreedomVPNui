import requests
import os 
import yaml
from vless_parsing import parse_vless_url

MIHOMO_API_URL = "https://127.0.0.1:9090"

def apply_keys_to_mihomo(valid_results):

    if not valid_results:
        print("Нет валидных ключей")
        return False

    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, 'confing_dir', 'config_yaml')

    parsed_proxie = []
    proxy_names = []

    for item in valid_results:
        vless_url = item['key']
        try:
            proxy_dict = parse_vless_url(vless_url)
            proxy_dict['name'] = f'{proxy_dict["name"]} [{item.get("ping", "?")}ms]'

            parsed_proxie.append(proxy_dict)
            proxy_names.append(proxy_dict['name'])
        except Exception as e:
            print(f'Ошибка конвертации: {e}')
    if not parsed_proxie:
        return False

    config_data = {
        "mixed-port": 7890,
        "allow-lan": False,
        "mode": "rule",
        "log-level": "info",
        "external-controller": "127.0.0.1:9090",
        "tun": {
            "enable": True,
            "stack": "system",
            "auto-route": True,
            "auto-detect-interface": True
        },
        "proxies": parsed_proxie,
        "proxy-groups": [
            {
                "name": "Авто-выбор",
                "type": "url-test",
                "url": "http://www.gstatic.com/generate_204",
                "interval": 300,
                "tolerance": 50,
                "proxies": ["Авто-выбор"] + proxy_names
            },
            {
                "name": "Выбор вручную",
                "type": "select",
                "proxies": ["Авто-выбор"] + proxy_names
            }
        ],
        "rules": [
            "GEOIP,RU,DIRECT",
            "MATCH,Выбор вручную"
        ]
    }
    try:
        response  = requests.put(
            f'{MIHOMO_API_URL}/configs?force=true',
            json={"path": config_path},
            timeout=3
        )
        if response.status_code == 204:
            print(f'Ядро подхватило новый сервер!')
            return True
        else:
            print(f"Mihomo вернул статус: {response.status_code}")
    except Exception as e:
        print(f'Не удалось связаться с ядром: {e}')

    return False