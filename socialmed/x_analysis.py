import pandas as pd
from config.database import get_settings
import re
import ast
from datetime import datetime, timezone
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from models.models import x0_model,x1_model,x2_model,xi_model
import spacy

data = pd.read_csv('/root/test2.csv')

settings = get_settings()
engine = create_engine(settings.DB_URL)
spcy_parser = spacy.load('en_core_web_sm')

for ele in data.iterrows():
    result = []
    inter_done = []
    try:
        user1 = ele[1]['user']
        new_string = re.sub(r'datetime\.datetime\(\d+,\s\d+,\s\d+,\s\d+,\s\d+,\s\d+,\s.*\)', "'replaced'", user1)
        user2 = ast.literal_eval(new_string)
        
        # Element extraction
        x_id = ele[1]['id_str']
        username = str(user2['username'])
        content = ele[1]['rawContent']
        view_count = ele[1]['viewCount']
        like_count = ele[1]['likeCount']
        current_dates = datetime.now(tz=timezone.utc).date()
        

        # Sentiment Analysis
        # intermediate counter holders
        positive = 0
        negative = 0
        neutral = 0
        # Prepping Article
        doc = spcy_parser(content) # Separate long text into sentences
        sentences = [sent.text for sent in doc.sents] # Get just the text from those sentences
        
        group_x0 = [x0_model(sentence)[0]['label'].lower() for sentence in sentences]
        group_x1 = [x1_model(sentence)[0]['label'].lower() for sentence in sentences]
        group_x2 = [x2_model(sentence).lower() for sentence in sentences]
        group_xi = [xi_model(sentence).lower() for sentence in sentences]

        sentiment = group_x0 + group_x1 + group_x2

        article_sentiment = pd.Series(sentiment).value_counts().index[0][0]
        irony_sentiment = pd.Series(group_xi).value_counts().index[0][0]
        
        if irony_sentiment == 'irony':
            final_sentiment = f'{article_sentiment}_irony'
        else:
            final_sentiment = article_sentiment
        # Append
        inter_done.append(str(x_id))
        inter_done.append(username)
        inter_done.append(str(content).encode('utf-8'))
        if view_count > 0:
            inter_done.append(view_count)
        else:
            inter_done.append(like_count)
        inter_done.append(final_sentiment)
        inter_done.append(current_dates)
        result.append(inter_done)

        # Write to Database
        final = pd.DataFrame(result, columns=['tweet_id', 'username', 'raw_content', 'view_count', 'sentiment', 'created_at'])
        final.to_sql(name='tweets', con=engine, if_exists='append', index=False)
    except IntegrityError as e:
        print(e)
    except ValueError as e:
        print(e)




'''Session = sessionmaker(bind=engine)
session = Session()

sql_statement = 

#CREATE TABLE IF NOT EXISTS tweets (
#    tweet_id VARCHAR(255) PRIMARY KEY,
#    username VARCHAR(255),
#    raw_content TEXT,
#    view_count INT,
#    sentiment VARCHAR(255),
#    created_at DATE
#);


#sql_query = text("SELECT * FROM init_scrape WHERE date_created = :yesterday")
#result = session.execute(sql_query, {'yesterday': yesterday}).fetchall()
# Execute the merge operation
session.execute(text(sql_statement))
session.commit()'''