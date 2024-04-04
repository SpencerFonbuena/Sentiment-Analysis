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


''' Process the front page'''
def nyt_econ(url):
    # ScraperAPI magic
    payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': url, 'render': 'true'}
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
            data.append({'link': link, 'title': title, 'network': 'NYT_Econ'})
        except:
            continue
    
    final_data = pd.DataFrame(data)
    return final_data

