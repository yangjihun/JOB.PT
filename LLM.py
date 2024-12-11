import openai
import os

# .env에서 API 키 로드
openai.api_key = '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'
question = input("무엇을 물어볼까요? : ")

def get_completion(prompt, model="gpt-4"):  # 모델을 gpt-4로 변경
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return response["choices"][0]["message"]["content"]

# 테스트용 프롬프트
prompt = "Tell me a fun fact about Python programming."
response = get_completion(prompt)
print(response)