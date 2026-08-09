from flask import Flask, render_template, jsonify
import sys
import os
import webview
import json
import asyncio
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

def run_server():
    app.run(host='127.0.0.1', port=5000)

def run_web():
    webview.create_window('FreedomVPN ui', 'http://127.0.0.1:5000', width=1000, height=800)
    webview.start(run_server)