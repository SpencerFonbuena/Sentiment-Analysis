import pandas as pd
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

ap_sites = ['https://www.economist.com/topics/united-states',
            'https://www.economist.com/the-world-this-week']


''' Process the front page'''
def economist_news(url):
    # ScraperAPI magic
    payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': url, 'render': 'true'}
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
        data.append({'link': link, 'title': title, 'network': 'Economist_News'})
    
    final_data = pd.DataFrame(data)
    return final_data

