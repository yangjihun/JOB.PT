#MBC 크롤링(완료+파일생성)

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def search_mbc_news(keyword, max_news=23): #max_nerws=23 23개의 뉴스 (이 값을 원하는 값으로 수정해주세요)
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # 필요에 따른 headless 모드 추가
    # chrome_options.add_argument("--headless")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 10)

    try:
        base_url = "https://imnews.imbc.com/pc_main.html"
        driver.get(base_url)

        search_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "search")))
        search_button.click()

        search_box = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="kwd"]')))
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)

        news_count = 0
        page_number = 1  # 페이지 번호 초기화

        with open("news.txt", "a", encoding="utf-8") as file:
            while news_count < max_news:
                try:
                    news_list = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="result"]/div[2]/div/div[3]/ul')))
                    news_items = news_list.find_elements(By.TAG_NAME, 'li')

                    if not news_items:  # 검색 결과가 없는 경우 처리
                        print("검색 결과가 없습니다.")
                        return

                    for news_item in news_items:
                        if news_count >= max_news:
                            break

                        try:  # 제목 또는 링크를 검색할 수 없는 경우를 대비
                            title = news_item.find_element(By.TAG_NAME, 'a').text
                            link = news_item.find_element(By.TAG_NAME, 'a').get_attribute('href')

                            # 파일에 저장 (출력 생략)
                            file.write(f"Title: {title}\n")
                            file.write("-" * 50 + "\n")

                            news_count += 1
                        except Exception:
                            continue  # 해당 아이템 건너뛰기

                    if news_count >= max_news:
                        break

                    # 다음 페이지 버튼 클릭 (마지막 페이지가 아닌 경우)
                    try:
                        page_number += 1
                        page_button_xpath = f'//*[@id="result"]/div[2]/div/div[3]/div/div/a[{page_number}]'
                        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, page_button_xpath)))
                        next_button.click()
                        time.sleep(2)  # 페이지 로딩 대기 시간 추가
                    except Exception:
                        break

                except Exception:
                    break

        print("작업이 완료되었습니다.")

    finally:
        driver.quit()

if __name__ == "__main__":
    keyword = input("검색할 키워드를 입력하세요: ")
    search_mbc_news(keyword)
