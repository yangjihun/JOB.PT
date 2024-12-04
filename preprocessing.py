import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# nltk 리소스 다운로드 (한 번만 실행)
# nltk.download('punkt')
# nltk.download('stopwords')

# 텍스트 파일 읽기
with open('text.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# 1. 소문자화
text = text.lower()

# 2. 구두점 및 특수 문자 제거
text = re.sub(r'[^\w\s]', '', text)

# 3. 불용어 제거
stop_words = set(stopwords.words('korean'))  # 한국어 불용어를 사용하려면 nltk를 통한 불용어 리스트가 필요
words = word_tokenize(text)
filtered_words = [word for word in words if word not in stop_words]

# 4. 공백 및 줄 바꿈 처리
cleaned_text = ' '.join(filtered_words)

print(cleaned_text)