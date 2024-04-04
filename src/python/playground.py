import requests

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/39.0.2171.95 Safari/537.36', 'Origin': 'https://www.investing.com', 'Referer': 'https://www.investing.com', 'Access-Control-Allow-Origin': '*'}

response = requests.get('https://api.investing.com/api/financialdata/historical/997941?start-date=2024-02-07&end-date=2024-04-04&time-frame=Daily&add-missing-rows=false', headers=headers)

print(response.text)