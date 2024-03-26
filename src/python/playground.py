import requests

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
req = requests.get('https://query1.finance.yahoo.com/v7/finance/download/%5EHSI?period1=536371200&period2=1711324800&interval=1d&events=history&includeAdjustedClose=true', headers=headers)
print(req.text )