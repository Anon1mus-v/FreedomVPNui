import yaml
from vless_parsing import parse_vless_url
def generate_mihomo_config(vless_links: list, output_path: str):
    proxies = []
    proxy_names = []

    for link in vless_links:
        try:
            parsed = parse_vless_url(link)
            if parsed:
                proxies.append(parsed)
                proxy_names.append(parsed['name'])
        except Exception as e:
            print(f"Ошибка парсинга ссылки: {e}")

    if not proxies:
        print("Предупреждение: Список прокси пуст!")
        return False

    config_data = {
        'port': 7890,
        'socks-port': 7891,
        'allow-lan': False,
        'mode': 'rule',
        'log-level': 'info',
        'external-controller': '127.0.0.1:9090',  # REST API управления Mihomo
        'secret': '',
        'tun': {
            'enable': True,
            'stack': 'system',
            'auto-route': True,
            'auto-detect-interface': True
        },
        'proxies': proxies,
        'proxy-groups': [
            {
                'name': 'Freedom-Group',
                'type': 'select',
                'proxies': proxy_names
            }
        ],
        'rules': [
            'GEOIP,LAN,DIRECT',
            'MATCH,Freedom-Group'
        ]
    }

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f, allow_unicode=True, sort_keys=False)
        print(f"Конфигурация успешно сохранена в {output_path}")
        return True
    except Exception as e:
        print(f"Ошибка при записи config.yaml: {e}")
        return False