import pandas as pd
from pydantic import BaseModel
from news.config.database import get_settings
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import LONGTEXT, TINYTEXT, MEDIUMBLOB, DATETIME
from datetime import datetime, timezone, date, timedelta
import json

settings = get_settings()
engine = create_engine(settings.DB_URL)

# Create a session to execute the query
Session = sessionmaker(bind=engine)
session = Session()

today = date.today()  # Gets today's date
one_ago = today - timedelta(days=1)
two_ago = today - timedelta(days=2)
three_ago = today - timedelta(days=3)
four_ago = today - timedelta(days=4)
five_ago = today - timedelta(days=5)
six_ago = today - timedelta(days=6)
seven_ago = today - timedelta(days=7)

def news_api():
    sql_query = text("SELECT * FROM news_articles WHERE date_created <= :today")
    # Execute the query and fetch results
    query_result = session.execute(sql_query, {'today': today}).fetchall()
    session.close()
    data = pd.DataFrame(query_result)
    # Extract information
    title_sentiment = data['title_sentiment']
    article_positive = sum(data['article_positive'].apply(lambda x: float(str(x))))
    article_negative = sum(data['article_negative'].apply(lambda x: float(str(x))))
    article_neutral = sum(data['article_neutral'].apply(lambda x: float(str(x))))
    group_title = title_sentiment.value_counts()
    positive_articles = 0
    negative_articles = 0

    # Series are not serializable, so this isolates the value count
    if group_title.index[0] == 'positive':
        positive_articles += group_title[0]
    elif group_title.index[0] == 'negative':
        negative_articles += group_title[0]

    if group_title.index[1] == 'negative':
        negative_articles += group_title[1]
    elif group_title.index[1] == 'positive':
        positive_articles += group_title[1]
    result =  json.dumps({'positive_articles': int(positive_articles), 'negative_articles': int(negative_articles) ,'positive_sentences': article_positive, 'neutral_sentences': article_neutral, 'negative_sentences': article_negative})
    return result


def twitter_api():
    sql_query = text("SELECT * FROM tweets WHERE date_created <= :today")
    # Execute the query and fetch results
    query_result = session.execute(sql_query, {'today': today}).fetchall()
    session.close()
    data = pd.DataFrame(query_result)
    
    # Temporary Data Stores
    positive = 0
    neutral = 0
    negative = 0
    positive_irony = 0
    neutral_irony = 0
    negative_irony = 0
    
    # Extract information
    for _, ele in data.iterrows():
        if ele['sentiment'] == 'positive':
            positive += ele['view_count']
        elif ele['sentiment'] == 'neutral':
            neutral += ele['view_count']
        elif ele['sentiment'] == 'negative':
            negative += ele['view_count']
        elif ele['sentiment'] == 'positive_irony':
            positive_irony += ele['view_count']
        elif ele['sentiment'] == 'neutral_irony':
            neutral_irony += ele['view_count']
        elif ele['sentiment'] == 'negative_irony':
            negative_irony += ele['view_count']
    
    result =  json.dumps({
            'positive': positive,  
            'neutral': neutral, 
            'negative': negative, 
            'positive_irony': positive_irony,
            'neutral_irony': neutral_irony,
            'negative_irony': negative_irony})
    return result
#news_sent = news_api()
#tweets_sent = twitter_api()
#print(news_sent)
#print(tweets_sent)