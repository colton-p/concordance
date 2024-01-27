import os.path
import urllib.parse

import requests

def url_key(url):
    o = urllib.parse.urlparse(url)

    return '-'.join([
        o.netloc,
        o.path.replace('/', '-').strip('-'),
        o.query.replace('&', '-')
    ])


def cached_get(url, force=False):
    path = f'.cache/{url_key(url)}'
    if os.path.exists(path) and not force:
        return open(path, 'r', encoding='utf8').read()

    print('! get', url)
    result = requests.get(url, timeout=20).text
    with open(path, 'w', encoding='utf8') as fp:
        fp.write(result)
    return result
