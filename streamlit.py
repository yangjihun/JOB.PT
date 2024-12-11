import streamlit as st

# ID와 비밀번호 설정
USER_CREDENTIALS = {"roy": "1012", "user1": "mypassword"}

# 인증 상태 확인
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# 인증 함수
def login(username, password):
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        st.session_state["authenticated"] = True
        st.success("로그인 성공!")
    else:
        st.error("로그인 실패. 아이디와 비밀번호를 확인하세요.")

# 로그인 화면
if not st.session_state["authenticated"]:
    st.title("로그인")
    username = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")
    if st.button("로그인"):
        login(username, password)
else:
    # 로그인 성공 시 보여줄 내용
    st.title("Streamlit 애플리케이션")
    st.write("여기에 애플리케이션 내용을 작성하세요.")
    if st.button("로그아웃"):
        st.session_state["authenticated"] = False