import pandas as pd
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

yahoo_sites = ['https://www.yahoo.com/news/world/',
               'https://www.yahoo.com/news/us/',
               'https://www.yahoo.com/news/politics/']

''' Process the front page'''
def yf_news(url):
    # ScraperAPI magic
    className = '[class="js-content-viewer rapidnofollow stream-title D(b) Td(n) Td(n):f C(--batcave) C($streamBrandHoverClass):h C($streamBrandHoverClass):fv wafer-destroyed"]'
    payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': url, 'render': 'true'}
    r = requests.get('https://api.scraperapi.com/', params=payload)
    html_response = r.text

    soup = BeautifulSoup(html_response, 'html.parser') # Parse response
    elements = soup.select(className) # Find specific element
    base_url = 'https://yahoo.com' # Create full Link
    data = []
    for ele in elements:
        link = base_url + ele['href']
        title = ele.get_text(strip=True)
        data.append({'link': link, 'title': title, 'network': 'YF_News'})
    
    final_data = pd.DataFrame(data)
    return final_data
