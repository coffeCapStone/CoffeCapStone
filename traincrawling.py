#1751018 이우배
#일반승차권 예매 프로그램 작성
#열차종류는 전체로 검색
import time
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoAlertPresentException,NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chorme_options = Options()
chorme_options.add_experimental_option("detach",True)

driver = webdriver.Chrome(options=chorme_options) #화면이 꺼지지 않는 옵션 추가 + webdriver 파일의 경로 추가

#로그인설정
def ask_login():
    driver.get('https://www.letskorail.com/korail/com/login.do')
    driver.implicitly_wait(15)
    
    root = Tk()
    root.withdraw()
    
    mem_num = simpledialog.askstring(title="ID",prompt="멤버쉽번호를 입력하세요",parent=root)
    
    driver.find_element(By.ID, 'txtMember').send_keys(mem_num)

    pwd = simpledialog.askstring(title="PW",prompt="비밀번호를 입력하세요",show="*",parent=root)
    
    driver.find_element(By.ID, 'txtPwd').send_keys(pwd)
    
    driver.implicitly_wait(15)
    
    driver.find_element(By.XPATH,'//*[@id="loginDisplay1"]/ul/li[3]/a/img').click()
    
    try:
        alert = Alert(driver)
        alert.accept()
        raise NoSuchElementException
    except NoAlertPresentException:
        driver.get('https://www.letskorail.com/ebizprd/EbizPrdTicketpr21100W_pr21110.do')
        driver.implicitly_wait(15)
    except NoSuchElementException:
        mem_num, pwd = ask_login()
    return mem_num, pwd

#시작할때 login물어보기
mem_num,pwd = ask_login()

#기차표 예매 GUI생성
def select_train():
    root = Tk()
    root.title("기차표 예매")
    root.geometry("740x600")

    #입력 필드 생성
    #출발
    depart_label = Label(root, text="출발지")
    depart_label.pack()
    depart = Entry(root)
    depart.pack()
    
    #도착
    arrival_label = Label(root, text="도착지")
    arrival_label.pack()
    arrival = Entry(root)
    arrival.pack()
    
    #년도
    year_label = Label(root, text="년도")
    year_label.pack()
    year = Entry(root)
    year.pack()
    #2023,2024,2025
    
    #월
    month_label = Label(root, text="월")
    month_label.pack()
    month = Entry(root)
    month.pack()
    #01~12
    
    #일
    day_label = Label(root, text="일")
    day_label.pack()
    day = Entry(root)
    day.pack()
    #01~31
    
    #시간
    hour_label = Label(root, text="시간")
    hour_label.pack()
    hour = Entry(root)
    hour.pack()
    #00~23시

    #성인
    adult_label = Label(root, text="성인")
    adult_label.pack()
    adult= Entry(root)
    adult.pack()
    #인원을 0~9명까지 선택가능
    
    #만6세~12세
    kids_label = Label(root, text="어린이")
    kids_label.pack()
    kids = Entry(root)
    kids.pack()
    #인원을 0~9까지 선택
    
    #만6세미만
    toddler_label = Label(root, text="유아")
    toddler_label.pack()
    toddler = Entry(root)
    toddler.pack()
    #인원을 0~9까지 선택
    
    #만65세이상
    elder_label = Label(root, text="노약자")
    elder_label.pack()
    elder = Entry(root)
    elder.pack()
    #인원을 0~9까지 선택
    
    #좌석종류
    seat_label = Label(root, text="좌석종류")
    seat_label.pack()
    seat = Entry(root)
    seat.pack()
    #000기본,011=1인석,012=창측,013=내측
        
    #좌석방향
    range_label = Label(root, text="좌석방향")
    range_label.pack()
    range = Entry(root)
    range.pack()
    #000=기본,009=순방향,010=역방향
    
    def button_set():
     # 버튼 클릭 코드 실행
        driver.find_element(By.XPATH,'//*[@id="center"]/form/div/p/a/img').click()
        
    #버튼 눌렀을시 실행할 기능
    def execute_button():
        departure = depart.get()
        arri = arrival.get()
        
        #출발입력받는 기능
        driver.find_element(By.ID,'start').clear()
        
        driver.find_element(By.ID,'start').send_keys(departure)
        
        #도착입력받는 기능
        driver.find_element(By.ID,'get').clear()
        
        driver.find_element(By.ID,'get').send_keys(arri)
        
        Select(driver.find_element(By.ID,'s_year')).select_by_value(year.get())
        Select(driver.find_element(By.ID,'s_month')).select_by_value(month.get())
        Select(driver.find_element(By.ID,'s_day')).select_by_value (day.get())
        Select(driver.find_element(By.ID,'s_hour')).select_by_value(hour.get())
        Select(driver.find_element(By.ID,'peop01')).select_by_value(adult.get())
        Select(driver.find_element(By.ID,'peop02')).select_by_value(kids.get())
        Select(driver.find_element(By.ID,'peop04')).select_by_value(toddler.get())
        Select(driver.find_element(By.ID,'peop03')).select_by_value(elder.get())
        Select(driver.find_element(By.ID,'seat01')).select_by_value(seat.get())
        Select(driver.find_element(By.ID,'seat02')).select_by_value(range.get())
        
        button_set()
        
    execute_btn = Button(root, text="실행", command=execute_button)
    execute_btn.pack(side=BOTTOM)
    
    root.mainloop()
    
select_train()

train_list = driver.find_element(By.CSS_SELECTOR, '#tableResult > tbody')
print(len(train_list))

for i in range(1,len(train_list)+1):
    for j in range(3,8):
        text = driver.find_element(By.CSS_SELECTOR,'#tableResult > tbody > tr:nth-child({i}) > td:nth-child({j})').text.replace("\n","")
        print(text,end="")
    print()
    
    #tableResult > tbody > tr:nth-child(1) > td:nth-child(3)
    #tableResult > tbody > tr:nth-child(1) > td:nth-child(4)
    #tableResult > tbody > tr:nth-child(1) > td:nth-child(1)

#여기부터 기차 자동예매 시스템 구축(도저히 모르겠다)*(일반석만 할꺼고 안되면 다시 조회버튼 누르고 예매 버튼 확인을 반복시키다가 다음 예매 창으로 넘어가면 break, 아니면 계속 무한 반복되는 프로그램)

#res = False
    
#while True:
    #for i in range(1,9):
        #standard_seat = driver.find_element(By.CSS_SELECTOR,'#tableResult > tbody > tr:nth-child({i}) > td:nth-child(6))').text
            
        #if "예약하기" in standard_seat:
            #driver.find_element(By.XPATH,'//*[@id="tableResult"]/tbody/tr[{i}]/td[6]/a[1]/img').click()
            #res = True
            #break
        
    #if not res:
        #time.sleep(4)
            
        #submit = driver.find_element(By.XPATH,'//*[@id="center"]/form/div/p/a/img')
        #driver.execute_script("arguments[0].click();",submit)
        #driver.implicitly_wait(15)
        #time.sleep(2)
    #else:
        #break
            
