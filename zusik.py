# 1961801 권강민 국내주식 주식정보 크롤링
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import pandas as pd
import time

# 조회 항목 설정(원하는 항목)
print()
select_list = ['거래량', '매수호가', '거래대금', '시가총액', '영업이익', 'PER', '시가',
               '매도호가','전일거래량','자산총계','영업이익증가율','ROE','고가','매수총잔량',
               '외국인비율','부채총계','당기순이익','ROA','저가','매도총진량','상장주식수',
               '매출액','주당순이익','PBR','매출액증가율','보통주배당금','유보율']

print(select_list[0:])
print()
print("띄어쓰기로만 구분됩니다.")
selection = input("원하는 조회 학목을 입력하세요(최대 6개) : ")
selected_items = selection.split()

url = "https://finance.naver.com/sise/sise_market_sum.naver?&page="

options = Options()
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)

# 페이지 이동
driver.get(url)
driver.maximize_window()

# 조회 항목 초기화(체크되어 있는 항목 체크 해제)
checkboxes = driver.find_elements(By.NAME,'fieldIds')
for checkbox in checkboxes:
    if checkbox.is_selected(): # 체크된 상태라면
        checkbox.click() # 클릭(체크 해제)
time.sleep(1)

# 최대 6개까지만 선택
selected_items = selected_items[:6]

# select_list에 있는 항목만 선택
items_to_select = [item for item in selected_items if item in select_list]

for checkbox in checkboxes:
    parent = checkbox.find_element(By.XPATH, '..')  # 부모 element 찾기
    label = parent.find_element(By.TAG_NAME, 'label')
    if label.text in items_to_select:  # 선택항목과 일치하면
        checkbox.click()  # 클릭(선택)

time.sleep(1)

# 적용하기
btn_apply = driver.find_element(By.XPATH,'//*[@id="contentarea_left"]/div[2]/form/div/div/div/a[1]/img')
btn_apply.click()

for idx in range(1,50): #1 이상 50미만 페이지 반복
    # 페이지 이동
    driver.get(url + str(idx))
    time.sleep(0.5)
    # 데이터 추출
    df = pd.read_html(driver.page_source)[1]
    df.dropna(axis='index', how='all', inplace=True)
    df.dropna(axis='columns', how='all', inplace=True)
    if len(df) == 0: #더이상 가져올 파일이 없으면 브레이크
        break
    # 파일 저장
    f_name = 'sise.csv'
    if os.path.exists(f_name): #파일이 있다면 헤더 제외
        df.to_csv(f_name, encoding='utf-8-sig', index=False, mode='a', header=False)
    else: # 파일이 없다면 헤더 포함
        df.to_csv(f_name, encoding='utf-8-sig', index=False)
    print(f'{idx} 페이지 완료' )
    
driver.quit() #브라우저 종료