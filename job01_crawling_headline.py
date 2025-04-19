from bs4 import BeautifulSoup   # HTML 파싱
import requests                 # 웹요청
import re                       # 정규식
import pandas as pd             # 데이터프레임 처리
import datetime                 # 파일명에 날짜 넣기용

# 섹터별 레이블 지정
category = ['Energy', 'Healthcare', 'Industrials', 'Real_Estate']
# 섹션의 뉴스 제목을 저장할 데이터프레임 초기화
df_titles = pd.DataFrame()

# 섹션 뉴스별 URL을 생성
for i in range(6):
    url = 'https://finance.yahoo.com/sectors/energy/'.format(i)  # 에너지 섹터 URL
    # 해당 URL로 HTTP GET 요청을 보내고, 응답받은 HTML을 파싱해서 soup 객체에 저장
    resp = requests.get(url)  # 서버에 해당 URL 정보 요청 (HTTP의 GET 요청)
    soup = BeautifulSoup(resp.text, 'html.parser')  # 응답받은 내용 정리
    # soup 객체의 전체 내용 출력(디버깅용)
    print(list(soup))


    # HTML에서 .sa_text_strong 클래스를 가진 요소를 모두 선택, 이게 각 기사 제목부분에 해당하는 태그
    title_tags = soup.select('.sa_text_strong')  # soup에서 sa_text_strong 클래스를 가진 것들만 선택
    print(list(title_tags))

    titles = []
    for tag in title_tags:
        titles.append(tag.text)
    print(titles)


    #
    df_section_titles = pd.DataFrame(titles, columns=['titles'])
    df_section_titles['category'] = category[i]
    df_titles = pd.concat([df_titles, df_section_titles],
                          axis='rows', ignore_index=True)
print(df_titles.head())
df_titles.info()
print(df_titles.category.value_counts())
df_titles.to_csv('./crawling_data/naver_headline_news_{}.csv'.format(
    datetime.datetime.now().strftime('%Y%m%d')), index=False)
