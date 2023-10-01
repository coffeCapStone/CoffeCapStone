##1752022이해빈
import tkinter as tk
from tkinter import ttk, messagebox
from selenium.webdriver.common.by import By
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time


# 로그인 및 예매 
def book_ticket():
    userid = id_var.get()
    password = password_var.get()
    

    driver = webdriver.Chrome()
    driver.get("https://www.lottecinema.co.kr/NLCHS/Member/login")
    button = driver.find_element(By.XPATH, '//*[@id="footer_section"]/div[3]/button')
    button.click()
    time.sleep(2)  # 로딩 시간
    
    # 아이디와 비밀번호 입력 후 로그인
    driver.find_element(By.ID, 'userId').send_keys(userid)
    driver.find_element(By.ID, 'userPassword').send_keys(password)
    driver.find_element(By.CLASS_NAME, "btn_login").click()
 
    time.sleep(4)  
    
    # 영화 예매 페이지로 이동
    driver.get("https://www.lottecinema.co.kr/NLCHS/Ticketing/Schedule")
    movie_button = driver.find_element(By.XPATH, "/html/body/div[6]/div/ul/li[2]/button")
    movie_button.click()
    time.sleep(4)  
    
    try:
        # 영화 선택
        selected_movie = movie_var.get()
        print(f"Selected Movie: {selected_movie}")
        
        movie_xpath = f"//strong[@class='tit' and text()='{selected_movie}']"
        movie_element = driver.find_element(By.XPATH, movie_xpath)
        movie_element.click()
        print(f"Movie {selected_movie} selected.")
        time.sleep(2)
        
        # 영화관 선택
        selected_theater = theater_var.get()
        print(f"Selected Theater: {selected_theater}")
        
        theater_elements = driver.find_elements(By.XPATH, "//strong[@class='tit']")
        theater_found = False
        
        for theater_element in theater_elements:
            if selected_theater in theater_element.text:
                theater_element.click()
                theater_found = True
                print(f"Theater {selected_theater} selected.")
                time.sleep(2)
                break
        
        if not theater_found:
            print(f"Theater {selected_theater} not found.")
            return
        
           # 상영 시간 선택 부분 업데이트
        selected_time = time_var.get()
        print(f"Selected Time: {selected_time}")

        time_xpath = f"//dd[@class='time']/strong[text()='{selected_time}']"
        wait = WebDriverWait(driver, 10)  
        time_element = wait.until(EC.presence_of_element_located((By.XPATH, time_xpath)))
        time_elements = driver.find_elements(By.XPATH, time_xpath)
        actions = ActionChains(driver)
        actions.double_click(time_element).perform()
        print(f"Time {selected_time} double-clicked.")
        time_found = False

        for time_element in time_elements:
                    if time_element.text == selected_time:
                        time_element.click()
                        time_found = True
                        print(f"Time {selected_time} selected.")
                        

        if not time_found:
                    print(f"Time {selected_time} not found.")
                    return
        


        
        # 팝업 창의 요소를 대기하고 선택
        popup_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#layerReserveStep01"))
        )

        # "인원/좌석 선택" 링크 요소를 선택
        seat_selection_link = popup_element.find_element(By.XPATH, '//a[@class="btn_col1 ty5" and text()="인원/좌석 선택"]')

        # 클릭
        seat_selection_link.click()



        #좌석결제까지
        selected_row = row_var.get()
        selected_seat = seat_var.get()
        selected_seat_number = f"{selected_row}{selected_seat}"

        # 티켓수
        plus_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'Plus|10'))
        )
        plus_button.click()

        # 선택한 좌석 지정.
        seat_selector = f'a[data-seat="{selected_seat_number}"]'
        user_selected_seat = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, seat_selector))
        )
        user_selected_seat.click()

        print(f"Seat {selected_seat_number} selected.")
         # 첫번째 결제 버튼 찾기
        payment_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'link_rpay'))
        )
        payment_button.click()

        print("Proceeding to payment.")

        # 간편결제 버튼 찾기
        easy_payment_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.cate3.active'))
        )
        easy_payment_button.click()

        # 네이버페이
        naverpay_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="네이버페이"]'))
        )
        naverpay_button.click()

        # 최종결제
        final_payment_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.btn_col1.btn_confirm'))
        )
        final_payment_button.click()

        # 쓸떄없는 팝업 엔터로 제거
        actions = ActionChains(driver)
        actions.send_keys(Keys.ENTER).perform()

        print("Payment completed.")

    except Exception as e:
        print(f"An error occurred: {e}")









