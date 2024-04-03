import pandas as pd
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

from transformers import pipeline
import spacy

from data_feeds.APNews.economics import ap_econ
from models.models import x0_model, x1_model, x2_model

spcy_parser = spacy.load('en_core_web_sm')

class SiteData:
    abcecon_sites = ['https://abcnews.go.com/Business',
                'https://abcnews.go.com/Technology']

    abcnews_sites = ['https://abcnews.go.com/Politics',
                'https://abcnews.go.com/US']

    # APNews
    apecon_sites = ['https://apnews.com/business']

    apnews_sites = ['https://apnews.com/politics',
                'https://apnews.com/us-news']

    #BBCNews
    bbcecon_sites = ['https://www.bbc.com/business']

    #BInsider
    biecon_sites = ['https://www.businessinsider.com/strategy'
                'https://www.businessinsider.com/business',
                'https://www.businessinsider.com/tech',
                'https://www.businessinsider.com/tech'
                ]

    binews_sites = ['https://www.businessinsider.com/politics']

    # Breitbart
    breitbartecon_sites = ['https://www.breitbart.com/economy/']

    breitbartnews_sites = ['https://www.breitbart.com/politics/']

    # CBS
    cbsecon_sites = ['https://www.cbsnews.com/moneywatch/']

    cbsnews_sites = ['https://www.cbsnews.com/us/',
                'https://www.cbsnews.com/politics/']

    # CNN
    cnnecon_sites = ['https://www.cnn.com/business']

    cnnnews_sites = ['https://www.cnn.com/us',
                'https://www.cnn.com/politics',
                'https://www.cnn.com/world']

    #Daily Mail
    dmecon_sites = ['https://www.dailymail.co.uk/news/us-economy/index.html',
                'https://www.dailymail.co.uk/yourmoney/index.html']

    dmnews_sites = ['https://www.dailymail.co.uk/news/us-politics/index.html']

    # Daily Wire
    dwnews_sites = ['https://www.dailywire.com/topic/politics',
                'https://www.dailywire.com/topic/u-s']

    # Fox News
    foxnews_sites = ['https://www.foxnews.com/politics',
                'https://www.foxnews.com/world']

    # Guardian
    guardianecon_sites = ['https://www.theguardian.com/us/business',
                    'https://www.theguardian.com/business/economics',
                    'https://www.theguardian.com/business/us-small-business']

    guardiannews_sites = ['https://www.theguardian.com/world']

    # Market Watch
    mwecon_sites = ['https://www.marketwatch.com/economy-politics/federal-reserve?mod=economy-politics',
                'https://www.marketwatch.com/economy-politics?mod=top_nav',
                'https://www.marketwatch.com/investing?mod=top_nav',
                'https://www.marketwatch.com/',
                'https://www.marketwatch.com/investing/stocks?mod=investing',
                'https://www.marketwatch.com/investing/barrons?mod=stocks',
                'https://www.marketwatch.com/markets/earnings?mod=barrons-on-marketwatch',
                'https://www.marketwatch.com/markets/us?mod=earnings',
                'https://www.marketwatch.com/market-data/asia?mod=currencies-market-data',
                'https://www.marketwatch.com/market-data/rates?mod=asia-market-data'
                ]


    # NBC Sites
    nbcecon_sites = ['https://www.nbcnews.com/business',
                'https://www.nbcnews.com/tech-media']

    nbcnews_sites = ['https://www.msnbc.com/']

    # NY Times
    nytecon_sites = ['https://www.nytimes.com/section/business',
                'https://www.nytimes.com/section/business/economy',
                'https://www.nytimes.com/section/business/energy-environment',
                'https://www.nytimes.com/section/business/media',
                'https://www.nytimes.com/section/technology',
                'https://www.nytimes.com/section/business/small-business',
                'https://www.nytimes.com/section/technology/personaltech']

    nytnews_sites = ['https://www.nytimes.com/section/politics']


    # Politico
    politiconews_sites = ['https://www.politico.com/']

    #Economist
    economistecon_sites = ['https://www.economist.com/finance-and-economics',
                'https://www.economist.com/business']

    economistnews_sites = ['https://www.economist.com/topics/united-states',
                'https://www.economist.com/the-world-this-week']

    # TYT News
    tytnews_sites = ['https://tyt.com/reports']

    # USA Today
    usatecon_sites = ['https://www.usatoday.com/money/',
                'https://www.usatoday.com/tech/']

    usatnews_sites = ['https://www.usatoday.com/news/nation/']


    # WSJ
    wsjecon_sites = ['https://www.wsj.com/business?mod=nav_top_section',
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

    wsjnews_sites = ['https://www.wsj.com/politics?mod=nav_top_section',
                'https://www.wsj.com/world/americas?mod=nav_top_subsection',
                'https://www.wsj.com/world/china?mod=nav_top_subsection',
                'https://www.wsj.com/world/europe?mod=nav_top_subsection',
                'https://www.wsj.com/world/middle-east?mod=nav_top_subsection']

    # Yahoo 
    yahooecon_sites = ['https://finance.yahoo.com/bidenomics/',
                'https://finance.yahoo.com/topic/stock-market-news/',
                'https://finance.yahoo.com/topic/economic-news/',
                'https://finance.yahoo.com/topic/earnings/',
                'https://finance.yahoo.com/topic/crypto/',
                'https://finance.yahoo.com/live/politics/',
                'https://finance.yahoo.com/bidenomics/']

    yahoonews_sites = ['https://www.yahoo.com/news/world/',
                'https://www.yahoo.com/news/us/',
                'https://www.yahoo.com/news/politics/']


class Article(BaseModel):
    url: str
    title: str

'''Process the article and get it ready for sentiment classifier'''
def article_pull(url):
    # Don't render articles. It will come up with many you don't want.
    payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': url}
    r = requests.get('https://api.scraperapi.com/', params=payload)
    html_response = r.text

    soup = BeautifulSoup(html_response, 'html.parser')
    text_only = soup.get_text(strip=True)
    return text_only


ap_base = Article(url=SiteData.apecon_sites[0], title='Test1')
ap = ap_econ(ap_base)

for _, ele in ap.iterrows():
    # intermediate counter holders
    positive = 0
    negative = 0
    neutral = 0

    '''Prepping Article'''
    article_text = article_pull(ele['link']) # Collect Link
    ap['article'] = article_text.encode('utf-8') # Store article text in database for backtesting
    doc = spcy_parser(article_text) # Separate long text into sentences
    sentences = [sent.text for sent in doc.sents] # Get just the text from those sentences


    '''Models'''
    title_sentiment_0 = x0_model(ele['title'])[0]['label'].lower()
    title_sentiment_1 = x1_model(ele['title'])[0]['label'].lower()
    title_sentiment_2 = x2_model(ele['title']).lower()

    group_title_sentiment = pd.Series([title_sentiment_0, title_sentiment_1, title_sentiment_2]).value_counts()
    ap['title_sentiment'] = group_title_sentiment.iloc[0]

    group_sentiments_0 = [x0_model(sentence)[0]['label'] for sentence in sentences]
    group_sentiments_1 = [x1_model(sentence)[0]['label'] for sentence in sentences]
    group_sentiments_2 = [x2_model(sentence) for sentence in sentences]
    
    article_sentiment_0 = pd.Series(group_sentiments_0).value_counts()
    article_sentiment_1 = pd.Series(group_sentiments_1).value_counts()
    article_sentiment_2 = pd.Series(group_sentiments_2).value_counts()

    for i in range(len(article_sentiment_0)):
        if article_sentiment_0.index[i].lower() == 'neutral':
            neutral += article_sentiment_0.iloc[i]
        if article_sentiment_0.index[i].lower() == 'positive':
            positive += article_sentiment_0.iloc[i]
        if article_sentiment_0.index[i].lower() == 'negative':
            negative += article_sentiment_0.iloc[i]
    
    for i in range(len(article_sentiment_1)):
        if article_sentiment_1.index[i].lower() == 'neutral':
            neutral += article_sentiment_1.iloc[i]
        if article_sentiment_1.index[i].lower() == 'positive':
            positive += article_sentiment_1.iloc[i]
        if article_sentiment_1.index[i].lower() == 'negative':
            negative += article_sentiment_1.iloc[i]

    for i in range(len(article_sentiment_2)):
        if article_sentiment_2.index[i].lower() == 'neutral':
            neutral += article_sentiment_2.iloc[i]
        if article_sentiment_2.index[i].lower() == 'positive':
            positive += article_sentiment_2.iloc[i]
        if article_sentiment_2.index[i].lower() == 'negative':
            negative += article_sentiment_2.iloc[i]
    
    '''The reason for divison, is that one of the models only predicts positive or negative. To simply add would be to triple count.
        Division is necessary for all of the counts to get back to realistic values'''
    ap['article_positive'] = positive / 3
    ap['article_negative'] = negative / 3
    ap['article_neutral'] = neutral / 2

    
    '''if title_sentiment == article_sentiment_0:
        ap['sentiment'] = article_sentiment_0
    else:
        ap['sentiment'] = title_sentiment'''
ap.to_csv('article_run.csv', index=False)







