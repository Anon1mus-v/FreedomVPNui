from flask import Flask, render_template, jsonify, request
import sys
import os
import webview
import json
import asyncio
import yaml
import requests
import base64
import urllib.parse
from mihomo_manager import MihomoManager
from config_updater import apply_keys_to_mihomo
from parsing import fetch_content, parse_all
from dotenv import load_dotenv

if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

template_folder = os.path.join(base_dir, 'templates')

app = Flask(__name__, template_folder=template_folder, static_folder=template_folder)
mihomo = MihomoManager()
load_dotenv()
raw_urls = os.getenv("URLS")
urls = raw_urls.split(",")
CONFIG_FILE = 'config.json'

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f'Ошибка при загрузке конфигурации: {e}')
            return{}
    return {}

def save_config(data):
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f'Ошибка при сохранении конфигурации: {e}')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['GET', 'POST'])
def start():
    try:
        mihomo.start()
        return jsonify({'status': 'ok'})
    except Exception as e:
        print(f'Ошибка: {e}')
        return jsonify({'status': 'er'})

@app.route('/stop', methods=['GET', 'POST'])
def stop():
    try:
        mihomo.stop()
        return jsonify({'status': 'ok'})
    except Exception as e:
        print(f'Ошибка: {e}')
        return jsonify({'status': 'er'})

@app.route('/update', methods=['GET', 'POST'])
def update():
    try:
        valid_results = asyncio.run(parse_all(urls))
        applied = apply_keys_to_mihomo(valid_results)
        if not valid_results:
            return jsonify({'status': 'no_valid_keys', 'message': 'Нет валидных ключей. Проверьте URL-адреса в .env и доступность источников.'})
        return jsonify({'status': 'ok', 'count': len(valid_results), 'applied': applied})
    except Exception as e:
        print(f'Ошибка: {e}')
        return jsonify({'status': 'er', 'message': str(e)})

@app.route('/api/update-subscription', methods=['POST'])
def update_subscription():
    data = request.get_json()
    sub_url = data.get('url')
    
    if not sub_url:
        return jsonify({'status': 'error', 'message': 'Ссылка не указана.'}), 400
    
    try:
        response = requests.get(sub_url, timeout=10)
        response.raise_for_status()
        config_data = response.text
        decode_bytes = base64.b64decode(config_data)
        decode_text = decode_bytes.decode('utf-8')
        lines = decode_text.splitlines()
        print("Кол-во строк: ",len(lines))
        print("Первые 300 символов текста: \n", decode_text[:300])

        server_list = []
        for line in lines:
            line = line.strip()
            print("Обрабатываем строку:", line[:50])    
            if not line:
                print("Пропущена пустая строка")
                continue
            
            proxy_type = line.split("://")[0] if "://" in line else "unknown"
            if "#" in line:
                raw_name = line.split('#')[1]
                name = urllib.parse.unquote(raw_name)
            else:
                name = "Без Названия"

            server_list.append({
                'name': name,
                'type': proxy_type,
                'link': line
            })
        print("отправлено серверов:", len(server_list))
        config = load_config()
        config['sub_url'] = sub_url
        config['servers'] = server_list
        save_config(config)
        return jsonify({'status': 'success', 'servers': server_list, 'count': len(server_list)})
        
    except Exception as e:
        print("Тип config-data:", type(config_data))
        print("Содержимое: ", config_data)
        return jsonify({'status': 'error', 'message': f'Ошибка при получении данных: {str(e)}'}), 500

@app.route('/api/get-config', methods=['GET'])
def get_config():
    config = load_config()
    return jsonify({'status': 'success', 'config': config})

def run_server():
    app.run(host='127.0.0.1', port=5000)

def run_web():
    webview.create_window('FreedomVPN ui', 'http://127.0.0.1:5000', width=1000, height=800)
    webview.start(run_server, debug=True)