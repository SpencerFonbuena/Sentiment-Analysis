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


from models.models import x0_model, x1_model, x2_model

spcy_parser = spacy.load('en_core_web_sm')
settings = get_settings()
'''Process the article and get it ready for sentiment classifier'''
def article_pull(url):
    # Don't render articles. It will come up with many you don't want.
    payload = { 'api_key': 'f96027d9e4562ff1645ab574bf4759a0', 'url': url}
    r = requests.get('https://api.scraperapi.com/', params=payload)
    html_response = r.text

    soup = BeautifulSoup(html_response, 'html.parser')
    text_only = soup.get_text(strip=True)
    return text_only


'''Fetch the Data'''
engine = create_engine(settings.DB_URL)
Session = sessionmaker(bind=engine)
session = Session()

today = date.today()  # Gets today's date
yesterday = today - timedelta(days=1)
sql_query = text("SELECT * FROM init_scrape WHERE date_created = :today")

# Execute the query and fetch results
result = session.execute(sql_query, {'today': today}).fetchall()

# Close the session
session.close()

column_names = ['id', 'link', 'title', 'network', 'date_created']
df = pd.DataFrame(result, columns=column_names)



i = 0
start = time.perf_counter()
for _, ele in df.iterrows():
    try:
        print(i, len(df))
        i += 1
        inter_data = []
        inter_output = []
        # intermediate counter holders
        positive = 0
        negative = 0
        neutral = 0
        '''Prepping Article'''
        article_text = article_pull(ele['link']) # Collect Link
        doc = spcy_parser(article_text) # Separate long text into sentences
        sentences = [sent.text for sent in doc.sents] # Get just the text from those sentences

        '''Models'''
        title_sentiment_0 = x0_model(ele['title'])[0]['label'].lower()
        title_sentiment_1 = x1_model(ele['title'])[0]['label'].lower()
        title_sentiment_2 = x2_model(ele['title']).lower()
        
        group_title_sentiment = pd.Series([title_sentiment_0, title_sentiment_1]).value_counts().index[0]
        

        group_sentiments_0 = [x0_model(sentence)[0]['label'] for sentence in sentences]
        group_sentiments_1 = [x1_model(sentence)[0]['label'] for sentence in sentences]
        group_sentiments_2 = [x2_model(sentence) for sentence in sentences]
        
        article_sentiment_0 = pd.Series(group_sentiments_0).value_counts()
        article_sentiment_1 = pd.Series(group_sentiments_1).value_counts()
        article_sentiment_2 = pd.Series(group_sentiments_2).value_counts()

        for j in range(len(article_sentiment_0)):
            if article_sentiment_0.index[j].lower() == 'neutral':
                neutral += article_sentiment_0.iloc[j]
            if article_sentiment_0.index[j].lower() == 'positive':
                positive += article_sentiment_0.iloc[j]
            if article_sentiment_0.index[j].lower() == 'negative':
                negative += article_sentiment_0.iloc[j]
        
        for k in range(len(article_sentiment_1)):
            if article_sentiment_1.index[k].lower() == 'neutral':
                neutral += article_sentiment_1.iloc[k]
            if article_sentiment_1.index[k].lower() == 'positive':
                positive += article_sentiment_1.iloc[k]
            if article_sentiment_1.index[k].lower() == 'negative':
                negative += article_sentiment_1.iloc[k]

        for l in range(len(article_sentiment_2)):
            if article_sentiment_2.index[l].lower() == 'neutral':
                neutral += article_sentiment_2.iloc[l]
            if article_sentiment_2.index[l].lower() == 'positive':
                positive += article_sentiment_2.iloc[l]
            if article_sentiment_2.index[l].lower() == 'negative':
                negative += article_sentiment_2.iloc[l]
        
        '''The reason for divison, is that one of the models only predicts positive or negative. To simply add would be to triple count.
            Division is necessary for all of the counts to get back to realistic values'''
        try:
            inter_data.append(ele['link']) # link
            inter_data.append(str(ele['title']).encode('utf-8')) # title
            inter_data.append(ele['network']) # network
            inter_data.append(article_text.encode('utf-8')) # article
            inter_data.append(group_title_sentiment) # title_sentiment
            inter_data.append(positive / 3) # article_positive
            inter_data.append(negative / 3) # article_negative
            inter_data.append(neutral / 2) # article_neutral
            inter_data.append(date.today()) # date_created
            inter_output.append(inter_data) # output to general inter logger
            output = pd.DataFrame(inter_output, columns=['link', 'title', 'network', 'article', 'title_sentiment', 'article_positive', 'article_negative', 'article_neutral', 'date_created'])
            output.to_sql(name='news_articles', con=engine, if_exists='append', index=False)
            
        except IntegrityError as e:
            print("Duplicate entry:", e)
            continue
    except RuntimeError as e:
        print(e)
        continue
    