
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

# 광고 제외
def is_ad_element(element):
    ad_id = element.get_attribute("id")
    return ad_id and ad_id.startswith("internal_trc_")

# 설정
options = ChromeOptions()
service = ChromeService(executable_path=ChromeDriverManager().install()) # 크롬 드라이버 설치
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)

# 광고 형태 '//*[@id="internal_trc_2290972430"]/div/a[1]/span/span[1]'

# 카테고리 설정
category = ['Energy', 'Healthcare', 'Industrials', 'Real_Estate']
df_titles = pd.DataFrame()
print("news headline and summary crawling try")
category_name = 'Industrials'

# 크롤링 대상 URL
finance_energy_url =  'https://finance.yahoo.com/sectors/industrials/'

# 광고요소 제거
def remove_ads():
    driver.execute_script("""
        var ads = document.querySelectorAll('div[id^="internal_trc_"]');
        ads.forEach(e => e.remove());
    """)

# 창 띄우기
print(f"[{category_name}] 뉴스 크롤링 시작")
driver.get(finance_energy_url)
time.sleep(5)


news_data = []
scroll_count = 0
max_scrolls = 20
last_height = driver.execute_script("return document.body.scrollHeight")

# Energy news 설정
try:
    while scroll_count < max_scrolls:
        remove_ads()  # 매 스크롤마다 광고 제거

        # 뉴스 항목(li)만 선택
        items = driver.find_elements(By.XPATH, '//*[@id="nimbus-app"]/section[1]/section[1]/section[1]/article/section[6]//ul/li')

        for idx, item in enumerate(items):
            try:
                h3_tags = item.find_elements(By.TAG_NAME, 'h3')
                p_tags = item.find_elements(By.TAG_NAME, 'p')

                if not h3_tags or not p_tags:
                    continue  # 뉴스 구조가 아닌 경우 건너뜀 (광고 등)

                title = h3_tags[0].text.strip()
                summary = p_tags[0].text.strip()

                # news_data.append({
                #     'title': title,
                #     'summary': summary,
                #     'category': category_name
                # })

                if not any(d['title'] == title for d in news_data):  # 중복 제거
                    print(f"[{idx+1}] HEADLINE: {title}")
                    print(f"[{idx+1}] SUMMARY : {summary}")
                    print("-" * 40)

                    news_data.append({
                        'title': title,
                        'summary': summary,
                        'category': category_name
                    })
            except Exception as e:
                print(f"li[{idx+1}] 에러: {e}")
                continue

        # 스크롤 다운
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        scroll_count += 1

except Exception as e:
    print("크롤링 중 오류 발생:", e)

finally:
    driver.quit()

# ✅ 결과 저장
df_news = pd.DataFrame(news_data)
file_name = '{}_titles_news_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d'), category_name)
df_news.to_csv(file_name, index=False)

print(f"✅ 저장 완료: {file_name}")