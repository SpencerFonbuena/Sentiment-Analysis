from config.database import get_settings
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pandas as pd
from sqlalchemy.dialects.mysql import LONGTEXT, TINYTEXT, MEDIUMBLOB, DATETIME
import mysql.connector

from data_feeds.APNews.economics import ap_econ
from data_feeds.APNews.news import APNews
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


df = pd.DataFrame(data)

engine = create_engine(settings.DB_URL)

df.to_sql(name='inter_articles', con=engine, if_exists='append', index=False)


# Create a session to execute the deletion
Session = sessionmaker(bind=engine)
session = Session()

sql_statement = """
INSERT INTO news_articles (url, network, sentiment, headline, article)
SELECT inter.url, inter.network, inter.sentiment, inter.headline, inter.article
FROM inter_articles AS inter
LEFT JOIN news_articles AS test ON inter.url = test.url
WHERE test.url IS NULL;
"""

# Create a session to execute the query
Session = sessionmaker(bind=engine)
session = Session()

# Execute the merge operation
session.execute(text(sql_statement))
session.commit()

# Execute the deletion
session.execute(text('DELETE FROM inter_news'))
session.commit()

# Close the session
session.close()

