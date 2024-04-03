import pandas as pd
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

nyt_sites = ['https://www.nytimes.com/section/business',
             'https://www.nytimes.com/section/business/economy',
             'https://www.nytimes.com/section/business/energy-environment',
             'https://www.nytimes.com/section/business/media',
             'https://www.nytimes.com/section/technology',
             'https://www.nytimes.com/section/business/small-business',
             'https://www.nytimes.com/section/technology/personaltech']


class Article(BaseModel):
    url: str
    title: str
class NYTEconomy():
    def __init__(self, url) -> None:
        self.url = url
    
    ''' Process the front page'''
    def main_pull(self):
        # ScraperAPI magic
        payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': self.url, 'render': 'true'}
        r = requests.get('https://api.scraperapi.com/', params=payload)
        html_response = r.text
        soup = BeautifulSoup(html_response, 'html.parser') # Parse response
        elements = soup.select('[class="css-1u3p7j1"]') # Find specific element
        base_url = 'https://www.nytimes.com' # Create full Link
        data = []
        for ele in elements:
            try:
                if ele['href'][:4] != 'http':
                    link = base_url + ele['href']
                else:
                    link = ele['href']
                title = ele.get_text(strip=True) if ele else 'does not contain'
                data.append({'link': link, 'title': title})
            except:
                continue

        elements = soup.select('[class="css-8hzhxf"]') # Find specific element
        for ele in elements:
            child_1 = ele.find('h3')
            try:
                if ele['href'][:4] != 'http':
                    link = base_url + ele['href']
                else:
                    link = ele['href']
                title = child_1.get_text(strip=True) if child_1 else 'does not contain'
                data.append({'link': link, 'title': title})
            except:
                continue
        
        final_data = pd.DataFrame(data)
        final_data.to_csv('nyt_bus.csv', index=False)

    '''Process the article and get it ready for sentiment classifier'''
    def article_pull(article: Article):
        # Don't render articles. It will come up with many you don't want.
        payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': article.url}
        r = requests.get('https://api.scraperapi.com/', params=payload)
        html_response = r.text

        soup = BeautifulSoup(html_response, 'html.parser')
        text_only = soup.get_text(strip=True)
        return {f'{article.title}': text_only}

reader = NYTEconomy(nyt_sites[1])
reader.main_pull()

