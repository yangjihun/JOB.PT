import os
import re
import json
import random
import requests
import streamlit as st
from openai import OpenAI
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from kbs_crolling import search_kbs_news
from mbc_crolling import search_mbc_news
from sbs_crolling import search_sbs_news
from crolling import data_crawl
from job_crawl import crawl_jobkorea

# .env 파일 로드
load_dotenv()

# 환경 변수에서 API 키를 읽어옴
api_key = os.getenv("OPENAI_API_KEY")

# OpenAI 클라이언트 생성
client = OpenAI(api_key=api_key)

# Streamlit 인터페이스 구성
st.title("JOB.PT")
st.sidebar.header("직업 추천 및 필요 역량 분석")
q = st.sidebar.text_input("분야를 입력하세요", "")

if not q:
    st.warning("분야를 입력해주세요!")  # 입력 유도가 없을 경우 메시지 출력
else:
    # 파일 로드 | 이 부분을 기사와 연결지어서 조인하면 될 듯 !
    try:
        # data_crawl(q) # 논문 불러오기
        # kbs_news = search_kbs_news(q, max_results=15)  # KBS 뉴스 크롤링
        # mbc_news = search_mbc_news(q, max_news=15)  # MBC 뉴스 크롤링
        # sbs_news = search_sbs_news(q, total_news=15)  # SBS 뉴스 크롤링
        # # kbs, mbc, sbs 각 3개의 txt
        with open("data.txt", "r", encoding="utf-8") as file:
            trend = file.read()
        with open("news.txt", "r", encoding="utf-8") as file:
            news = file.read()


    except FileNotFoundError:
        st.error("데이터 파일을 찾을 수 없습니다. 'data.txt'와 'news.txt'가 필요합니다.")
        st.stop()

    # 결과 저장용 리스트
    answers = []

    # 랜덤으로 GIF URL 생성
    random_number = random.randint(1, 30)  # 1부터 30까지의 랜덤 숫자   
    gif_url = f"https://giphy.com/search/cat"
    
    # GIF 페이지에서 HTML을 가져오기
    response = requests.get(gif_url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 원하는 a[x] 태그에서 랜덤 x 값을 넣어 img 태그 추출
    img_tag = soup.select(f"div div div a:nth-of-type({random_number}) picture img")
    
    # 이미지가 있는 경우 처리
    if img_tag:
        gif_image_url = img_tag[0]['src']
    else:
        gif_image_url = "https://media.giphy.com/media/3o7aD6YcSHFlh0hnre/giphy.gif"  # 기본 이미지 URL

    # 진행률 표시용 바
    progress_bar = st.progress(0)  # 초기 진행률을 0으로 설정

    # 실행 중 상태 표시
    text_placeholder = st.empty()  # 텍스트를 동적으로 제어하기 위한 placeholder
    loading_placeholder = st.empty()
    text_placeholder.write("**Self-Consistency 실행 중... 기다려주세요!**")
    loading_placeholder.markdown(
        f'<img src="{gif_image_url}" alt="loading gif">',
        unsafe_allow_html=True,
    )

    # Self-Consistency 수행
    for i in range(3):
        # 첫 번째 요청 / 기사 기반
        response1 = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON. Please write in Korean."},
                {"role": "user", "content": f"사회 트렌드 분석 결과는 다음과 같습니다: {news}. 이를 기반으로 '{q}'와 연관된 사회 트렌드를 분석하고, 중간 결과를 나타내시오."}
            ]
        )
        result1 = response1.choices[0].message.content

        # print("11111", result1)      # 학습 출력물

        # 두 번째 요청 / 논문 기반
        response2 = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON. Please write in Korean."},
                {"role": "user", "content": f"이전 분석 결과는 다음과 같습니다: {result1}. 이를 기반으로 '{trend}'의 내용을 참고하여 추천할 만한 관련 직업 3개를 명시하세요. 출력값은 다음과 같은 형식을 따르세요. {{'직업':[의사,회계사,작곡가]}}."}
            ]
        )
        result2 = response2.choices[0].message.content
        result2 = json.loads(result2)
        answers.append(result2["직업"])

        # print("22222",result2)      # 두번째 학습 출력물

        # 진행률 업데이트
        progress_bar.progress(int((i + 1) * 33)+1)  # 3단계로 진행을 나누어 퍼센트 업데이트 (33, 66, 100)

    # 최종 요청
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON. Please write in Korean."},
            {"role": "user", "content": f"{answers}의 내용에서 가장 많이 나온 직업 3개와 각 직업에 대한 필요 역량을 답변하세요. 출력값은 다음과 같은 형식을 따르세요. {{'직업':[의사,회계사,작곡가], '필요역량':[의사자격증,수학지식,음악감각]}}. 직업[0]에 대한 필요역량은 필요역량[0]에 해당하는 방식이다."}
        ]   
    )

    # 결과 출력
    result = json.loads(response.choices[0].message.content)

    # print("33333",result)       # 세번째 출력물

    # 로딩 상태 제거
    loading_placeholder.empty()  # GIF 제거
    text_placeholder.empty()  # 텍스트 제거
    progress_bar.empty()  # 진행률 바 제거
    st.write("**Self-Consistency 실행 완료!** ✅")

    # 결과를 시각적으로 예쁘게 출력
    st.subheader("🔍 분석 결과")
    st.write("### 추천 직업")
    for job, skill in zip(result["직업"], result["필요역량"]):
        st.markdown(f"- **직업**: {job}  <br>  **필요 역량**: {skill}", unsafe_allow_html=True)
        job_list = crawl_jobkorea(job)
        # print(job_list)
    # # 선택적으로 JSON 전체 출력
    # st.write("### Raw JSON 결과 (Optional)")
    # st.json(result)

    st.subheader("🔗 추천 직업 및 필요 역량 분석")

    for job, skill in zip(result["직업"], result["필요역량"]):
        st.markdown(f"#### **직업**: {job}")
        st.markdown(f"- **필요 역량**: {skill}")
        
        # JobKorea 크롤링 데이터 표시
        st.write("**관련 공고:**")
        job_list = crawl_jobkorea(job)
        if job_list:
            for idx, job_info in enumerate(job_list, 1):
                st.write(f"{idx}. [{job_info['title']}](<{job_info['link']}>)")
        else:
            st.write("관련 공고를 찾을 수 없습니다.")

