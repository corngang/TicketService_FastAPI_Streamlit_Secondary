import configparser
import os

config = configparser.ConfigParser()
config.read('/TicketService_FastAPI_Streamlit/cognito_split/fastapi/cognito.ini')
# ------------------------------------
# Read constants from environment file
# ------------------------------------
COGNITO_DOMAIN = os.getenv("RESERVE_URL", config['COGNITO']['COGNITO_DOMAIN'])
import requests

# COGNITO_USER_INFO_URL = f'{COGNITO_DOMAIN}/oauth2/userInfo'

userinf = "https://ap-southeast-2p93rziokn.auth.ap-southeast-2.amazoncognito.com/oauth2/userInfo"

access_token = 'eyJraWQiOiI5Ykt4RFNKemJMaVdwOVNuNEFIYk9oQ1I0dVYyY0xxT003ZFRPek5GdjdnPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIxOTJlMTQxOC00MDYxLTcwY2YtMzY3MS05NWQ2NWRlMzQzMDAiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuYXAtc291dGhlYXN0LTIuYW1hem9uYXdzLmNvbVwvYXAtc291dGhlYXN0LTJfUDkzUlppT2tuIiwidmVyc2lvbiI6MiwiY2xpZW50X2lkIjoiNW9tY3RqMjg2MWZ0bDU5N2E1ZmlzNmQ4bWkiLCJvcmlnaW5fanRpIjoiNTBlZmYwZjMtNjVhMi00NmM3LWE3YzctZGE2YTA3YmQwMmM4IiwidG9rZW5fdXNlIjoiYWNjZXNzIiwic2NvcGUiOiJvcGVuaWQgZW1haWwiLCJhdXRoX3RpbWUiOjE3NDIxNDc0MDYsImV4cCI6MTc0MjE1MTAwNiwiaWF0IjoxNzQyMTQ3NDA2LCJqdGkiOiI2MDE0ZmE4ZS02ZTdlLTRlMjktOTgxNy1mMmE0Mzk3ZGViNzUiLCJ1c2VybmFtZSI6IjE5MmUxNDE4LTQwNjEtNzBjZi0zNjcxLTk1ZDY1ZGUzNDMwMCJ9.Y9AqB7ofDz4kFKKPRiBDBaqIRPESqIvOfMU4layZfP1NxRoc-5lsOtPiWl4tsaMPaoB5pFXpWMUQUJFC1TRfnMEhMa5vrTuW7e77npBwZIuGHD8HowXr_h3Ge2LjpjW-9iJze5f3NgDcSAWxuHdWDHfPPBKPYLHYkS9jKHAXghra5M_L_rKWnz7R7SY8mUYzkFlnT_fLizrCNw9_ri5PXMGa_p9Xwiv87ayYxAlwS2WDf5XdZxQLyQqgc3Nw0NufGURigf3T3PF6cR3evRueRHXsPSnuxZVyRQUHj3JS7yhZ0KKk-SNxi_qYmqvQ1WuqxuPIe6WqM29rTkE_OM5Uiw'
headers = {
    "Authorization": f"Bearer {access_token}"
}

response = requests.get(userinf, headers=headers)

if response.status_code == 200:
    user_info = response.json()
    print(user_info)
else:
    print("사용자 정보 조회 실패:", response.status_code, response.text)

# userinfo_endpoint = "https://cognito-idp.ap-southeast-2.amazonaws.com/ap-southeast-2_P93RZiOkn/.well-known/openid-configuration"

# # Cognito의 UserInfo URL을 가져옵니다
# response = requests.get(userinfo_endpoint)
# config = response.json()
# print(config)