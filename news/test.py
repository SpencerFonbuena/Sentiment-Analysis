from config.database import get_settings
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pandas as pd
from sqlalchemy.dialects.mysql import LONGTEXT, TINYTEXT, MEDIUMBLOB, DATETIME
import mysql.connector

settings = get_settings()
data = {
    'url': [
        'http://example.com/article4',
        'http://example.com/article2',
        'http://example.com/article3'
    ],
    'network': ['CNN', 'BBC', 'FOX'],
    'sentiment': ['Positive', 'Neutral', 'Negative'],
    'headline': [
        'Market Rallies on Good News',
        'Election Results Awaited',
        'Sports Team Wins Championship'
    ],
    'article': [
        'First article text goes here',
        'Second article text, another one',
        'The third article text is this'
    ]
}

df = pd.DataFrame(data)
df['article'] = df['article'].apply(lambda x: x.encode('utf-8'))

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

