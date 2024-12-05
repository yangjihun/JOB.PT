from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Chrome 드라이버 자동 설치 및 경로 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# RISS 사이트 접속
driver.get('https://www.riss.kr/')
print("RISS 사이트 접속 완료")

# 명시적 대기 (검색창이 사용 가능할 때까지 기다리기)
wait = WebDriverWait(driver, 10)
search_box = wait.until(EC.element_to_be_clickable((By.NAME, 'query')))
print("검색창 활성화됨")

# 팝업 닫기 - 업데이트
main_window = driver.current_window_handle
all_windows = driver.window_handles

for window in all_windows:
    if window != main_window:
        driver.switch_to.window(window)
        driver.close()
        print("팝업 창 닫음")

driver.switch_to.window(main_window)

# 검색어 입력
search_box.send_keys('금융')
search_box.send_keys(Keys.RETURN)
print("검색어 '금융' 입력 및 검색 실행")

# "국내학술논문" 클릭
try:
    domestic_papers_tab = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="tabMenu"]/ul/li/div/ul/li[2]/a'))
    )
    domestic_papers_tab.click()
    print("'국내학술논문' 탭 클릭")
    time.sleep(3)  # 페이지 로딩 대기
except Exception as e:
    print(f"'국내학술논문' 탭 클릭 실패: {e}")
    driver.quit()
    exit()

# 상위 5개 논문 탐색 및 출력
paper_list_xpath = '//*[@id="divContent"]/div/div[2]/div/div[3]/div[2]/ul/li/div[2]/p/a'

def get_paper_links():
    """현재 페이지에서 논문 제목과 링크를 가져오는 함수"""
    try:
        # 리스트 재탐색
        paper_elements = driver.find_elements(By.XPATH, paper_list_xpath)
        return paper_elements
    except Exception as e:
        print(f"논문 요소 재탐색 실패: {e}")
        return []

# 텍스트 파일 경로 설정
file_path = "papers_info.txt"

# 파일 열기 (쓰기 모드)
with open(file_path, 'w', encoding='utf-8') as file:
    # 파일에 헤더 추가 (선택 사항)
    file.write("논문 제목과 초록 목록\n\n")

    print("논문 목록 탐색 중...")
    paper_elements = get_paper_links()

    if paper_elements:
        for i in range(min(5, len(paper_elements))):
            try:
                # 재탐색을 통해 요소를 새로 가져옴
                paper_elements = get_paper_links()
                paper = paper_elements[i]
                title = paper.text
                link = paper.get_attribute('href')
                print(f"{i+1}. {title}\n")

                # 논문 페이지로 이동하여 초록 추출
                driver.get(link)
                print(f"논문 페이지 접속: {link}")

                # 텍스트 확장 버튼 클릭
                expand_button_xpath = '//*[@id="additionalInfoDiv"]/div/div[1]/a'
                try:
                    expand_button = wait.until(EC.element_to_be_clickable((By.XPATH, expand_button_xpath)))
                    expand_button.click()
                    print("텍스트 확장 버튼 클릭")
                except:
                    print("텍스트 확장 버튼 없음")

                # 초록 텍스트 추출
                abstract_xpath = '//*[@id="additionalInfoDiv"]/div/div[1]/div[3]/p'
                try:
                    abstract_element = wait.until(EC.presence_of_element_located((By.XPATH, abstract_xpath)))
                    abstract_text = abstract_element.text
                    print("초록:", abstract_text)
                except:
                    abstract_text = "초록을 찾을 수 없습니다."
                    print("초록을 찾을 수 없습니다.")

                # 파일에 논문 제목과 초록 저장
                file.write(f"{i+1}. {title}\n")
                file.write(f"초록: {abstract_text}\n\n")

                # 검색 결과 페이지로 돌아가기
                driver.back()
                print("검색 결과 페이지로 돌아옴")

                # 페이지 로드 대기
                time.sleep(2)

            except Exception as e:
                print(f"논문 정보 가져오기 실패: {e}")
    else:
        print("논문 목록을 찾을 수 없습니다.")

# 크롬 드라이버 종료
driver.quit()
print("크롬 드라이버 종료")
print(f"논문 제목과 초록 정보가 {file_path} 파일에 저장되었습니다.")
