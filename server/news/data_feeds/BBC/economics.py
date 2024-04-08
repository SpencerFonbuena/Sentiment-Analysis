import pandas as pd
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

bbc_sites = ['https://www.bbc.com/business']


class Article(BaseModel):
    url: str
    title: str

''' Process the front page'''
def bbc_econ(url):
    # ScraperAPI magic
    payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': url, 'render': 'true'}
    r = requests.get('https://api.scraperapi.com/', params=payload)
    html_response = r.text
    soup = BeautifulSoup(html_response, 'html.parser') # Parse response
    elements = soup.select('[data-testid="edinburgh-card"]') # Find specific element
    base_url = 'https://www.bbc.com' # Create full Link
    data = []
    for ele in elements:
        child_1 = ele.find('div').find('a')
        child_2 = child_1.find_all('h2')
        try:
            if child_1['href'][:4] != 'http':
                link = base_url + child_1['href']
            else:
                link = child_1['href']
            title = child_2.get_text(strip=True) if child_2 else 'does not contain'
            data.append({'link': link, 'title': title, 'network': 'BBC_Econ'})
        except:
            continue
    
    final_data = pd.DataFrame(data)
    return final_data