# 로그인 함수
def login():
    userid = id_var.get()
    password = password_var.get()
    print(f"ID: {userid}")
    print(f"Password: {password}")
    messagebox.showinfo("Login info", f"Logged in with {userid}")

# 영화 및 상영 시간 업데이트 함수
def update_times(*args):
    selected_movie = movie_var.get()
    selected_theater = theater_var.get()
    filtered_df = df[(df['영화 제목'] == selected_movie) & (df['영화관'] == selected_theater)]
    times = filtered_df['상영 시간'].unique().tolist()
    time_var.set('')
    time_dropdown['values'] = times

# 영화 정보를 포함한 엑셀 파일 로드
df = pd.read_excel('movie.xlsx')

# 영화 제목과 영화관 정보 추출
movies = df['영화 제목'].unique().tolist()
theaters = df['영화관'].unique().tolist()

# 좌석 정보
rows = ['A', 'B', 'C', 'D', 'E']
seats = list(range(1, 12))

# Tkinter GUI 생성
root = tk.Tk()
root.title('영화예매 프로그램')

# 아이디 입력 칸
tk.Label(root, text="아이디:").grid(row=0, column=0, sticky=tk.W)
id_var = tk.StringVar()
id_entry = tk.Entry(root, textvariable=id_var)
id_entry.grid(row=0, column=1)

# 비밀번호 입력 칸
tk.Label(root, text="비밀번호:").grid(row=1, column=0, sticky=tk.W)
password_var = tk.StringVar()
password_entry = tk.Entry(root, textvariable=password_var, show="*") 
password_entry.grid(row=1, column=1)

# 영화 선택 드롭다운
tk.Label(root, text="영화 제목").grid(row=2, column=0)
movie_var = tk.StringVar()
movie_var.trace_add('write', update_times)
movie_dropdown = ttk.Combobox(root, textvariable=movie_var, values=movies)
movie_dropdown.grid(row=2, column=1)

# 영화관 선택 드롭다운
tk.Label(root, text="영화관").grid(row=3, column=0)
theater_var = tk.StringVar()
theater_var.trace_add('write', update_times)
theater_dropdown = ttk.Combobox(root, textvariable=theater_var, values=theaters)
theater_dropdown.grid(row=3, column=1)

# 상영 시간 선택 드롭다운
tk.Label(root, text="상영시간").grid(row=4, column=0)
time_var = tk.StringVar()
time_dropdown = ttk.Combobox(root, textvariable=time_var)
time_dropdown.grid(row=4, column=1)

# 좌석 행 선택 드롭다운
tk.Label(root, text="좌석번호(영어)").grid(row=5, column=0)
row_var = tk.StringVar()
row_dropdown = ttk.Combobox(root, textvariable=row_var, values=rows)
row_dropdown.grid(row=5, column=1)

# 좌석 번호 선택 드롭다운
tk.Label(root, text="좌석번호").grid(row=6, column=0)
seat_var = tk.StringVar()
seat_dropdown = ttk.Combobox(root, textvariable=seat_var, values=seats)
seat_dropdown.grid(row=6, column=1)

# 예매 시작버튼
book_button = tk.Button(root, text="좌석 예매하기", command=book_ticket)
book_button.grid(row=7, column=0, columnspan=2, pady=10)

# Tkinter 메인 이벤트 루프 실행
root.mainloop()