#SBS 크롤링(완료+파일생성)
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
import time

def search_sbs_news(search_term, total_news=5, output_file="News.txt"):
    
    # Chrome 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # 브라우저 최대화

    # ChromeDriver 경로 설정
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # WebDriverWait 설정
    wait = WebDriverWait(driver, 10)

    try:
        # SBS 뉴스 페이지 열기
        driver.get("https://news.sbs.co.kr/news/newsMain.do?plink=GNB&cooper=SBSNEWS")

        # 검색 버튼 클릭
        search_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="header_search_input"]')))
        search_button.click()

        # 검색 창에 검색어 입력
        search_bar = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="search-bar"]')))
        search_bar.send_keys(search_term)
        search_bar.send_keys(Keys.RETURN)  # Enter 키로 검색 실행

        # 뉴스 탭 클릭
        news_tab = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id=\"tab\"]/ul/li[2]/a')))
        news_tab.click()

        # 뉴스 크롤링 변수 초기화
        news_count = 0
        page_number = 1

        # 결과 저장을 위한 파일 오픈
        with open(output_file, "a", encoding="utf-8") as file:
            while news_count < total_news:
                for idx in range(1, 11):  # 한 페이지당 10개의 뉴스
                    try:
                        # 뉴스 제목과 링크 가져오기
                        title_xpath = f'//*[@id="search-article"]/div/div[4]/ul/li[{idx}]/a/span[2]/strong'
                        link_xpath = f'//*[@id="search-article"]/div/div[4]/ul/li[{idx}]/a'

                        title = wait.until(EC.presence_of_element_located((By.XPATH, title_xpath))).text
                        link = wait.until(EC.presence_of_element_located((By.XPATH, link_xpath))).get_attribute("href")

                        file.write(f"{news_count + 1}: {title}\n")

                        # 각 뉴스 링크에 바로 접속
                        driver.get(link)
                        time.sleep(3)  # 페이지 로드 대기

                        # 뉴스 본문 크롤링
                        try:
                            article_body = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "text_area"))).text
                            if article_body:
                                file.write(f"본문: {article_body}\n\n")
                        except TimeoutException:
                            print("본문을 찾을 수 없습니다.")
                            file.write("본문을 찾을 수 없습니다.\n\n")

                        # 검색 결과 페이지로 복귀
                        driver.back()
                        time.sleep(2)

                        news_count += 1
                        if news_count >= total_news:
                            break

                    except (TimeoutException, StaleElementReferenceException):
                        print(f"{news_count + 1}: 요소가 더 이상 유효하지 않습니다.")

                # 다음 페이지로 이동
                if news_count < total_news:
                    try:
                        next_button_xpath = f'//*[@id="search-article"]/div/div[5]/div/a[{page_number + 2}]'
                        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, next_button_xpath)))
                        next_button.click()
                        page_number += 1
                        time.sleep(3)  # 페이지 로드 대기
                    except TimeoutException:
                        print("더 이상 다음 페이지가 없습니다.")
                        break

    except TimeoutException:
        print("\n요소를 찾지 못했습니다. 페이지 로드 상태를 확인하거나 XPATH를 점검하세요.")

    finally:
        # 브라우저 닫기
        driver.quit()
        print(f"작업이 완료되었습니다.")


