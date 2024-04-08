from config.database import get_settings
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pandas as pd
from sqlalchemy.dialects.mysql import LONGTEXT, TINYTEXT, MEDIUMBLOB, DATETIME
import mysql.connector
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel
from datetime import datetime, timezone

from data_feeds.ABCNews.economics import abc_econ
from data_feeds.ABCNews.news import abc_news

from data_feeds.APNews.economics import ap_econ
from data_feeds.APNews.news import ap_news

from data_feeds.BBC.economics import bbc_econ

from data_feeds.BInsider.economics import binsider_econ
from data_feeds.BInsider.news import binsider_news

from data_feeds.Breitbart.economy import breitbart_econ
from data_feeds.Breitbart.news import breitbart_news

from data_feeds.CBS.economics import cbs_econ
from data_feeds.CBS.news import cbs_news

from data_feeds.CNN.economics import cnn_econ
from data_feeds.CNN.news import cnn_news

from data_feeds.DailyMail.economics import dm_econ
from data_feeds.DailyMail.news import dm_news

from data_feeds.DailyWire.news import dw_news

from data_feeds.Fox.news import fox_news

from data_feeds.Guardian.economics import guardian_econ
from data_feeds.Guardian.news import guardian_news

from data_feeds.MarketWatch.economics import mw_econ

from data_feeds.NBC.economics import nbc_econ
from data_feeds.NBC.news import nbc_news

from data_feeds.NYTimes.economics import nyt_econ
from data_feeds.NYTimes.news import nyt_news

from data_feeds.Politico.news import politico_news

from data_feeds.TheEconomist.economics import economist_econ
from data_feeds.TheEconomist.news import economist_news

from data_feeds.TYT.news import tyt_news

from data_feeds.UsaToday.economics import usat_econ
from data_feeds.UsaToday.news import usat_news

from data_feeds.WSJ.economics import wsj_econ
from data_feeds.WSJ.news import wsj_news

from data_feeds.Yahoo.finance import yf_econ
from data_feeds.Yahoo.news import yf_news



settings = get_settings()

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


'''Process the article and get it ready for sentiment classifier'''
def article_pull(url):
    # Don't render articles. It will come up with many you don't want.
    payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': url}
    r = requests.get('https://api.scraperapi.com/', params=payload)
    html_response = r.text

    soup = BeautifulSoup(html_response, 'html.parser')
    text_only = soup.get_text(strip=True)
    return text_only



df = pd.DataFrame(columns=['link', 'title', 'network'])

# ABC Econ
for ele in SiteData.abcecon_sites:
    abcEcon = abc_econ(ele)
    df = pd.concat((df, abcEcon))

for ele in SiteData.abcnews_sites:
    abcnews = abc_news(ele)
    df = pd.concat((df, abcnews))

# AP News
for ele in SiteData.apecon_sites:
    apEcon = ap_econ(ele)
    df = pd.concat((df, apEcon))

for ele in SiteData.apnews_sites:
    apNews = ap_news(ele)
    df = pd.concat((df, apNews))

# BBC News
for ele in SiteData.bbcecon_sites:
    bbcEcon = bbc_econ(ele)
    df = pd.concat((df, bbcEcon))

#BInsider
for ele in SiteData.biecon_sites:
    biEcon = binsider_econ(ele)
    df = pd.concat((df, biEcon))

for ele in SiteData.binews_sites:
    biNews = binsider_news(ele)
    df = pd.concat((df, biNews))

#Breitbart
for ele in SiteData.breitbartecon_sites:
    breitbartEcon = breitbart_econ(ele)
    df = pd.concat((df, breitbartEcon))

for ele in SiteData.breitbartnews_sites:
    breitbartNews = breitbart_news(ele)
    df = pd.concat((df, breitbartNews))

# CBS
for ele in SiteData.cbsecon_sites:
    cbsEcon = cbs_econ(ele)
    df = pd.concat((df, cbsEcon))

for ele in SiteData.cbsnews_sites:
    cbsNews = cbs_news(ele)
    df = pd.concat((df, cbsNews))

