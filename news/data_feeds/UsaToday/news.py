import pandas as pd
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

bbc_sites = ['https://www.usatoday.com/news/nation/']


class Article(BaseModel):
    url: str
    title: str

''' Process the front page'''
def usat_news(article: Article):
    # ScraperAPI magic
    payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': article.url, 'render': 'true'}
    r = requests.get('https://api.scraperapi.com/', params=payload)
    html_response = r.text
    soup = BeautifulSoup(html_response, 'html.parser') # Parse response
    elements = soup.select('[class="gnt_m_flm_a"]') # Find specific element
    base_url = 'https://www.usatoday.com' # Create full Link
    data = []
    for ele in elements:

        if ele['href'][:4] != 'http':
            link = base_url + ele['href']
        else:
            link = ele['href']
        title = ele.get_text(strip=True) if ele else 'does not contain'
        print(link, title)
        data.append({'link': link, 'title': title})

    
    final_data = pd.DataFrame(data)
    final_data.to_csv('usat_news.csv', index=False)

'''Process the article and get it ready for sentiment classifier'''
def article_pull(article: Article):
    # Don't render articles. It will come up with many you don't want.
    payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': article.url}
    r = requests.get('https://api.scraperapi.com/', params=payload)
    html_response = r.text

    soup = BeautifulSoup(html_response, 'html.parser')
    text_only = soup.get_text(strip=True)
    return {f'{article.title}': text_only}
