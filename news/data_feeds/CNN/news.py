import pandas as pd
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

fox_sites = ['https://www.cnn.com/us',
             'https://www.cnn.com/politics',
             'https://www.cnn.com/world']


class Article(BaseModel):
    url: str
    title: str


''' Process the front page'''
def cnn_news(url):
    # ScraperAPI magic
    payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': url, 'render': 'true'}
    r = requests.get('https://api.scraperapi.com/', params=payload)
    html_response = r.text
    soup = BeautifulSoup(html_response, 'html.parser') # Parse response
    elements = soup.select('[class="container__link container__link--type-article container_lead-plus-headlines__link"]') # Find specific element
    base_url = 'https://www.cnn.com' # Create full Link
    data = []
    for ele in elements:
        try:
            child_1 = ele.find('div')
            child_2 = child_1.find('div')
            child_3 = child_2.find('span')
            if ele['href'] != 'http':
                link = base_url + ele['href']
            else:
                link = ele['href']
            title = child_3.get_text(strip=True) if child_3 else 'does not contain'
            data.append({'link': link, 'title': title, 'network': 'CNN_News'})
        except TypeError:
            continue
    
    final_data = pd.DataFrame(data)
    return final_data

