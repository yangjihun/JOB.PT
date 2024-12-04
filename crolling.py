import requests
from bs4 import BeautifulSoup
import time

# RISS 검색 URL
BASE_URL = "https://www.riss.kr/search/Search.do"

# 검색어 입력
search_query = "금융"

# 검색 요청 파라미터 설정
params = {
    "query": search_query,
    "searchGubun": "true",
    "colName": "re_a_kor",
    "isDetailSearch": "N",
}

# 검색 결과 가져오기
response = requests.get(BASE_URL, params=params)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

# 검색 결과 추출
results = soup.find_all("div", class_="cont")  # 검색 결과가 포함된 태그
if not results:
    print("No results found.")
    exit()

# 첫 5개 논문 정보 추출
for i, result in enumerate(results[:5]):
    try:
        # 논문 제목
        title = result.find("p", class_="title").text.strip()

        # 논문 저자
        author = result.find("span", class_="writer").text.strip() if result.find("span", class_="writer") else "Unknown"

        # 상세 페이지 URL
        detail_link = result.find("p", class_="title").find("a")["href"]
        if not detail_link.startswith("http"):
            detail_link = "https://www.riss.kr" + detail_link

        # 상세 페이지에서 초록 가져오기
        time.sleep(1)  # 요청 간 간격 유지
        detail_response = requests.get(detail_link)
        detail_response.raise_for_status()
        detail_soup = BeautifulSoup(detail_response.text, "html.parser")

        # BeautifulSoup로 초록 추출
        abstract_div = detail_soup.find("div", class_="text off")  # CSS Selector로 추출
        abstract_text = abstract_div.text.strip() if abstract_div else "Abstract not available."

        # 출력
        print(f"\nResult {i + 1}")
        print(f"Title: {title}")
        print(f"Author: {author}")
        print(f"Abstract: {abstract_text}")
        print(f"URL: {detail_link}")

    except Exception as e:
        print(f"Error fetching result {i + 1}: {e}")

