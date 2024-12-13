
import streamlit as st
import json
from openai import OpenAI

# OpenAI 클라이언트 설정
client = OpenAI(api_key="YOUR_API_KEY")

# 제목 설정
st.title("사회 트렌드 기반 챗봇")
st.markdown("분야와 트렌드를 분석하여 직업 추천과 필요 역량을 제공합니다.")

# 파일 업로드
uploaded_data = st.file_uploader("트렌드 파일 업로드 (data.txt)", type=["txt"])
uploaded_news = st.file_uploader("뉴스 파일 업로드 (News.txt)", type=["txt"])

# 사용자 입력
q = st.text_input("분야를 입력하세요", value="")

# 로딩 애니메이션 (gif)
loading_gif_path = "loading.gif"
if st.button("분석 시작"):
    if uploaded_data and uploaded_news and q:
        with open(uploaded_data.name, "r", encoding="utf-8") as f:
            trend = f.read()
        with open(uploaded_news.name, "r", encoding="utf-8") as f:
            News = f.read()
        
        # 로딩 메시지
        with st.spinner("분석 중입니다... 잠시만 기다려 주세요."):
            # 결과 저장
            answers = []

            # 1단계 분석
            response1 = client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": "You are a helpful assistant designed to output JSON. Please write in Korean."},
                    {"role": "user", "content": f"사회 트렌드 분석 결과는 다음과 같습니다: {trend}. 이를 기반으로 '{q}'와 연관된 사회 트렌드를 분석하고, 중간 결과를 나타내시오."}
                ]
            )
            result1 = response1.choices[0].message.content

            # 2단계 분석
            for _ in range(3):  # Self-consistency
                response2 = client.chat.completions.create(
                    model="gpt-4o-mini",
                    response_format={"type": "json_object"},
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant designed to output JSON. Please write in Korean."},
                        {"role": "user", "content": f"이전 분석 결과는 다음과 같습니다: {result1}. 이를 기반으로 '{News}'의 내용을 참고하여 추천할 만한 관련 직업 3개를 명시하세요. 출력값은 다음과 같은 형식을 따르세요. {{'직업':[의사,회계사,작곡가]}}."}
                    ]
                )
                result2 = json.loads(response2.choices[0].message.content)
                answers.extend(result2["직업"])

            # 3단계 분석
            final_response = client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": "You are a helpful assistant designed to output JSON. Please write in Korean."},
                    {"role": "user", "content": f"{answers}의 내용에서 가장 많이 나온 직업 3개와 각 직업에 대한 필요 역량을 답변하세요. 출력값은 다음과 같은 형식을 따르세요. {{'직업':[의사,회계사,작곡가], '필요역량':[의사자격증,수학지식,음악감각]}}."}
                ]
            )

            result = final_response.choices[0].message.content

            # 결과 출력
            st.success("분석이 완료되었습니다!")
            st.json(json.loads(result))
    else:
        st.error("모든 입력 필드와 파일을 업로드해야 합니다.")
