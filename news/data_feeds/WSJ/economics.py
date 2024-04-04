import pandas as pd
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

wsj_sites = ['https://www.wsj.com/business?mod=nav_top_section',
            'https://www.wsj.com/business/autos?mod=nav_top_subsection',
            'https://www.wsj.com/business/airlines?mod=nav_top_subsection',
            'https://www.wsj.com/business/autos?mod=nav_top_subsection',
            'https://www.wsj.com/business/c-suite?mod=nav_top_subsection',
            'https://www.wsj.com/business/energy-oil?mod=nav_top_subsection',
            'https://www.wsj.com/business/telecom?mod=nav_top_subsection',
            'https://www.wsj.com/business/retail?mod=nav_top_subsection',
            'https://www.wsj.com/business/hospitality?mod=nav_top_subsection',
            'https://www.wsj.com/business/logistics?mod=nav_top_subsection',
            'https://www.wsj.com/business/media?mod=nav_top_subsection',
            'https://www.wsj.com/economy/central-banking?mod=nav_top_subsection',
            'https://www.wsj.com/economy/consumers?mod=nav_top_subsection',
            'https://www.wsj.com/economy/housing?mod=nav_top_subsection',
            'https://www.wsj.com/economy/jobs?mod=nav_top_subsection',
            'https://www.wsj.com/economy/trade?mod=nav_top_subsection',
            'https://www.wsj.com/economy/global',
            'https://www.wsj.com/finance/banking?mod=nav_top_subsection',
            'https://www.wsj.com/finance/commodities-futures?mod=nav_top_subsection',
            'https://www.wsj.com/finance/currencies?mod=nav_top_subsection',
            'https://www.wsj.com/finance/investing?mod=nav_top_subsection',
            'https://www.wsj.com/finance/regulation?mod=nav_top_subsection',
            'https://www.wsj.com/finance/stocks?mod=nav_top_subsection']


''' Process the front page'''
def wsj_econ(url):
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
        data.append({'link': link, 'title': title, 'network': 'WSJ_Econ'})
    
    final_data = pd.DataFrame(data)
    return final_data
