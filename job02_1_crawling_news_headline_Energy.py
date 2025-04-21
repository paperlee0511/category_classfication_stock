
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

# 설정
options = ChromeOptions()
service = ChromeService(executable_path=ChromeDriverManager().install()) # 크롬 드라이버 설치
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)

news_headline = '//*[@id="nimbus-app"]/section/section/section/article/section[6]/div[2]/div/div/div/ul/li[{}]/section/div/a/h3'
news_summary = '//*[@id="nimbus-app"]/section/section/section/article/section[6]/div[2]/div/div/div/ul/li[{}]/section/div/a/p'

# 광고 형태 '//*[@id="internal_trc_2290972430"]/div/a[1]/span/span[1]'

# 카테고리 설정
category = ['Energy', 'Healthcare', 'Industrials', 'Real_Estate']
df_titles = pd.DataFrame()
print("news headline and summary crawling try")

# 크롤링 대상 URL
finance_energy_url =  'https://finance.yahoo.com/sectors/energy/'
driver.get(finance_energy_url)
time.sleep(5)

headline = []
summary = []

# Energy news 설정
try :
    # for문으로 돌려야 하나?
    driver.find_element(By.XPATH, button_sector_select).click()     # 섹터 선택창 클릭
    # reset으로 변경, reset 정의
    reset_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'link2-btn') and contains(., 'Reset')]")))
    reset_button.click()
    #driver.find_element(By.XPATH, button_sector_tech).click()       # tech 해제
    driver.find_element(By.XPATH, button_sector_real_estate).click()     # real_estate 섹터 클릭
    # apply 정의
    apply_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, apply_xpath)))

    apply_button.click()     # apply 섹터 클릭
    time.sleep(1)

except Exception as e:
    print("필터 설정 중 오류 발생")

# 결과 수집 시작
titles = []
max_page = 27
for i in range(max_page):
    print(f"page {i+1} 수집중...")
    for j in range(1, 101):
        try :
            x_path = f'//*[@id="nimbus-app"]/section/section/section/article/section/div/div[5]/div[1]/table/tbody/tr[{j}]/td[3]/div'
            name = wait.until(EC.presence_of_element_located((By.XPATH, x_path))).text
            titles.append(name)
            fail_count = 0 # 성공시 실패 카운터 초기화
        except :
            print(f"기업 {j}정보 수집 실패")
            fail_count += 1
            if fail_count >= 3:
                print("기업정보 3번 이상 실패, 페이지 종료")
                break

    # 다음 페이지 버튼 클릭
    try :
        # 다음 페이지 버튼
        next_btn_x_path = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, button_next))).click()
        time.sleep(2)
    except :
        print("다음 페이지 없음 또는 클릭 실패")
        break

# DataFrame

df_real_estate_titles = pd.DataFrame(titles, columns=['titles'])
df_real_estate_titles['category'] = 'Real_Estate'
df_titles = pd.concat([df_titles, df_real_estate_titles],axis='rows', ignore_index=True)

# save
df_titles.to_csv('{}_titles_Real_Estate.csv'.format(datetime.datetime.now().strftime('%Y%m%d')), index=False)

print("저장 완료: Real_Estate 기업 수집 종료")
