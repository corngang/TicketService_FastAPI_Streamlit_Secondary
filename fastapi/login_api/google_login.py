from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
import uvicorn

# )


# OAuth 등록 (Google OAuth)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# FastAPI 애플리케이션
app = FastAPI()

# 세션 미들웨어 추가
app.add_middleware(SessionMiddleware, secret_key="secret-string")

# 로그인 엔드포인트
@app.get('/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')  # 인증 후 리디렉션될 URL
    return await oauth.google.authorize_redirect(request, redirect_uri)

# 인증 후 콜백 처리
@app.get('/auth')
async def auth(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = token['userinfo']
    return JSONResponse(content=user)  # 사용자 정보 반환


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)

