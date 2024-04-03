import pandas as pd
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

breitbart_sites = ['https://www.breitbart.com/politics/']
# 


class Article(BaseModel):
    url: str
    title: str

class BreitbartNews():
    def __init__(self, url) -> None:
        self.url = url
    
    ''' Process the front page'''
    def main_pull(self):
        # ScraperAPI magic
        payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': self.url, 'render': 'true'}
        r = requests.get('https://api.scraperapi.com/', params=payload)
        html_response = r.text
        soup = BeautifulSoup(html_response, 'html.parser') # Parse response
        elements = soup.select('.tC') # Find specific element
        data = []
        for ele in elements:
            h2_tag = ele.find('h2')
            a_tag = h2_tag.find('a')
            link = a_tag['href']
            title = a_tag.get_text(strip=True)
            data.append({'link': link, 'title': title})
        
        final_data = pd.DataFrame(data)
        final_data.to_csv('test3.csv', index=False)

    '''Process the article and get it ready for sentiment classifier'''
    def article_pull(article: Article):
        # Don't render articles. It will come up with many you don't want.
        payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': article.url}
        r = requests.get('https://api.scraperapi.com/', params=payload)
        html_response = r.text

        soup = BeautifulSoup(html_response, 'html.parser')
        text_only = soup.get_text(strip=True)
        return {f'{article.title}': text_only}

reader = BreitbartNews(breitbart_sites)
reader.main_pull()
