import time
from mihomo_manager import MihomoManager
from config_updater import apply_keys_to_mihomo

if __name__ == "__main__":
    mihomo = MihomoManager()
    if mihomo.start():
        print("Ядро работает 5 сек...")
        apply_keys_to_mihomo([
            {'key': 'vless://7c74b0e4-f132-5583-4692-622a7d6b71a4@88.218.44.4:993?security=reality&amp;type=tcp&amp;flow=xtls-rprx-vision&amp;sni=download.nvidia.com&amp;fp=chrome&amp;pbk=EG3y7UktGRlzSZZ2oXT_YaO2gVP4ca3Xe6AQ0u9A5DQ#yavpn_robot', 'ping': 120},
            {'key': 'vless://e2f6a9b4-84c1-4b11-9a72-3c224b1f6d34@nl.secure-tunnel.org:8443?type=grpc&security=reality&sni=yahoo.com&pbk=i7Xb8_Hk9z2Wv4mP0lQsR9-A6cB7dE1fG2hI3jK4lM5&serviceName=vless-grpc#NL-Amsterdam-Reality', 'ping': 150}
        ])
        time.sleep(5)
        mihomo.stop()