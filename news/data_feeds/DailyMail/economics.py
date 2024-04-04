import pandas as pd
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

bbc_sites = ['https://www.dailymail.co.uk/news/us-economy/index.html',
             'https://www.dailymail.co.uk/yourmoney/index.html']


class Article(BaseModel):
    url: str
    title: str

''' Process the front page'''
def dm_econ(article: Article):
    # ScraperAPI magic
    payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': article.url, 'render': 'true'}
    r = requests.get('https://api.scraperapi.com/', params=payload)
    html_response = r.text
    soup = BeautifulSoup(html_response, 'html.parser') # Parse response
    elements = soup.select('[class="linkro-darkred"]') # Find specific element
    base_url = 'https://www.dailymail.co.uk' # Create full Link
    data = []
    for ele in elements:
        child_1 = ele.find('a')
        try:
            if child_1['href'][:4] != 'http':
                link = base_url + child_1['href']
            else:
                link = child_1['href']
            title = child_1.get_text(strip=True) if child_1 else 'does not contain'
            data.append({'link': link, 'title': title})
        except:
            continue
    
    final_data = pd.DataFrame(data)
    final_data.to_csv('dm_bus.csv', index=False)

'''Process the article and get it ready for sentiment classifier'''
def article_pull(article: Article):
    # Don't render articles. It will come up with many you don't want.
    payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': article.url}
    r = requests.get('https://api.scraperapi.com/', params=payload)
    html_response = r.text

    soup = BeautifulSoup(html_response, 'html.parser')
    text_only = soup.get_text(strip=True)
    return {f'{article.title}': text_only}



