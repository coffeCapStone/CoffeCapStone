#1751018 이우배
#인스타그램 키워드 검색 엑셀파일로 저장 프로그램
import time
import re
from tkinter import *
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from datetime import datetime
from selenium.webdriver.chrome.options import Options
from tkinter import simpledialog
from selenium.webdriver.support.select import Select

#크롬이 꺼지지 않는 옵션
chorme_options = Options()
chorme_options.add_experimental_option("detach",True)

#검색어 조건에 따른 url 생성
def insta_search(word):
    url = "https://www.instagram.com/explore/tags/" + str(word)
    return url

#검색 결과 첫번째 게시물을 클릭하여 가져오기
def select_first():
    first = driver.find_elements(By.CSS_SELECTOR,"div._aagw")[0]
    first.click()
    time.sleep(3)
    
#본문,작성일자,좋아요 수, 위치정보, 해시태그 가져오기
def get_content():
    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')
    #본문
    try:
        content = soup.select('div.a9zs')[0].text
    except:
        content = ''
        
    #해쉬태그
    tags = re.findall(r'#[^\s#,\\]+',content)
    
    #일자
    date = soup.select('time._aaqe')['datetime'][:10]
    
    #종아요
    try:
        like = soup.select('div._aacl._aaco._aacw._aacx._aada._aade')[0].findAll('span')[-1].text
    except:
        like = 0
    
    #위치
    try:
        place = soup.select('div._aaqm')[0].text
    except:
        place = ''
    
    data = [content,date,like,place,tags]
    return data

#첫번째 게시물 클릭후 다음게시물 클릭
def move_next():
    right = driver.find_element(By.CSS_SELECTOR,"div._aaqg._aaqh")
    right.click()
    time.sleep(3)

#여기부터 크롤링
#크롬브라우저
driver = webdriver.Chrome(options=chorme_options)

driver.get('https://www.instagram.com')
time.sleep(3)

#인스타그램 로그인 정보
root = Tk()
root.withdraw()

email = simpledialog.askstring(title="ID",prompt="아이디를 입력하세요",parent=root)
input_id = driver.find_elements(By.CSS_SELECTOR,'#loginForm > div > div:nth-child(1) > div > label > input')[0]
input_id.clear()
input_id.send_keys(email)

password = simpledialog.askstring(title="PW",prompt="비밀번호를 입력하세요",show="*",parent=root)
input_pw = driver.find_elements(By.CSS_SELECTOR,'#loginForm > div > div:nth-child(2) > div > label > input')[0]
input_pw.clear()
input_pw.send_keys(password)
input_pw.submit()

time.sleep(5)

#게시물을 조회할 검색 키워드 입력
word = input("검색어를 입력하세요 : ")
word = str(word)
url = insta_search(word)

#검색결과 페이지 
driver.get(url)
time.sleep(10)

#첫번째 게시물 클릭
select_first()

results = []

target = 10
for i in range(target):
    try:
        data = get_content()
        results.append(data)
        move_next()
    except:
        time.sleep(2)
        move_next()
    time.sleep(5)

print(results[:2])

#검색결과 엑셀파일로 저장
date = datetime.today().strftime('%Y-%m-%d')

result_df = pd.DataFrame(results, columns = ['content','date','like','place','tags'])
result_df.to_excel(date + '_about '+word+' insta crawling.xlsx')

