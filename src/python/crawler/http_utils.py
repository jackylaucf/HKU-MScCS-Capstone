import requests


def get(url: str, not_ok_exception=True) -> requests.Response:
    print(f'HTTP GET: {url}')
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if not_ok_exception and not response.ok:
        raise requests.HTTPError(f'HTTP Error ({response.status_code})')
    return response
