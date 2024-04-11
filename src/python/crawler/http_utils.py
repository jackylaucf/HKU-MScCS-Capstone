import requests


def get(url: str, not_ok_exception=True) -> requests.Response:
    print(f'HTTP GET: {url}')
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0'}
    response = requests.get(url, headers=headers)
    if not_ok_exception and not response.ok:
        raise requests.HTTPError(f'HTTP Error ({response.status_code})')
    return response
