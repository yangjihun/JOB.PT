# P-Project

## 프로젝트 개요
JOB.PT는 입력한 분야를 기반으로 논문/뉴스 트렌드를 분석해 관련 직업과 필요 역량을 추천하는 Streamlit 앱입니다.

## 기획 요약
- 문제: 관심 분야에 맞는 직업과 필요한 역량을 빠르게 파악하기 어렵다
- 목표: 최신 논문/뉴스 트렌드를 반영한 직업 3개와 필요 역량을 제시한다
- 대상: 진로 탐색 중인 학생/구직자, 직무 리서치가 필요한 사용자
- 출력: 추천 직업 3개 + 각 직업별 필요 역량 + 관련 채용 링크(잡코리아)

## 주요 기능
- RISS 논문 크롤링을 통해 분야 트렌드 요약용 데이터 수집
- KBS/MBC/SBS 뉴스 크롤링으로 사회 이슈 반영
- OpenAI 모델을 사용한 Self-Consistency 3회 실행 후 빈도 기반 상위 직업 선정
- 직업별 필요 역량 제시 및 잡코리아 공고 링크 제공

## 기술 스택
- Python 3
- Streamlit
- OpenAI API (gpt-4o-mini)
- Selenium + webdriver-manager
- Requests + BeautifulSoup4
- python-dotenv

## 폴더 구조
- `backend/app.py` : Streamlit 앱 엔트리
- `backend/crolling/` : RISS/뉴스/잡코리아 크롤러 모듈
- `backend/data.txt` : 논문 크롤링 결과
- `backend/News.txt` : 뉴스 크롤링 결과
- `backend/requirements.txt` : 의존성

## 실행 방법 (PowerShell)
```powershell
cd c:\Users\avjab\OneDrive\Desktop\project\P-Project\P-Project\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

`.env` 파일 생성:
```
OPENAI_API_KEY=your_key_here
```

모듈 경로 설정 및 실행:
```powershell
$env:PYTHONPATH="$PWD\crolling"
streamlit run app.py
```

## 주의사항
- 최초 실행 시 Selenium이 크롬 드라이버를 다운로드하므로 네트워크가 필요합니다.
- 크롬 설치가 필요합니다.
- 크롤링 결과는 `backend` 폴더 기준 상대경로로 저장/조회됩니다.