# CNN
for ele in SiteData.cnnecon_sites:
    cnnEcon = cnn_econ(ele)
    df = pd.concat((df, cnnEcon))

for ele in SiteData.cnnnews_sites:
    cnnNews = cnn_news(ele)
    df = pd.concat((df, cnnNews))

# Daily Mail
for ele in SiteData.dmecon_sites:
    dmEcon = dm_econ(ele)
    df = pd.concat((df, dmEcon))

for ele in SiteData.dmnews_sites:
    dmNews = dm_news(ele)
    df = pd.concat((df, dmNews))

# Daily Wire
for ele in SiteData.dwnews_sites:
    dwNews = dw_news(ele)
    df = pd.concat((df, dwNews))

# Fox
for ele in SiteData.foxnews_sites:
    foxNews = fox_news(ele)
    df = pd.concat((df, foxNews))

# Guardian
for ele in SiteData.guardianecon_sites:
    guardianEcon = guardian_econ(ele)
    df = pd.concat((df, guardianEcon))

for ele in SiteData.guardiannews_sites:
    guardianNews = guardian_news(ele)
    df = pd.concat((df, guardianNews))

# Market Watch
for ele in SiteData.mwecon_sites:
    mwEcon = mw_econ(ele)
    df = pd.concat((df, mwEcon))

# NBC
for ele in SiteData.nbcecon_sites:
    nbcEcon = nbc_econ(ele)
    df = pd.concat((df, nbcEcon))

for ele in SiteData.nbcnews_sites:
    nbcNews = nbc_news(ele)
    df = pd.concat((df, nbcNews))

# NY Times
for ele in SiteData.nytecon_sites:
    nytEcon = nyt_econ(ele)
    df = pd.concat((df, nytEcon))

for ele in SiteData.nytnews_sites:
    nytNews = nyt_news(ele)
    df = pd.concat((df, nytNews))

# Politico
for ele in SiteData.politiconews_sites:
    politicoNews = politico_news(ele)
    df = pd.concat((df, politicoNews))

# The Economist
for ele in SiteData.economistecon_sites:
    economistEcon = economist_econ(ele)
    df = pd.concat((df, economistEcon))

for ele in SiteData.economistnews_sites:
    economistNews = economist_news(ele)
    df = pd.concat((df, economistNews))

# TYT
for ele in SiteData.tytnews_sites:
    tytNews = tyt_news(ele)
    df = pd.concat((df, tytNews))

# USA Today
for ele in SiteData.usatecon_sites:
    usatEcon = usat_econ(ele)
    df = pd.concat((df, usatEcon))

for ele in SiteData.usatnews_sites:
    usatNews = usat_news(ele)
    df = pd.concat((df, usatNews))

# WSJ
for ele in SiteData.wsjecon_sites:
    wsjEcon = wsj_econ(ele)
    df = pd.concat((df, wsjEcon))

for ele in SiteData.wsjnews_sites:
    wsjNews = wsj_news(ele)
    df = pd.concat((df, wsjNews))

# Yahoo
for ele in SiteData.yahooecon_sites:
    yahooEcon = yf_econ(ele)
    df = pd.concat((df, yahooEcon))

for ele in SiteData.yahoonews_sites:
    yahooNews = yf_news(ele)
    df = pd.concat((df, yahooNews))


engine = create_engine(settings.DB_URL)

df.to_sql(name='inter_init_scrape', con=engine, if_exists='append', index=False)


# Create a session to execute the deletion
Session = sessionmaker(bind=engine)
session = Session()

sql_statement = """
INSERT INTO init_scrape (link, title, network, date_created)
SELECT inter.link, inter.title, inter.network, CURDATE()
FROM inter_init_scrape AS inter
LEFT JOIN init_scrape AS test ON inter.link = test.link
WHERE test.link IS NULL;
"""

# Create a session to execute the query
Session = sessionmaker(bind=engine)
session = Session()

# Execute the merge operation
session.execute(text(sql_statement))
session.commit()

# Execute the deletion
session.execute(text('DELETE FROM inter_init_scrape'))
session.commit()

# Close the session
session.close()

