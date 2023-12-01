# 1961801 권강민 식당예약 크롤링
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# 예약 페이지 링크
url = "https://map.naver.com/p?c=15.00,0,0,0,dh"

# 아이디 비밀번호 아래에 입력
ID = input("네이버 아이디를 입력해주세요 : ")
PW = input("네이버 비밀번호를 입력해주세요 : ")

# 예약할 식당 이름과 인원수 입력
sikdang_Name = input("예약을 하고 싶은 식당 이름을 적어주세요(예약 서비스가 없는 식당은 예약이 안됩니다.) : ")
people = input("예약할 인원수를 적어주세요(최대 100명) : ")

# 예약할 날짜 입력
weekInput = input("예약할 주차를 입력해주세요 (1~6) : ")
days = ['일 - 1', '월 - 1', '화 - 3', '수 - 4', '목 - 5', '금 - 6', '토 - 7']
print(days[0:])
dayInput = input("예약할 요일을 숫자로 입력해주세요 : ")

# 예약 시간 입력
time_select = ['오전 - 1','오후 - 2']
print(time_select[0:])

am_pm = int(input("오전 오후중 예약할 시간대를 입력하세요(숫자로 입력하세요) : "))
if am_pm != 1 and am_pm != 2:
    print("시간을 잘못 입력하셨습니다. 다시 실행해 주세요")
    time.sleep(2)
    exit()
    
hour_select = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
print(hour_select[0:])

reserv_time_hour = int(input("예약할 시를 입력하세요(숫자만 입력하세요) : "))
if(reserv_time_hour < 1 and reserv_time_hour > 12):
    print("시간을 잘못 입력하셨습니다. 다시 실행해 주세요")
    time.sleep(2)
    exit()
    
minute_select = [00,30]
print(minute_select[0:])

reserv_time_minute = int(input("예약할 분을 골라주세요(숫자만 입력하세요) : "))
if(reserv_time_minute != 00 and reserv_time_minute != 30):
    print("시간을 잘못 입력하셨습니다. 다시 실행해 주세요")
    time.sleep(2)
    exit()

# 새로 바뀐 셀레니움 웹페이지 강제 종료 안당하는 코드
options = Options()
options.add_argument("--start-maximaized")
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)

# 동적 웹페이지에 이용할 드라이버 설정
wait = WebDriverWait(driver, 10)
act = ActionChains(driver)

# 링크를 가져옴
driver.get(url)

# iframe을 찾고 들어가기
def iframe_list():
    iframe_element = driver.find_element(By.ID, "searchIframe")  #iframe 엘리먼트 식별
    driver.switch_to.frame(iframe_element) # iframe 내부로 전환

def iframe_reservation():
    iframe_element = driver.find_element(By.ID, "entryIframe") # iframe 엘리먼트 식별
    driver.switch_to.frame(iframe_element) # iframe 내부로 전환
    
# 네이버 예약 로그인
def login():
    loginBtn = driver.find_element(By.CLASS_NAME, 'gnb_btn_login')
    act.click(loginBtn).perform()
    driver.find_element(By.ID, 'id').send_keys(ID) # 아이디 창에 위에 적은 아이디 입력
    driver.find_element(By.ID, 'pw').send_keys(PW) # 비밀번호 창에 위에 적은 비밀번호 입력
    loginEtr =  driver.find_element(By.XPATH, '//*[@id="log.login"]')
    act.click(loginEtr).perform()

# 입력한 식당을 검색
def search():
    Search = driver.find_element(By.CLASS_NAME, 'input_search')
    Search.send_keys(sikdang_Name)
    Search.send_keys(Keys.RETURN)
    time.sleep(2)

# 검색한 식당에 예약
def reservation():
    iframe_list()
    # 최상단의 식당 누르기
    reserv = driver.find_element(By.XPATH,'//*[@id="_pcmap_list_scroll_container"]/ul/li[1]/div[1]/a/div/div') 
    act.click(reserv).perform()
    time.sleep(2)
    driver.switch_to.default_content()
    
    # 식당 페이지의 예약버튼 누르기
    iframe_reservation()
    sik_reserv_btn = driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[2]/div[4]/div/span/a')
    act.click(sik_reserv_btn).perform()
    time.sleep(2)
    # 식당 예약 일정 클릭
    reserv_date = driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[6]/div[2]/div/div/div[2]/div/div/span/a')
    act.click(reserv_date).perform()
    time.sleep(2)
    # 예약 날짜 선택 요일 = td값 변경 // 주차 = tr값 변경 // 월 = div/div값 변경
    # 달력선택은 /div[Month]/table/tbody/tr[Week]/td[Day]
    day_select = driver.find_element(By.XPATH, '//*[@id="scroll_area"]/div[1]/div/div[2]/table/tbody/tr['+weekInput+']/td['+dayInput+']/a').click()
    time.sleep(2)
    
    # 예약 시간 선택 클릭
    total_minutes = reserv_time_hour * 60 + reserv_time_minute

    if am_pm == 1 and reserv_time_hour == 12 and reserv_time_minute == 0: #수정된 부분
        total_minutes = 30
        cnt += total_minutes // 30  # 수정된 부분
    elif am_pm == 1:
        cnt = total_minutes // 30 + 1
    elif am_pm == 2:
        total_minutes = (reserv_time_hour+12) * 60 + reserv_time_minute
        cnt = total_minutes // 30 + 1  # 수정된 부분
    str_cnt = str(cnt)
    reserv_time = driver.find_element(By.XPATH, '//*[@id="scroll_area"]/div[2]/div/div/div/div/div/span['+str_cnt+']/a')
    act.click(reserv_time).perform()
    time.sleep(2)
    
    # 예약 인원 결정
    reserv_people = driver.find_element(By.XPATH,'//*[@id="place_personnel_input"]')
    reserv_people.clear()
    reserv_people.send_keys(people)
    time.sleep(2)
    
    # 예약 클릭
    # 활성화 하면 예약
    # reservation_complete = driver.find_element(By.XPATH,'//*[@id="_place_portal_root"]/div/div[2]/div[2]/a[2]')
    # act.click(reservation_complete).perform()
    
def main():
    time.sleep(0.5)
    login()
    time.sleep(20)
    search() 
    time.sleep(2)
    reservation()
    
main()
time.sleep(1000)
