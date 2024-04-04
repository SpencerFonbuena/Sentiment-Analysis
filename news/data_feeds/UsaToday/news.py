import pandas as pd
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

bbc_sites = ['https://www.usatoday.com/news/nation/']


''' Process the front page'''
def usat_news(url):
    # ScraperAPI magic
    payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': url, 'render': 'true'}
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
        data.append({'link': link, 'title': title, 'network': 'USAT_News'})

    
    final_data = pd.DataFrame(data)
    return final_data