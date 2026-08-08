from flask import Flask, render_template, jsonify
import sys
import os
import webview
import json
from mihomo_manager import MihomoManager
from config_updater import apply_keys_to_mihomo

if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

template_folder = os.path.join(base_dir, 'templates')

app = Flask(__name__, template_folder=template_folder, static_folder=template_folder)
mihomo = MihomoManager()

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
        apply_keys_to_mihomo()
        return jsonify({'status': 'ok'})
    except Exception as e:
        print(f'Ошибка: {e}')
        return jsonify({'status': 'er'})

if __name__ == "__main__":
    webview.create_window('FreedomVPN ui', 'http://127.0.0.1:5000', width=1000, height=800)
    webview.start(app)