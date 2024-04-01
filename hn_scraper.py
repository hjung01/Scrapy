import requests
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
# r = requests.get(rf'https://www.harveynorman.co.nz/whiteware/refrigeration/?', headers=HEADERS)
# soup = BeautifulSoup(r.content, "html.parser")
# print(soup)
# p = soup.find_all('span', {'class': 'price-num'})
# print(len(p))

with requests.Session() as session:
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    })

    response = session.get('https://www.harveynorman.co.nz/whiteware/refrigeration/?', headers=HEADERS)

    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup)
    prices = soup.find_all('span', {'class': 'price-num'})
    print(response.url)
    print(len(prices))