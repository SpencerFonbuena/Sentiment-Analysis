import pandas as pd
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

nbc_sites = ['https://www.nbcnews.com/business',
             'https://www.nbcnews.com/tech-media']


class Article(BaseModel):
    url: str
    title: str

''' Process the front page'''
def nbc_econ(article: Article):
    # ScraperAPI magic
    payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': article.url, 'render': 'true'}
    r = requests.get('https://api.scraperapi.com/', params=payload)
    html_response = r.text
    soup = BeautifulSoup(html_response, 'html.parser') # Parse response
    elements = soup.select('[class="styles_headline__ice3t"]') # Find specific element
    base_url = 'https://www.nbc.com' # Create full Link
    data = []
    for ele in elements:
        try:
            a_ref = ele.find('a')
            if a_ref['href'][:4] != 'http':
                link = base_url + a_ref['href']
            else:
                link = a_ref['href']
            title = a_ref.get_text(strip=True) if a_ref else 'does not contain'
            data.append({'link': link, 'title': title})
        except:
            continue

    elements = soup.select('[class="wide-tease-item__info-wrapper flex-grow-1-m"]') # Find specific element
    for ele in elements:
        try:
            a_ref = ele.find_all('a')
            child_1 = a_ref[1].find('h2')
            if a_ref[1]['href'][:4] != 'http':
                link = base_url + a_ref[1]['href']
            else:
                link = a_ref[1]['href']
            title = child_1.get_text(strip=True) if child_1 else 'does not contain'
            data.append({'link': link, 'title': title})
        except:
            continue
    
    final_data = pd.DataFrame(data)
    final_data.to_csv('nbc_bus.csv', index=False)

'''Process the article and get it ready for sentiment classifier'''
def article_pull(article: Article):
    # Don't render articles. It will come up with many you don't want.
    payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': article.url}
    r = requests.get('https://api.scraperapi.com/', params=payload)
    html_response = r.text

    soup = BeautifulSoup(html_response, 'html.parser')
    text_only = soup.get_text(strip=True)
    return {f'{article.title}': text_only}
