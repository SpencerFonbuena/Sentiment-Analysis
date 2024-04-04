import pandas as pd
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

bbc_sites = ['https://www.cbsnews.com/us/',
             'https://www.cbsnews.com/politics/']


class Article(BaseModel):
    url: str
    title: str

''' Process the front page'''
def cbs_news(url):
    # ScraperAPI magic
    payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': url, 'render': 'true'}
    r = requests.get('https://api.scraperapi.com/', params=payload)
    html_response = r.text
    soup = BeautifulSoup(html_response, 'html.parser') # Parse response
    elements = soup.select('[class="item__anchor"]') # Find specific element
    base_url = 'https://www.cbsnews.com' # Create full Link
    data = []
    for ele in elements:
        child_1 = ele.find('div').find('h4')
        try:
            if ele['href'][:4] != 'http':
                link = base_url + ele['href']
            else:
                link = ele['href']
            title = child_1.get_text(strip=True) if child_1 else 'does not contain'
            data.append({'link': link, 'title': title, 'network': 'CBS_News'})
        except:
            continue
    
    final_data = pd.DataFrame(data)
    return final_data

