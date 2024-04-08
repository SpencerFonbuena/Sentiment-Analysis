from fastapi import APIRouter, status, Depends, Header, Request
from sqlalchemy.orm import Session
from news.config.database import get_db
from fastapi.responses import JSONResponse
import json
from sentiment_api import news_api, twitter_api

# Auth Router and routes
general_router = APIRouter(
    prefix="/ga",
    tags=["General "],
    responses={404: {"description": "Not found"}},
)

# Attached to the login button. The token needs to sent from session memory still
@general_router.get("/data_pull", status_code=status.HTTP_200_OK)
async def data_pull():
    news = news_api()
    tweets = twitter_api()
    payload = {'news': news, 'tweets': tweets}
    return JSONResponse(payload, status_code=status.HTTP_200_OK)