#일반승차권 예매 프로그램 작성
#열차종류는 전체로 검색
#실행버튼을 누르기 전 tkinter창에서 잘못 입력해도 오류가 발생하지 않도록 아에 바를 만들어서 선택을 할 수 있게 tkinter에 조건이랑 GUI 추가하자
import time
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    
    def sebutton_set():
     # 조회버튼 클릭 코드 실행
        driver.find_element(By.XPATH,'//*[@id="center"]/form/div/p/a/img').click()
        time.sleep(1)
        for handle in driver.window_handles[1:]:
            driver.switch_to.window(handle)
            driver.close()
    
    #예약실행 버튼 클릭 코드 실행
    def lobutoon_set():
        unavaiable_seat= None
        while True:
            if unavaiable_seat == "예약하기":
                driver.find_element(By.XPATH,'//*[@id="tableResult"]/tbody/tr[1]/td[6]/a/img').click()
                time.sleep(3)
                break
            else:
                #여기 오류 발생
                #만약 매진으로 표시가 되어 표가 없으면 다시 조회하기 버튼을 누르고 다시 예매하기 버튼을 계속 다음창 넘어갈때까지 하고 싶은데 이걸 어떻게 해야할까
                driver.find_element(By.CSS_SELECTOR,'#tableResult > tbody > tr:nth-child(1) > td:nth-child(6) > img').get_attribute("alt")
                time.sleep(2)
                
                driver.find_element(By.XPATH,'//*[@id="center"]/div[3]/p/a/img').click()
                time.sleep(2)
                
        
    #조회버튼 눌렀을시 실행할 기능
    def execute_button():
        departure = depart.get()
        arri = arrival.get()
        
        #출발입력받는 기능
        driver.find_element(By.ID,'start').clear()
        
        driver.find_element(By.ID,'start').send_keys(departure)
        
        #도착입력받는 기능
        driver.find_element(By.ID,'get').clear()
        
        driver.find_element(By.ID,'get').send_keys(arri)
        
        #기차조회 조건 설정
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
        
        sebutton_set()
        
    #예약실행 버튼 눌렀을때 실행할 기능
    def loop_butoon():
        
        lobutoon_set()
    
    #조회버튼
    execute_btn = Button(root, text="조회", command=execute_button)
    execute_btn.place(x=300,y=550)
    #예약실행버튼
    loop_btn = Button(root, text = "예약실행", command=loop_butoon)
    loop_btn.place(x=380,y=550)
    
    root.mainloop()
    
select_train()
            
