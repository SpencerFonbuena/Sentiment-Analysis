import pandas as pd
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

ap_sites = ['https://apnews.com/politics',
            'https://apnews.com/us-news']


class Article(BaseModel):
    url: str
    title: str
    
''' Process the front page'''
def ap_news(url):
    # ScraperAPI magic
    payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': url, 'render': 'true'}
    r = requests.get('https://api.scraperapi.com/', params=payload)
    html_response = r.text
    soup = BeautifulSoup(html_response, 'html.parser') # Parse response
    elements = soup.select('[class="PagePromo-title"]') # Find specific element
    base_url = 'https://www.apnews.com' # Create full Link
    data = []
    for ele in elements:
        a_ref = ele.find('a')
        child_1 = a_ref.find('span')
        if a_ref['href'][:4] != 'http':
            link = base_url + a_ref['href']
        else:
            link = a_ref['href']
        title = child_1.get_text(strip=True) if child_1 else 'does not contain'
        data.append({'link': link, 'title': title, 'network': 'AP_News'})
    
    final_data = pd.DataFrame(data)
    return final_data


