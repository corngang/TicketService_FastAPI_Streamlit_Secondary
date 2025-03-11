import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from common.user_validation import UserRequest
from common.db_connect import select_query, insert_query

import uvicorn

# 환경 변수로 호스트와 포트를 설정
host = os.getenv("HOST", "0.0.0.0")
port = int(os.getenv("PORT", 8002))

app = FastAPI()

# 사용자 정의 예외 처리 함수
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

# 간단한 로그인 처리 예시
@app.post("/user")
def join_user(request: UserRequest):
    query = "SELECT * FROM account;"
    account_data = select_query(query)

    user_id_exists = False
    for row in account_data:
        # ID 존재 여부 확인
        if row[0] == request.username:
            user_id_exists = True
            break

    # 중복된 ID 확인
    if user_id_exists == True:
        raise HTTPException(status_code=409, detail="이미 존재하는 아이디입니다.")
    

    # 이름, 전화번호, 생년월일이 동일한 사용자가 있는지 확인
    for row in account_data:
        if row[1] == request.name and row[3] == request.phone_number and row[4] == request.birth:
            raise HTTPException(status_code=410, detail="이미 가입된 사용자입니다.")
        elif row[3] == request.phone_number:
            raise HTTPException(status_code=411, detail="이미 존재하는 전화번호입니다.")

# insert_data('account', ['username', 'name', 'password', 'phone', 'birthdate'],
#             ['testuser', '김김김', 'test@1234', '01011112222', '2000-01-01'])
       

    # 사용자 저장
    query = "INSERT INTO account (account_id, name, password, phone_number, birth) VALUES (%s, %s, %s, %s, %s)"
    parms = (request.username, request.name, request.password, request.phone_number, request.birth)
    insert_query(query, parms)
    
    return {
        "status_code": 0,
        "data": {
            "username": request.username,
        },
        "message": "signup_success"
    }
#python main.py에서 파일을 불러올 때 Uvicorn서버를 기동
if __name__ == "__main__":
    uvicorn.run(app, host=host, port=port)