from urllib.parse import urlparse, parse_qs, unquote

def parse_vless_url(vless_url: str) -> dict:
    # Разбираем URL VLESS и возвращаем словарь с его компонентами
    parsed_url = urlparse(vless_url)

    if parsed_url.scheme != 'vless':
        raise ValueError("URL не является VLESS")

    uiid = parsed_url.username
    server = parsed_url.hostname
    port = parsed_url.port

    params = parse_qs(parsed_url.query)

    name = unquote(parsed_url.fragment) if parsed_url.fragment else f"Vless-{server}:{port}"

    security = params.get('security', [''])[0]
    is_tls = security in ['tls', 'reality']

    proxy = {
        "name": name,
        "type": "vless",
        "server": server,
        "port": port,
        "uuid": uiid,
        "udp": True,
        "tls": is_tls,
        "skip-cert-verify": True
    }

    network = params.get('type', ['tcp'])[0]
    proxy["network"] = network

    if network == 'ws':
        ws_opts = {}
        if 'path' in params:
            ws_opts['path'] = params['path'][0]
        if 'host' in params:
            ws_opts['headers'] = {'Host': params['host'][0]}
        if ws_opts:
            proxy['ws-opts'] = ws_opts

    if security == 'reality':
        reality_opts = {}

        pbk = params.get('pbk') or params.get('pub')
        if pbk:
            reality_opts['public-key'] = pbk[0]
        sid = params.get('sid') or params.get('shor')
        if sid:
            reality_opts['short-id'] = params['shor'][0]
        if reality_opts:
            proxy['reality-opts'] = reality_opts

    if 'sni' in params:
        proxy['servername'] = params['sni'][0]
    elif 'host' in params:
        proxy['servername'] = params['host'][0]

    if "flow" in params:
        proxy["flow"] = params["flow"][0]

    return proxy

if __name__ == "__main__":
    test_url = "vless://uuid@server:443?type=ws&security=tls&host=example.com&path=/ws#MyVless"
    result = parse_vless_url(test_url)
    import pprint
    pprint.pprint(result)
