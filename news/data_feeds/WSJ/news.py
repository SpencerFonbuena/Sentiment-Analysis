import pandas as pd
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

ap_sites = ['https://www.wsj.com/politics?mod=nav_top_section',
            'https://www.wsj.com/world/americas?mod=nav_top_subsection',
            'https://www.wsj.com/world/china?mod=nav_top_subsection',
            'https://www.wsj.com/world/europe?mod=nav_top_subsection',
            'https://www.wsj.com/world/middle-east?mod=nav_top_subsection']


''' Process the front page'''
def wsj_news(url):
    # ScraperAPI magic
    payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': url, 'render': 'true'}
    r = requests.get('https://api.scraperapi.com/', params=payload)
    html_response = r.text
    soup = BeautifulSoup(html_response, 'html.parser') # Parse response
    elements = soup.select('[class="e1sf124z13 css-1me4f21-HeadlineLink"]') # Find specific element
    base_url = 'https://www.economist.com' # Create full Link
    data = []
    for ele in elements:
        child_1 = ele.find('span').find('p')
        if ele['href'][:4] != 'http':
            link = base_url + ele['href']
        else:
            link = ele['href']
        title = child_1.get_text(strip=True) if child_1 else 'does not contain'
        data.append({'link': link, 'title': title, 'network': 'WSJ_News'})
    
    final_data = pd.DataFrame(data)
    return final_data
