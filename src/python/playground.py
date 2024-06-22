import requests

url = 'https://www.niftyindices.com/IndexConstituent/ind_{ticker}list.csv'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
           }
session = requests.Session()
response = session.get('https://www.niftyindices.com/IndexConstituent/ind_niftymidcap100list.csv', headers=headers)
print(response.text)
