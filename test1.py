# LLM OpenAI API
from openai import OpenAI
import json

# OpenAI 클라이언트 생성
client = OpenAI(api_key="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")

# 사용자 입력
q = input("분야? ")

# 데이터 로드
trend = open("data.txt", "r", encoding="utf-8").read()
News = open("News.txt", "r", encoding="utf-8").read()

# 결과 저장용 리스트
answers = []

# 5회 반복 실행 (Self-Consistency)
for i in range(3):
    # 첫 번째 요청: 사회 트렌드와 분야의 연관성을 분석
    response1 = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON. Please write in Korean."},
            {"role": "user", "content": f"사회 트렌드 분석 결과는 다음과 같습니다: {trend}. 이를 기반으로 '{q}'와 연관된 사회 트렌드를 분석하고, 중간 결과를 나타내시오."}
        ]
    )
    result1 = response1.choices[0].message.content

    # 두 번째 요청: 중간 결과를 활용하여 직업을 추천
    response2 = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON. Please write in Korean."},
            {"role": "user", "content": f"이전 분석 결과는 다음과 같습니다: {result1}. 이를 기반으로 '{News}'의 내용을 참고하여 추천할 만한 관련 직업 3개를 명시하세요. 출력값은 다음과 같은 형식을 따르세요. {{'직업':[의사,회계사,작곡가]}}."}
        ]
    )
    result2 = response2.choices[0].message.content
    
    result2 = json.loads(result2)
    answers.append(result2["직업"])
response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON. Please write in Korean."},
            {"role": "user", "content": f"{answers}의 내용에서 가장 많이 나온 직업 3개와 각 직업에 대한 필요 역량을 답변하세요. 출력값은 다음과 같은 형식을 따르세요. {{'직업':[의사,회계사,작곡가], '필요역량':[의사자격증,수학지식,음악감각]}}. 직업[0]에 대한 필요역량은 필요역량[0]에 해당하는 방식이다."}
        ]   
    )

result = response.choices[0].message.content

# 결과 출력
print("Self-Consistency를 통한 최종 답변:\n", result)