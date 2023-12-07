#1751018 이우배
#일반승차권 예매 프로그램 작성
#열차종류는 전체로 검색
import time
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException
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
#출발지 도착지 목록
station_list = ["서울","용산","영등포","광명","수원","평택","천안아산","천안","오송","조치원","대전","서대전","김천","구미","김천구미","대구","동대구","포항","밀양","구포","부산","신경주","태화강","울산","마산","창원중앙","경산","논산","익산","정읍","광주송정","목포","전주","순천","여수","대천","청량리","춘천","제천","동해","강릉","행신","남춘천","부전","신탄진","영동","왜관","원주","정동진","홍성","행신","나주","정읍","남원"]

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
    depbox = ttk.Combobox(root)
    depbox.config(height=3)
    depbox.config(values=station_list)
    depbox.pack()
    # depart = Entry(root)
    # depart.pack()
    
    #도착
    arrival_label = Label(root, text="도착지")
    arrival_label.pack()
    arrbox = ttk.Combobox(root)
    arrbox.config(height=3)
    arrbox.config(values=station_list)
    arrbox.pack()
    # arrival = Entry(root)
    # arrival.pack()
    
    #년도
    year_label = Label(root, text="년도")
    year_label.pack()
    ybox = ttk.Combobox(root)
    ybox.config(height=3)
    ybox['values']=('2023','2024','2025')
    ybox.pack()
    # year = Entry(root)
    # year.pack()
    #2023,2024,2025
    
    #월
    month_label = Label(root, text="월")
    month_label.pack()
    mbox = ttk.Combobox(root)
    mbox.config(height=3)
    mbox['values']=('01','02','03','04','05','06','07','08','09','10','11','12')
    mbox.pack()
    #01~12
    
    #일
    day_label = Label(root, text="일")
    day_label.pack()
    dbox = ttk.Combobox(root)
    dbox.config(height=3)
    dbox['values']=('01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31')
    dbox.pack()
    #01~31
    
    #시간
    hour_label = Label(root, text="시간")
    hour_label.pack()
    hbox = ttk.Combobox(root)
    hbox.config(height=3)
    hbox['values']=('00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23')
    hbox.pack()
    #00~23시

    #성인
    adult_label = Label(root, text="성인")
    adult_label.pack()
    adbox = ttk.Combobox(root)
    adbox.config(height=3)
    adbox['values']=('0','1','2','3','4','5','6','7','8','9')
    adbox.pack()
    #인원을 0~9명까지 선택가능
    
    #만6세~12세
    kids_label = Label(root, text="어린이")
    kids_label.pack()
    kibox = ttk.Combobox(root)
    kibox.config(height=3)
    kibox['values']=('0','1','2','3','4','5','6','7','8','9')
    kibox.pack()
    #인원을 0~9까지 선택
    
    #만6세미만
    toddler_label = Label(root, text="유아")
    toddler_label.pack()
    tobox = ttk.Combobox(root)
    tobox.config(height=3)
    tobox['values']=('0','1','2','3','4','5','6','7','8','9')
    tobox.pack()
    #인원을 0~9까지 선택
    
    #만65세이상
    elder_label = Label(root, text="노약자")
    elder_label.pack()
    elbox = ttk.Combobox(root)
    elbox.config(height=3)
    elbox['values']=('0','1','2','3','4','5','6','7','8','9')
    elbox.pack()
    #인원을 0~9까지 선택
    
    #좌석종류
    seat_label = Label(root, text="좌석종류(000:기본,011:1인,012:창측,013:내측)")
    seat_label.pack()
    sebox = ttk.Combobox(root)
    sebox.config(height=3)
    sebox['values']=('000','011','012','013')
    sebox.pack()
    #000기본,011=1인석,012=창측,013=내측
        
    #좌석방향
    range_label = Label(root, text="좌석방향(000:기본,009:순방향,010:역방향)")
    range_label.pack()
    rabox = ttk.Combobox(root)
    rabox.config(height=3)
    rabox['values']=('000','009','010')
    rabox.pack()
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
        while True:
            try:
            # 예약 버튼 클릭
                reservation_button = driver.find_element(By.XPATH, '//*[@id="tableResult"]/tbody/tr[1]/td[6]/a/img')
                reservation_button.click()

            # 예약 알림창 확인
                WebDriverWait(driver, 5).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()

                time.sleep(2)  # 필요에 따라 대기 시간 조절

            # 루프에서 탈출
                break

            except TimeoutException:
            # 예약 버튼이 없는 경우
        
                WebDriverWait(driver, 5).until(EC.url_changes(driver.current_url))
                
                driver.refresh() #다시 조회
                
    #조회버튼 눌렀을시 입력할 내용
    def execute_button():
        departure = depbox.get()
        arri = arrbox.get()
        
        #출발입력받는 기능
        driver.find_element(By.ID,'start').clear()
        
        driver.find_element(By.ID,'start').send_keys(departure)
        
        #도착입력받는 기능
        driver.find_element(By.ID,'get').clear()
        
        driver.find_element(By.ID,'get').send_keys(arri)
        
        #기차조회 조건 설정
        Select(driver.find_element(By.ID,'s_year')).select_by_value(ybox.get())
        Select(driver.find_element(By.ID,'s_month')).select_by_value(mbox.get())
        Select(driver.find_element(By.ID,'s_day')).select_by_value (dbox.get())
        Select(driver.find_element(By.ID,'s_hour')).select_by_value(hbox.get())
        Select(driver.find_element(By.ID,'peop01')).select_by_value(adbox.get())
        Select(driver.find_element(By.ID,'peop02')).select_by_value(kibox.get())
        Select(driver.find_element(By.ID,'peop04')).select_by_value(tobox.get())
        Select(driver.find_element(By.ID,'peop03')).select_by_value(elbox.get())
        Select(driver.find_element(By.ID,'seat01')).select_by_value(sebox.get())
        Select(driver.find_element(By.ID,'seat02')).select_by_value(rabox.get())
        
        sebutton_set()
        
    def loop_button():
        lobutoon_set()
        
    #조회버튼
    execute_btn = Button(root, text="조회", command=execute_button)
    execute_btn.place(x=300,y=550)
    
    #예약실행버튼
    loop_btn = Button(root, text = "예약실행", command=loop_button)
    loop_btn.place(x=380,y=550)
    
    root.mainloop()
    
select_train()
