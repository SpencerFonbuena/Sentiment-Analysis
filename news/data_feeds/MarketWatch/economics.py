import pandas as pd
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

ap_sites = ['https://www.marketwatch.com/economy-politics/federal-reserve?mod=economy-politics',
            'https://www.marketwatch.com/economy-politics?mod=top_nav',
            'https://www.marketwatch.com/investing?mod=top_nav',
            'https://www.marketwatch.com/',
            'https://www.marketwatch.com/investing/stocks?mod=investing',
            'https://www.marketwatch.com/investing/barrons?mod=stocks',
            'https://www.marketwatch.com/markets/earnings?mod=barrons-on-marketwatch',
            'https://www.marketwatch.com/markets/us?mod=earnings',
            'https://www.marketwatch.com/market-data/asia?mod=currencies-market-data',
            'https://www.marketwatch.com/market-data/rates?mod=asia-market-data'
            ]

''' Process the front page'''
def mw_econ(url):
    # ScraperAPI magic
    payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': url, 'render': 'true'}
    r = requests.get('https://api.scraperapi.com/', params=payload)
    html_response = r.text
    soup = BeautifulSoup(html_response, 'html.parser') # Parse response
    elements = soup.select('[class="article__headline"]') # Find specific element
    base_url = 'https://www.marketwatch.com' # Create full Link
    data = []
    for ele in elements:
        a_ref = ele.find('a')
        if a_ref['href'][:4] != 'http':
            link = base_url + a_ref['href']
        else:
            link = a_ref['href']
        title = a_ref.get_text(strip=True) if a_ref else 'does not contain'
        data.append({'link': link, 'title': title, 'network': 'Mw_Econ'})
    
    final_data = pd.DataFrame(data)
    return final_data


