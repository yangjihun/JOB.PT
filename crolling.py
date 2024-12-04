from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# ChromeDriver 자동 설치 및 경로 설정
service = Service(ChromeDriverManager().install())

# Chrome 드라이버 초기화
driver = webdriver.Chrome(service=service)

# 웹 페이지 열기
driver.get('https://www.riss.kr/search/detail/DetailView.do?p_mat_type=1a0202e37d52c72d&control_no=98bfef90e76549d1ffe0bdc3ef48d419&keyword=%EA%B8%88%EC%9C%B5')

# 페이지가 로딩될 때까지 기다리기 (예: 10초)
wait = WebDriverWait(driver, 10)

# # 접힌 텍스트 추출 (확장 전)
# collapsed_text_xpath = '//*[@id="additionalInfoDiv"]/div/div[1]/div[2]/p'
# collapsed_text_element = wait.until(EC.presence_of_element_located((By.XPATH, collapsed_text_xpath)))
# collapsed_text = collapsed_text_element.text
# print("접힌 텍스트:", collapsed_text)

# 텍스트 확장 버튼 클릭 (해당 버튼의 XPath)
expand_button_xpath = '//*[@id="additionalInfoDiv"]/div/div[1]/a'
expand_button = wait.until(EC.element_to_be_clickable((By.XPATH, expand_button_xpath)))
expand_button.click()  # 버튼 클릭

# 페이지가 업데이트 될 때까지 잠시 대기 (예: 2초)
time.sleep(2)

# 열려진 텍스트 추출 (확장 후)
expanded_text_xpath = '//*[@id="additionalInfoDiv"]/div/div[1]/div[3]/p'
expanded_text_element = wait.until(EC.presence_of_element_located((By.XPATH, expanded_text_xpath)))
expanded_text = expanded_text_element.text
print("열린 텍스트:", expanded_text)

# 브라우저 종료
driver.quit()