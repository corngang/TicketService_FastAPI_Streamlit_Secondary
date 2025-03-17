from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import requests
import base64
import os
import configparser
import uvicorn
from common.db_connect import select_query, insert_query

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

# 로그인 URL 제공 (Streamlit에서 이 URL로 리디렉션)
@app.get("/login")
def login():
    login_url = (
        f"{COGNITO_DOMAIN}/login?client_id={CLIENT_ID}&response_type=code&scope=email+openid&redirect_uri={APP_URI}"
    )
    return RedirectResponse(login_url)

# 인증 후 액세스 토큰 요청 (POST 요청 처리)
class AuthRequest(BaseModel):
    code: str  # POST로 받을 인증 코드

@app.post("/login/auth")
def auth_callback(auth_request: AuthRequest):
    try:
        # 액세스 토큰을 받기 위한 요청
        token_url = f"{COGNITO_DOMAIN}/oauth2/token"
        client_secret_encoded = str(base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode("utf-8")), "utf-8")
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {client_secret_encoded}",
        }
        body = {
            "grant_type": "authorization_code",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": auth_request.code,
            "redirect_uri": APP_URI,
            "scope": "openid profile email phone"
        }

        # 액세스 토큰 요청
        response = requests.post(token_url, headers=headers, data=body)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to authenticate")
        
        tokens = response.json()
        print(tokens)

        query = """
            INSERT INTO token (code, access_token, id_token)
            VALUES (%s, %s, %s);
            """
        insert_query(query, (auth_request.code, tokens["access_token"], tokens["id_token"]))
        
        # 토큰을 성공적으로 받으면 토큰 반환
        return {"access_token": tokens["access_token"], "id_token": tokens["id_token"]}

    except:
        query = "SELECT access_token, id_token FROM token WHERE code = %s"
        token_data = select_query(query, (auth_request.code,))
        if token_data != []:
            return {"access_token": token_data[0][0], "id_token": token_data[0][1]}


# 로그아웃 URL 제공
@app.get("/logout")
def logout():
    logout_url = f"{COGNITO_DOMAIN}/logout?client_id={CLIENT_ID}&logout_uri={APP_URI}"
    return RedirectResponse(logout_url)

# python main.py에서 파일을 불러올 때 Uvicorn 서버를 기동
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)