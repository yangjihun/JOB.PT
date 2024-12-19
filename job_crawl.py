import requests
from bs4 import BeautifulSoup

def crawl_jobkorea(search_keyword):
    """
    JobKorea에서 특정 검색어에 대한 공고 제목과 링크를 크롤링합니다.

    Args:
        search_keyword (str): 검색어

    Returns:
        list[dict]: 공고 제목과 링크를 포함한 딕셔너리 리스트
    """
    results_list = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    base_url = "https://www.jobkorea.co.kr/Search/?stext="
    search_url = base_url + requests.utils.quote(search_keyword)  # 검색어를 URL에 추가

    try:
        # HTML 페이지 요청
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()  # HTTP 상태 코드 확인
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 검색 결과의 제목과 링크 추출
        job_posts = soup.select("a.information-title-link.dev-view")  # 제목 링크 요소 선택
        for idx, post in enumerate(job_posts[:3], 1):  # 상위 3개 공고만 가져옴
            title = post.text.strip()
            link = post['href']
            if not link.startswith("http"):
                link = "https://www.jobkorea.co.kr" + link  # 상대 경로 처리
            results_list.append({"title": title, "link": link})

    except requests.exceptions.RequestException as e:
        print(f"HTTP 요청 중 오류 발생: {e}")

    return results_list
