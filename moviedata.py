##1752022이해빈
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd  

# 웹 드라이버 설정
driver = webdriver.Chrome()
driver.get("https://www.lottecinema.co.kr/NLCHS/Ticketing/Schedule")
button = driver.find_element(By.XPATH, '//*[@id="footer_section"]/div[3]/button')
time.sleep(5)  

movie_button = driver.find_element(By.XPATH, "/html/body/div[6]/div/ul/li[2]/button")
movie_button.click()
time.sleep(4)  

movies = driver.find_elements(By.CSS_SELECTOR, "strong.tit")

data = []

for movie in movies[:13]:  
    movie_title = movie.text
    if movie_title:  
        movie.click()  
        time.sleep(2)  

        html = driver.page_source  
        soup = BeautifulSoup(html, 'html.parser')
        theaters_info = soup.find_all('div', class_='time_select_wrap timeSelect')

        for theater_info in theaters_info:
            theater_name = theater_info.find_previous('strong', class_='tit').text
            times = theater_info.find_all('dl')

            for t in times:  
                screening_time = t.find('strong').text
                seats = t.find('dd', class_='seat').find('strong').text
                
                # 데이터 리스트추가
                data.append([movie_title, theater_name, screening_time, seats])

        movie_button = driver.find_element(By.XPATH, "/html/body/div[6]/div/ul/li[2]/button")
        movie_button.click()
        time.sleep(2)


driver.quit()

# 데이터를 DataFrame으로 변환
df = pd.DataFrame(data, columns=["영화 제목", "영화관", "상영 시간", "잔여석"])

# 엑셀 저장
df.to_excel("movie.xlsx", index=False, engine='openpyxl')

#저장 다 끝나면 예매 프로그램 실행
import subprocess
subprocess.run(["python", "movieAuto.py"])