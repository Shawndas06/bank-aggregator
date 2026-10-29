"""Verify the running production images, not source-mounted development servers."""
import json
import re
import subprocess
from urllib.request import urlopen


def get(path):
    with urlopen('http://127.0.0.1:8080' + path, timeout=15) as response:
        return response.read(), response.headers.get('Content-Type', '')


with urlopen('http://127.0.0.1:8000/health', timeout=15) as response:
    data = json.load(response)['data']
    assert data['api'] == data['redis'] == 'healthy', data
html, kind = get('/')
assert 'text/html' in kind and b'id="root"' in html
assets = re.findall(rb'(?:src|href)="(/assets/[^"?]+)', html)
assert assets, 'Build produced no linked assets'
for asset in assets:
    body, kind = get(asset.decode())
    assert body and 'text/html' not in kind, (asset, kind)
route, _ = get('/accounts')
assert route == html, 'SPA fallback failed'
for service in ('backend', 'frontend'):
    subprocess.run([
        'docker', 'compose', '-f', 'compose.ci.yml', 'exec', '-T', service,
        'sh', '-ec',
        'test ! -f /app/.env; test ! -d /app/.git; test ! -d /app/.codex; test ! -f /app/AGENTS.md',
    ], check=True)
print('API, Redis, production assets, SPA fallback and image contents passed')
