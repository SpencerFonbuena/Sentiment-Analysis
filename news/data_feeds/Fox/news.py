import pandas as pd
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

fox_sites = ['https://www.foxnews.com/politics',
             'https://www.foxnews.com/world']


class Article(BaseModel):
    url: str
    title: str

class FoxNews():
    def __init__(self, url) -> None:
        self.url = url
    
    ''' Process the front page'''
    def main_pull(self):
        # ScraperAPI magic
        payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': self.url, 'render': 'true'}
        r = requests.get('https://api.scraperapi.com/', params=payload)
        html_response = r.text
        soup = BeautifulSoup(html_response, 'html.parser') # Parse response
        elements = soup.select('[class="title"]') # Find specific element
        base_url = 'https://foxnews.com' # Create full Link
        data = []
        for ele in elements:
            try:
                a_tag = ele.find('a')
                if a_tag['href'][:4] != 'http':
                    link = base_url + a_tag['href']
                else:
                    link = a_tag['href']
                title = a_tag.get_text(strip=True)
                data.append({'link': link, 'title': title})
            except TypeError:
                continue
        
        final_data = pd.DataFrame(data)
        final_data.to_csv('fox_politics.csv', index=False)

    '''Process the article and get it ready for sentiment classifier'''
    def article_pull(article: Article):
        # Don't render articles. It will come up with many you don't want.
        payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': article.url}
        r = requests.get('https://api.scraperapi.com/', params=payload)
        html_response = r.text

        soup = BeautifulSoup(html_response, 'html.parser')
        text_only = soup.get_text(strip=True)
        return {f'{article.title}': text_only}

reader = FoxNews(fox_sites)
reader.main_pull()
