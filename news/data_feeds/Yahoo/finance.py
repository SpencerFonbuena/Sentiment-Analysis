import pandas as pd
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

yahoo_sites = ['https://finance.yahoo.com/bidenomics/',
               'https://finance.yahoo.com/topic/stock-market-news/',
               'https://finance.yahoo.com/topic/economic-news/',
               'https://finance.yahoo.com/topic/earnings/',
               'https://finance.yahoo.com/topic/crypto/',
               'https://finance.yahoo.com/live/politics/',
               'https://finance.yahoo.com/bidenomics/']


class Article(BaseModel):
    url: str
    title: str


''' Process the front page'''
def yf_econ(article: Article):
    # ScraperAPI magic
    payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': article.url, 'render': 'true'}
    r = requests.get('https://api.scraperapi.com/', params=payload)
    html_response = r.text

    soup = BeautifulSoup(html_response, 'html.parser') # Parse response
    elements = soup.select('[class="Mb(5px)"]') # Find specific element
    base_url = 'https://finance.yahoo.com' # Create full Link
    data = []
    for ele in elements:
        a_tag = ele.find('a')
        link = base_url + a_tag['href']
        title = a_tag.get_text(strip=True)
        data.append({'link': link, 'title': title})
    
    final_data = pd.DataFrame(data)
    final_data.to_csv('test.csv', index=False)

'''Process the article and get it ready for sentiment classifier'''
def article_pull(article: Article):
    # Don't render articles. It will come up with many you don't want.
    payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': article.url}
    r = requests.get('https://api.scraperapi.com/', params=payload)
    html_response = r.text

    soup = BeautifulSoup(html_response, 'html.parser')
    text_only = soup.get_text(strip=True)
    return {f'{article.title}': text_only}

    