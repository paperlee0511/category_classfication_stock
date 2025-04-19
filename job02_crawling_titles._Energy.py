
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import datetime

options = ChromeOptions()

service = ChromeService(executable_path=ChromeDriverManager().install()) # 크롬 드라이버 설치
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)

category = ['Energy', 'Healthcare', 'Industrials', 'Real_Estate']
df_titles = pd.DataFrame()

print("Energy crawling")

# 크롤링 대상 URL
energy_url =  'https://finance.yahoo.com/research-hub/screener/sec-ind_ind-largest-equities_software-infrastructure/?start=0&count=100'
driver.get(energy_url)
time.sleep(5)

button_sector_delete1 = '//*[@id="nimbus-app"]/section/section/section/article/section/div/div[3]/div/div[5]/button/div'
button_sector_delete2 = '//*[@id="nimbus-app"]/section/section/section/article/section/div/div[3]/div/div[4]/button/div'
button_sector_select = '//*[@id="nimbus-app"]/section/section/section/article/section/div/div[3]/div/div[3]/div/button'
button_sector_tech = '//*[@id="Technology"]'
button_sector_energy = '//*[@id="Energy"]'
apply_xpath = '//button[text()="Apply" and not(@disabled)]'
button_select = '//*[@id="nimbus-app"]/section/section/section/article/section/div/div[5]/div[2]/div[1]/div/div/div/button'
button_select_100 = '//*[@id="opt-8234"]'
button_next = '//*[@id="nimbus-app"]/section/section/section/article/section/div/div[5]/div[2]/div[3]/button[3]'

# Energy 카테고리 필터 설정
try :
    driver.find_element(By.XPATH, button_sector_delete1).click()    # 필터 5 제거
    driver.find_element(By.XPATH, button_sector_delete2).click()    # 필터 4 제거
    driver.find_element(By.XPATH, button_sector_select).click()     # 섹터 선택창 클릭
    driver.find_element(By.XPATH, button_sector_tech).click()       # tech 해제
    driver.find_element(By.XPATH, button_sector_energy).click()     # encergy 섹터 클릭

    apply_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, apply_xpath)))

    apply_button.click()     # apply 섹터 클릭
    time.sleep(1)

except Exception as e:
    print("필터 설정 중 오류 발생")

# 결과 수집 시작
titles = []
max_page = 10
for i in range(max_page):
    print(f"page {i+1} 수집중...")
    for j in range(1, 101):
        try :
            x_path = f'//*[@id="nimbus-app"]/section/section/section/article/section/div/div[5]/div[1]/table/tbody/tr[{j}]/td[3]/div'
            name = wait.until(EC.presence_of_element_located((By.XPATH, x_path))).text
            titles.append(name)
        except :
            print(f"기업 {j}정보 수집 실패")

    # 다음 페이지 버튼 클릭
    try :
        # 다음 페이지 버튼
        next_btn_x_path = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, button_next))).click()
        time.sleep(2)
    except :
        print("다음 페이지 없음 또는 클릭 실패")
        break

# DataFrame

df_energy_titles = pd.DataFrame(titles, columns=['titles'])
df_energy_titles['category'] = 'Energy'
df_titles = pd.concat([df_titles, df_energy_titles],axis='rows', ignore_index=True)

# save
df_titles.to_csv('{}_titles_Energy.csv'.format(datetime.datetime.now().strftime('%Y%m%d')), index=False)

print("저장 완료: Energy 기업 수집 종료")

# for i in range(1, 6): # 5회
#     for j in range(1, 7): # 1부터 6까지
#         title_path = '//*[@id="newsct"]/div[4]/div/div[1]/div[{}]/ul/li[{}]/div/div/div[2]/a/strong'.format(i, j)
#         try: # 해당 경로가 없을 수도 있으니까 예외 처리를 위한 try-except 문
#             title = driver.find_element(By.XPATH, title_path).text # 요소 찾기.text
#             print(title)
#             titles.append(title)
#         except:
#             print('error', i, j)
# df_politics_titles = pd.DataFrame(titles, columns=['titles'])
# df_politics_titles['category'] = 'Politics'
# df_titles = pd.concat([df_titles, df_politics_titles],
#                       axis='rows', ignore_index=True)
#
# time.sleep(1)
#
# print("Economic crawling")
#
# titles = []
#
# economic_url = 'https://news.naver.com/section/101'
# driver.get(economic_url)
# time.sleep(5)
# button_xpath = '//*[@id="newsct"]/div[5]/div/div[2]/a' # '기사 더보기' 버튼의 상대 경로(id 기준)
# for i in range(15): # 15번 반복
#     time.sleep(0.5) # 약간의 시간 딜레이
#     driver.find_element(By.XPATH, button_xpath).click() # 설정한 경로의 버튼을 클릭
# time.sleep(5) # 5초 기다리기
#
# for i in range(1, 6): # 5회
#     for j in range(1, 7): # 1부터 6까지
#         # title path: //*[@id="newsct"]/div[5]/div/div[1]/div[1]/ul/li[1]/div/div/div[2]/a/strong
#         title_path = '//*[@id="newsct"]/div[5]/div/div[1]/div[{}]/ul/li[{}]/div/div/div[2]/a/strong'.format(i, j)
#         try: # 해당 경로가 없을 수도 있으니까 예외 처리를 위한 try-except 문
#             title = driver.find_element(By.XPATH, title_path).text # 요소 찾기.text
#             print(title)
#             titles.append(title)
#         except:
#             print('error', i, j)
#
# df_economic_titles = pd.DataFrame(titles, columns=['titles'])
# df_economic_titles['category'] = 'Economic'
# df_titles = pd.concat([df_titles, df_economic_titles],
#                       axis='rows', ignore_index=True)
#
# # csv 파일로 크롤링한 제목들 저장하기
# df_titles.to_csv('{}_titles_Politics_Economic.csv'.format(datetime.datetime.now().strftime('%Y%m%d')), index=False)