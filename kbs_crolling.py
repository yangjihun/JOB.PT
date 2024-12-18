#KBS 크롤링(완료+파일생성) 12-18 ㅅ

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def search_kbs_news(keyword, max_results):
    """
    KBS 뉴스 웹사이트에서 지정된 키워드로 뉴스를 검색하고 결과를 크롤링하여 파일로 저장합니다.

    Parameters:
        keyword (str): 검색할 키워드
        max_results (int): 최대 크롤링할 뉴스 개수

    Returns:
        None
    """
    # ChromeOptions 설정 (옵션)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # GUI 없는 환경에서 필수
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")  # GPU 사용 비활성화
    chrome_options.add_argument("--window-size=1920x1080")  # 가상 디스플레이 설정

    # 크롬 드라이버 자동 설치 및 설정
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # KBS 뉴스 메인 페이지로 이동
        base_url = "https://news.kbs.co.kr/news/pc/main/main.html?ref=pLogo"
        driver.get(base_url)

        # 페이지가 완전히 로드될 때까지 대기
        wait = WebDriverWait(driver, 10)

        # 검색 버튼 클릭
        search_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "search-btn")))
        search_button.click()

        # 검색창이 나타날 때까지 대기
        search_box = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "search-box-input")))

        # 검색어 입력 및 검색 실행
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)

        # 결과 로드 대기
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id=\"contents\"]/div[2]/div[1]/div[4]')))

        # 검색 결과 수집
        results = []
        current_page = 1

        while len(results) < max_results:
            # 현재 페이지의 뉴스 기사 수집
            news_list = driver.find_element(By.CLASS_NAME, "box-contents")
            articles = news_list.find_elements(By.CLASS_NAME, "title")

            for article in articles:
                if len(results) >= max_results:
                    break
                title = article.text
                link = article.find_element(By.XPATH, './ancestor::a').get_attribute("href")
                results.append({"title": title, "link": link})

            # 페이지 ID를 변경하여 이동
            try:
                next_page_id = f"page{current_page + 1}"
                next_page_button = driver.find_element(By.ID, next_page_id)
                next_page_button.click()
                time.sleep(2)  # 페이지 로드 대기
                current_page += 1
            except Exception:
                # 더 이상 페이지가 없으면 종료
                break

        # 각 링크에 접속하여 추가 정보 추출
        for result in results:
            driver.get(result["link"])
            time.sleep(2)  # 페이지 로드 대기
            try:
                # 기사 내용 추출
                content_element = driver.find_element(By.CLASS_NAME, "detail-body")  # 기사 내용이 들어있는 클래스명
                result["content"] = content_element.text.strip()
            except Exception:
                result["content"] = "기사 내용을 가져올 수 없습니다."

        # 결과를 텍스트 파일로 저장
        with open("News.txt", "w", encoding="utf-8") as file:
            for result in results:
                file.write(f"Title: {result['title']}\n")
                file.write(f"Link: {result['link']}\n")
                file.write(f"Content: {result['content']}\n")
                file.write("-" * 50 + "\n")

        print("작업이 완료되었습니다.")

    finally:
        # 크롤링이 끝나면 브라우저 종료
        driver.quit()