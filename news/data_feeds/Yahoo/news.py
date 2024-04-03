import pandas as pd
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

yahoo_sites = ['https://www.yahoo.com/news/world/',
               'https://www.yahoo.com/news/us/',
               'https://www.yahoo.com/news/politics/']

class Article(BaseModel):
    url: str
    title: str

class YFNews():
    def __init__(self, url) -> None:
        self.url = url
        self.className = '[class="js-content-viewer rapidnofollow stream-title D(b) Td(n) Td(n):f C(--batcave) C($streamBrandHoverClass):h C($streamBrandHoverClass):fv wafer-destroyed"]'

    ''' Process the front page'''
    def main_pull(self):
        # ScraperAPI magic
        payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': self.url, 'render': 'true'}
        r = requests.get('https://api.scraperapi.com/', params=payload)
        html_response = r.text

        soup = BeautifulSoup(html_response, 'html.parser') # Parse response
        elements = soup.select(self.className) # Find specific element
        base_url = 'https://yahoo.com' # Create full Link
        data = []
        for ele in elements:
            link = base_url + ele['href']
            title = ele.get_text(strip=True)
            data.append({'link': link, 'title': title})
        
        final_data = pd.DataFrame(data)
        final_data.to_csv('test2.csv', index=False)

    '''Process the article and get it ready for sentiment classifier'''
    def article_pull(article: Article):
        # Don't render articles. It will come up with many you don't want.
        payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': article.url}
        r = requests.get('https://api.scraperapi.com/', params=payload)
        html_response = r.text

        soup = BeautifulSoup(html_response, 'html.parser')
        text_only = soup.get_text(strip=True)
        return {f'{article.title}': text_only}

