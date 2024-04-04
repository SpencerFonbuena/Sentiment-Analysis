import pandas as pd
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

bi_sites = ['https://www.businessinsider.com/strategy'
            'https://www.businessinsider.com/business',
            'https://www.businessinsider.com/tech',
            'https://www.businessinsider.com/tech'
            ]


class Article(BaseModel):
    url: str
    title: str

''' Process the front page'''
def binsider_econ(url):
    # ScraperAPI magic
    payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': url, 'render': 'true'}
    r = requests.get('https://api.scraperapi.com/', params=payload)
    html_response = r.text
    soup = BeautifulSoup(html_response, 'html.parser') # Parse response
    elements = soup.select('[class="tout-text-wrapper default-tout"]') # Find specific element
    base_url = 'https://www.businessinsider.com' # Create full Link
    data = []
    for ele in elements:
        a_ref = ele.find('h2').find('a')
        child = ele.find('div')
        if a_ref['href'][:4] != 'http':
            link = base_url + a_ref['href']
        else:
            link = a_ref['href']
        title = child.get_text(strip=True) if child else 'does not contain'
        data.append({'link': link, 'title': title, 'network': 'BInsider_Econ'})
    
    final_data = pd.DataFrame(data)
    return final_data


