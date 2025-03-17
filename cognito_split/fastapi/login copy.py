from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import requests
import base64
import os
import configparser
import uvicorn
from common.db_connect import select_query, insert_query
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)

config = configparser.ConfigParser()
config.read('/TicketService_FastAPI_Streamlit/cognito_split/fastapi/cognito.ini')
# ------------------------------------
# Read constants from environment file
# ------------------------------------
COGNITO_DOMAIN = os.getenv("RESERVE_URL", config['COGNITO']['COGNITO_DOMAIN'])
CLIENT_ID = os.getenv("CLIENT_ID", config['COGNITO']['CLIENT_ID'])
CLIENT_SECRET = os.getenv("CLIENT_SECRET", config['COGNITO']['CLIENT_SECRET'])
APP_URI = os.getenv("APP_URI", config['COGNITO']['APP_URI'])

# 환경 변수로 호스트와 포트를 설정
host = os.getenv("HOST", "0.0.0.0")
port = int(os.getenv("PORT", 8001))

app = FastAPI()

app.secret_key = os.urandom(24)  # Use a secure random key in production
oauth = OAuth(app)

oauth.register(
  name='oidc',
  authority='https://cognito-idp.ap-southeast-2.amazonaws.com/ap-southeast-2_P93RZiOkn',
  client_id='5omctj2861ftl597a5fis6d8mi',
  client_secret='<client secret>',
  server_metadata_url='https://cognito-idp.ap-southeast-2.amazonaws.com/ap-southeast-2_P93RZiOkn/.well-known/openid-configuration',
  client_kwargs={'scope': 'email openid phone profile'}
)

# python main.py에서 파일을 불러올 때 Uvicorn 서버를 기동
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)