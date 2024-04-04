import pandas as pd
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

nbc_sites = ['https://www.nbcnews.com/business',
             'https://www.nbcnews.com/tech-media']


''' Process the front page'''
def nbc_econ(url):
    # ScraperAPI magic
    payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': url, 'render': 'true'}
    r = requests.get('https://api.scraperapi.com/', params=payload)
    html_response = r.text
    soup = BeautifulSoup(html_response, 'html.parser') # Parse response
    elements = soup.select('[class="styles_headline__ice3t"]') # Find specific element
    base_url = 'https://www.nbc.com' # Create full Link
    data = []
    for ele in elements:
        try:
            a_ref = ele.find('a')
            if a_ref['href'][:4] != 'http':
                link = base_url + a_ref['href']
            else:
                link = a_ref['href']
            title = a_ref.get_text(strip=True) if a_ref else 'does not contain'
            data.append({'link': link, 'title': title})
        except:
            continue

    elements = soup.select('[class="wide-tease-item__info-wrapper flex-grow-1-m"]') # Find specific element
    for ele in elements:
        try:
            a_ref = ele.find_all('a')
            child_1 = a_ref[1].find('h2')
            if a_ref[1]['href'][:4] != 'http':
                link = base_url + a_ref[1]['href']
            else:
                link = a_ref[1]['href']
            title = child_1.get_text(strip=True) if child_1 else 'does not contain'
            data.append({'link': link, 'title': title, 'network': 'NBC_Econ'})
        except:
            continue
    
    final_data = pd.DataFrame(data)
    return final_data
