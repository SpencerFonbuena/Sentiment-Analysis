from pathlib import Path
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator
from sqlalchemy import Boolean, Column, Integer, String, DateTime, LargeBinary,func
from datetime import datetime

class Settings(BaseSettings):
    
    DB_HOST: str = "viaduct.proxy.rlwy.net"  
    DB_USER: str = "root"       
    DB_PASS: str = "fhGsALhNYypVIoXxZJqaOpUruyeqPTyE"  
    MYSQL_PORT: int  = 47890    
    DB_NAME: str = "railway"       
    DB_URL: str = f'mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{MYSQL_PORT}/{DB_NAME}'
    
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

engine = create_engine(
    settings.DB_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=0
)
    

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

'''Production Tables'''
# Type verification of data inputs
class NewsArticles(Base):
    __tablename__ = "news_articles"
    id = Column(Integer, primary_key=True, unique=True)
    link = Column(String(300), unique=True)
    title = Column(String(255),  nullable=False)
    network = Column(String(50), default=False, nullable=False)
    article = Column(LargeBinary, nullable=False)
    title_sentiment = Column(String(50), nullable=False)
    article_positive = Column(String(50), nullable=False)
    article_negative = Column(String(50), nullable=False)
    article_neutral = Column(String(50), nullable=False)
    date_created = Column(DateTime, nullable=False, server_default=func.now())

'''
# # Define the SQLAlchemy model for the file_data table
class TwitterData(Base):
    __tablename__ = 'twitter_data'
    tweet_id = Column(String(50), primary_key=True)
    tweet = Column(LargeBinary, nullable=False)
    sentiment = Column(String(50), default=None, nullable=True)
    user = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())


# # Define the SQLAlchemy model for the file_data table
class InterTwitterData(Base):
    __tablename__ = 'inter_twitter'
    tweet_id = Column(String(50), primary_key=True)
    tweet = Column(LargeBinary, nullable=False)
    sentiment = Column(String(50), default=None, nullable=True)
    user = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

class InterInitScrape(Base):
    __tablename__ = 'inter_init_scrape'
    id = Column(Integer, primary_key=True)
    link = Column(String(255), nullable=False)
    title = Column(String(255),  nullable=False)
    network = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

class InitScrape(Base):
    __tablename__ = 'init_scrape'
    id = Column(Integer, primary_key=True)
    link = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    network = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())'''

def create_tables():
    # this command will create the tables, if they don't exist already
    Base.metadata.create_all(engine)
create_tables()
