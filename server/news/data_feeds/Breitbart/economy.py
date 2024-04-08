import pandas as pd
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

breitbart_sites = ['https://www.breitbart.com/economy/']
# 


class Article(BaseModel):
    url: str
    title: str

class BreitbartEcon():
    def __init__(self, url) -> None:
        self.url = url
    
''' Process the front page'''
def breitbart_econ(url):
    # ScraperAPI magic
    payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': url, 'render': 'true'}
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
        data.append({'link': link, 'title': title, 'network': 'Breitbart_Econ'})
    
    final_data = pd.DataFrame(data)
    return final_data


