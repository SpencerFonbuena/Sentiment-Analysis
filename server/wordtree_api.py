import pandas as pd
from pydantic import BaseModel
from news.config.database import get_settings
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import LONGTEXT, TINYTEXT, MEDIUMBLOB, DATETIME
from datetime import datetime, timezone, date, timedelta

settings = get_settings()
engine = create_engine(settings.DB_URL)

# Create a session to execute the query
Session = sessionmaker(bind=engine)
session = Session()

today = date.today()  # Gets today's date
yesterday = today - timedelta(days=1)

def news_api():
    sql_query = text("SELECT * FROM news_articles WHERE date_created <= :today")

    # Execute the query and fetch results
    query_result = session.execute(sql_query, {'today': today}).fetchall()
    session.close()
    data = pd.DataFrame(query_result)
    # Extract information
    article = data['article']

def twitter_api():
    sql_query = text("SELECT * FROM tweets WHERE date_created <= :today")
    # Execute the query and fetch results
    query_result = session.execute(sql_query, {'today': today}).fetchall()
    session.close()
    data = pd.DataFrame(query_result)
    # Extract information
    tweet = data['raw_content']

print(twitter_api())