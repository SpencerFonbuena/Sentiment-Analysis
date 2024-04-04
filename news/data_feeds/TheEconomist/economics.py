import pandas as pd
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

ap_sites = ['https://www.economist.com/finance-and-economics',
            'https://www.economist.com/business']


class Article(BaseModel):
    url: str
    title: str

''' Process the front page'''
def economist_econ(article: Article):
    # ScraperAPI magic
    payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': article.url, 'render': 'true'}
    r = requests.get('https://api.scraperapi.com/', params=payload)
    html_response = r.text
    soup = BeautifulSoup(html_response, 'html.parser') # Parse response
    elements = soup.select('[class="css-a022oj e7j57mt0"]') # Find specific element
    base_url = 'https://www.economist.com' # Create full Link
    data = []
    for ele in elements:
        a_ref = ele.find('a')
        if a_ref['href'][:4] != 'http':
            link = base_url + a_ref['href']
        else:
            link = a_ref['href']
        title = ele.get_text(strip=True) if ele else 'does not contain'
        data.append({'link': link, 'title': title})
    
    final_data = pd.DataFrame(data)
    final_data.to_csv('economist_econ.csv', index=False)

'''Process the article and get it ready for sentiment classifier'''
def article_pull(article: Article):
    # Don't render articles. It will come up with many you don't want.
    payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': article.url}
    r = requests.get('https://api.scraperapi.com/', params=payload)
    html_response = r.text

    soup = BeautifulSoup(html_response, 'html.parser')
    text_only = soup.get_text(strip=True)
    return {f'{article.title}': text_only}
