import streamlit as st
import requests

API_BASE_URL = "http://localhost:8001"

def login():
    response = requests.get(f"{API_BASE_URL}/login")
    st.markdown(f'<meta http-equiv="refresh" content="0;url={response.url}">', unsafe_allow_html=True)

def logout():
    response = requests.get(f"{API_BASE_URL}/logout")
    st.markdown(f'<meta http-equiv="refresh" content="0;url={response.url}">', unsafe_allow_html=True)

def check_auth(code):
    # POST 방식으로 인증 코드 전달
    response = requests.post(f"{API_BASE_URL}/login/auth", json={"code": code})
    if response.status_code == 200:
        tokens = response.json()
        st.session_state["authenticated"] = True
        st.session_state["access_token"] = tokens["access_token"]
        st.session_state["id_token"] = tokens["id_token"]
    else:
        st.error("로그인 실패")

# Streamlit UI
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

st.title("Cognito 인증 시스템")

auth_code = st.query_params.get("code", [None])
print(auth_code)
if auth_code:
    check_auth(auth_code)

if st.session_state["authenticated"]:
    st.write("✅ 로그인 성공!")
    if st.button("로그아웃"):
        logout()
else:
    if st.button("로그인"):
        login()
