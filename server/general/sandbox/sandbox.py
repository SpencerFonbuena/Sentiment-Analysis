import pandas as pd

def news_api():
    data = pd.read_csv('/root/Sentiment-Analysis/test1.csv')
    title_sentiment = data['title_sentiment']
    article_positive = data['article_positive']
    article_negative = data['article_negative']
    article_neutral = data['article_neutral']
    group_title = title_sentiment.value_counts()
    print(group_title)
    print(sum(article_positive))
    print(sum(article_negative))
    print(sum(article_neutral))
