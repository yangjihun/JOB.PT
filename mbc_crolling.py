#MBC 크롤링(완료+파일생성) 12-18 수정 완료

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def search_mbc_news(keyword, max_news):
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # 필요에 따른 headless 모드 추가
    # chrome_options.add_argument("--headless")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        base_url = "https://imnews.imbc.com/pc_main.html"
        driver.get(base_url)

        driver.find_element(By.CLASS_NAME, "search").click()
        search_box = driver.find_element(By.XPATH, '//*[@id="kwd"]')
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)

        news_count = 0
        page_number = 1

        with open("News.txt", "a", encoding="utf-8") as file:
            while news_count < max_news:
                news_items = driver.find_elements(By.XPATH, '//*[@id="result"]/div[2]/div/div[3]/ul/li')

                if not news_items:
                    print("검색 결과가 없습니다.")
                    return

                for news_item in news_items:
                    if news_count >= max_news:
                        break

                    try:
                        title = news_item.find_element(By.TAG_NAME, 'a').text
                        link = news_item.find_element(By.TAG_NAME, 'a').get_attribute('href')

                        # 뉴스 상세 페이지 접속
                        driver.get(link)

                        # 한 번의 시도로 본문 찾기
                        report_content = ""
                        try:
                            report_content = driver.find_element(By.CLASS_NAME, "report").text
                        except:
                            try:
                                report_content = driver.find_element(By.CLASS_NAME, "news_txt").text
                            except:
                                report_content = "본문을 찾을 수 없습니다."

                        # 파일에 저장
                        file.write(f"Title: {title}\n")
                        file.write(f"Link: {link}\n")
                        file.write(f"Content: {report_content}\n")
                        file.write("-" * 50 + "\n")

                        news_count += 1
                        driver.back()
                    except Exception as e:
                        print(f"Error processing news item: {e}")
                        continue

                if news_count >= max_news:
                    break

                try:
                    page_number += 1
                    next_button = driver.find_element(By.XPATH, f'//*[@id="result"]/div[2]/div/div[3]/div/div/a[{page_number}]')
                    next_button.click()
                    time.sleep(1)  # 로딩 시간 최소화
                except:
                    break

        print("작업이 완료되었습니다.")

    finally:
        driver.quit()
