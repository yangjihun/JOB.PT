import streamlit as st
from openai import OpenAI
import json

# API 키 및 클라이언트 설정
client = OpenAI(api_key="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")

# Streamlit UI 설정
st.title("사회 트렌드 분석")
st.write("사회 트렌드 분석을 기반으로 관련 직업과 필요한 핵심 스킬을 추천합니다.")

# 사용자 입력 받기
q = st.text_input("분야를 입력하세요:")

# 데이터 파일 읽기
with open("data.txt", "r", encoding="utf-8") as f:
    trend = f.read()

if q:
    # OpenAI API 호출
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": f"사회 트렌드 분석 결과는 다음과 같습니다: {trend}. 사회 트렌드 분석 결과를 말하고, 이를 기반으로 {q} 내용과 연관된 직업을 3개 말하시오. 그 직무를 위한 필요 핵심 스킬 3가지도 말하시오."}
        ]
    )

    # 결과 처리 및 출력
    result = response.choices[0].message.content
    
    # 결과를 JSON 형식으로 포맷팅하여 보기 좋게 출력
    try:
        result_json = json.loads(result)  # JSON 파싱
        pretty_result = json.dumps(result_json, ensure_ascii=False, indent=4)  # 예쁘게 포맷팅
        st.subheader("분석 결과:")
        st.json(pretty_result)  # Streamlit의 json 출력 형식
    except json.JSONDecodeError:
        st.write("분석 결과를 JSON으로 파싱하는데 오류가 발생했습니다. 다시 시도해 주세요.")