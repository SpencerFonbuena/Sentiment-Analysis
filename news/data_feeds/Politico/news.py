import pandas as pd
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

bbc_sites = ['https://www.politico.com/']


''' Process the front page'''
def politico_news(url):
    # ScraperAPI magic
    payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': url, 'render': 'true'}
    r = requests.get('https://api.scraperapi.com/', params=payload)
    html_response = r.text
    soup = BeautifulSoup(html_response, 'html.parser') # Parse response
    elements = soup.select('[class="headline is-standard-typeface"]') # Find specific element
    base_url = 'https://www.politico.com' # Create full Link
    data = []
    for ele in elements:
        a_ref = ele.find('a')
        try:
            if a_ref['href'][:4] != 'http':
                link = base_url + a_ref['href']
            else:
                link = a_ref['href']
            title = a_ref.get_text(strip=True) if a_ref else 'does not contain'
            data.append({'link': link, 'title': title, 'network': 'Politico_News'})
        except:
            continue
    
    final_data = pd.DataFrame(data)
    return final_data

