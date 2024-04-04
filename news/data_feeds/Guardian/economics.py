import pandas as pd
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

guardian_sites = ['https://www.theguardian.com/us/business',
                  'https://www.theguardian.com/business/economics',
                  'https://www.theguardian.com/business/us-small-business']

''' Process the front page'''
def guardian_econ(url):
    # ScraperAPI magic
    payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': url, 'render': 'true'}
    r = requests.get('https://api.scraperapi.com/', params=payload)
    html_response = r.text

    soup = BeautifulSoup(html_response, 'html.parser') # Parse response
    elements = soup.select('[class="dcr-16c50tn"]') # Find specific element
    base_url = 'https://www.theguardian.com/' # Create full Link
    data = []
    for ele in elements:
        a_tag = ele.find('a')
        link = base_url + a_tag['href']
        title = a_tag['aria-label']
        data.append({'link': link, 'title': title})

    # This pull is for the economics page. It own't work otherwise
    elements = soup.select('[class="u-faux-block-link__overlay js-headline-text"]') # Find specific element
    for ele in elements:
        link = ele['href']
        title = ele.get_text(strip=True)
        data.append({'link': link, 'title': title, 'network': 'Guardian_Econ'})
    
    final_data = pd.DataFrame(data)
    return final_data
