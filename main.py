#1752022 이해빈
import subprocess
import tkinter as tk
import os
##본인꺼 외에 건들지 마세요
# 영화 예매
def open_movie_reservation():
    subprocess.Popen(['python', 'moviedata.py'])

# 영화 평점
def open_rating_view():
   subprocess.Popen('python movieRating.py')

# KTX 예매
def open_ktx_reservation():
    subprocess.Popen(['python','traincrawling.py'])

# 네이버 쇼핑 특가 목록
def open_naver_shopping():
    pass

# 식당 예약
def open_restaurant_reservation():
    subprocess.Popen(['python', 'sikdang_reserve.py'])

# 주식 정보
def open_stock_info():
    subprocess.Popen(['python', 'zusik.py'])

# 쿠팡 및 쇼핑몰별 가격 비교
def open_price_comparison():
    subprocess.Popen(['python', 'CPangCR.py'])

root = tk.Tk()

movie_button = tk.Button(root, text="영화 예매", command=open_movie_reservation)
movie_button.pack()

rating_button = tk.Button(root, text="영화 평점", command=open_rating_view)
rating_button.pack()

ktx_button = tk.Button(root, text="KTX 예매", command=open_ktx_reservation)
ktx_button.pack()

naver_shopping_button = tk.Button(root, text="네이버 쇼핑 특가 목록", command=open_naver_shopping)
naver_shopping_button.pack()

restaurant_button = tk.Button(root, text="식당 예약", command=open_restaurant_reservation)
restaurant_button.pack()

stock_info_button = tk.Button(root, text="주식 정보", command=open_stock_info)
stock_info_button.pack()

price_comparison_button = tk.Button(root, text="쿠팡 가격 비교", command=open_price_comparison)
price_comparison_button.pack()

root.mainloop()
