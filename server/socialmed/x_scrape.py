import asyncio
import pandas as pd
from twscrape import API, gather
from twscrape.logger import set_log_level
import pandas as pd
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel
import numpy as np
import time
from transformers import pipeline
import spacy
from config.database import get_settings
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import LONGTEXT, TINYTEXT, MEDIUMBLOB, DATETIME
from datetime import datetime, timezone, date, timedelta
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import re
import ast



# search (latest tab)
async def main():
    settings = get_settings()
    engine = create_engine(settings.DB_URL)
    #Session = sessionmaker(bind=engine)
    #session = Session()
    users = [
        # Geo-Political
        'realDonaldTrump', # Trump
        'POTUS', # USA pres
        'JoeBiden', # Joe Biden
        'KremlinRussia_E', # Putin / Russa
        'Bundeskanzler', # Germany
        'RishiSunak', # UK Conservative Leader
        'TheBlueHouseEng', # South Korea
        'EmmanuelMacron', # France
        'JPN_PMO', # Japan
        'spagov', # Saudi Arabia
        'MohamedBinZayed', # UAE
        'BarackObama', #Obama

        'DaveRamsey', #Dave Ramsay
        'WarrenBuffett', #Warren Buffett
        'elonmusk', #Elon Musk
        'RayDalio', #Ray Dalio

        'benshapiro', #Ben Shaprio
        'cenkuygur', #Cenk Uyger
        'donlemon', #Don Lemon
        'maddow', #Rachel Maddow
        'seanhannity', #Sean Hannity
        'TuckerCarlson',#Tucker Carlson
        'jaketapper',#Jake Tapper
        'RealCandaceO',#Candace Owens
        'JudgeJeanine',#Jeanine Pirro
    ]

    search_queries = [
        's and p 500',
        'nasdaq',
        'russell 5000',
        'dow jones', 
        'interest rates', 
        'jerome powell', 
        'jamie dimon', 
        'american economy', 
        'capital markets', 
        'politics', 

    ]
    
    db_url = '/root/Sentiment-Analysis/accounts.db'
    api = API(db_url)
    
    await api.pool.login_all()
    inter_data = pd.DataFrame()
    for user in users:
        single_user = await api.user_by_login(user)
        single_user_id = single_user.id
        user_tweets_and_replies = await gather(api.user_tweets_and_replies(single_user_id, limit=50))
        pd_test = pd.DataFrame(user_tweets_and_replies)
        inter_data = pd.concat((inter_data, pd_test))

    for ele in search_queries:
        test = await gather(api.search(ele, limit=50, kv={"product": "Top"}))
        pd_test = pd.DataFrame(test)
        inter_data = pd.concat((inter_data, pd_test))
    inter_data.to_csv('/root/test2.csv')

    
if __name__ == "__main__":
    asyncio.run(main())
