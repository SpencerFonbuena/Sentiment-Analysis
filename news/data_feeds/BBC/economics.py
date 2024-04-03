import pandas as pd
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

bbc_sites = ['https://www.bbc.com/business']


class Article(BaseModel):
    url: str
    title: str
class BBCEcon():
    def __init__(self, url) -> None:
        self.url = url
    
    ''' Process the front page'''
    def main_pull(self):
        # ScraperAPI magic
        payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': self.url, 'render': 'true'}
        r = requests.get('https://api.scraperapi.com/', params=payload)
        html_response = r.text
        soup = BeautifulSoup(html_response, 'html.parser') # Parse response
        elements = soup.select('[data-testid="edinburgh-card"]') # Find specific element
        base_url = 'https://www.bbc.com' # Create full Link
        data = []
        for ele in elements:
            child_1 = ele.find('div').find('a')
            child_2 = child_1.find_all('h2')
            
            print(child_2)
            try:
                if child_1['href'][:4] != 'http':
                    link = base_url + child_1['href']
                else:
                    link = child_1['href']
                #title = child_3.get_text(strip=True) if child_3 else 'does not contain'
                print(link)
                #data.append({'link': link, 'title': title})
            except:
                continue
        
        final_data = pd.DataFrame(data)
        final_data.to_csv('bbc_bus.csv', index=False)

    '''Process the article and get it ready for sentiment classifier'''
    def article_pull(article: Article):
        # Don't render articles. It will come up with many you don't want.
        payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': article.url}
        r = requests.get('https://api.scraperapi.com/', params=payload)
        html_response = r.text

        soup = BeautifulSoup(html_response, 'html.parser')
        text_only = soup.get_text(strip=True)
        return {f'{article.title}': text_only}

reader = BBCEcon(bbc_sites)
reader.main_pull()

