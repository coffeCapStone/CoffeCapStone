import tkinter as tk
from tkinter import scrolledtext
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

def crawl_data():
    driver = webdriver.Chrome()
    url = "https://movie.daum.net/ranking/reservation"
    driver.get(url)
    time.sleep(2)

    data = []
    movie_count = len(driver.find_elements(By.CSS_SELECTOR, "strong.tit_item"))

    for index in range(movie_count):
        movie = driver.find_elements(By.CSS_SELECTOR, "strong.tit_item")[index]
        rating = driver.find_elements(By.CSS_SELECTOR, "span.txt_grade")[index]

        title = movie.text.strip()
        score = rating.text.strip()
        link = movie.find_element(By.TAG_NAME, 'a').get_attribute('href').replace('main', 'grade')

        movie_data = {'Title': title, 'Score': score, 'Link': link, 'Comments': []}
        driver.get(link)
        time.sleep(2)

        comments = driver.find_elements(By.CSS_SELECTOR, "p.desc_txt")
        if comments:
            for i, comment in enumerate(comments):
                if i < 10:
                    movie_data['Comments'].append(comment.text.strip())
                else:
                    break

        data.append(movie_data)
        
        movie_info = f"영화 제목: {title}\n평점: {score}\n링크: {link}\n"
        output.insert(tk.END, movie_info)

        for i, comment in enumerate(movie_data['Comments']):
            output.insert(tk.END, f"댓글 {i+1}: {comment}\n")

        output.insert(tk.END, "-"*50 + "\n")
        output.yview(tk.END)

        driver.get(url)
        time.sleep(2)

    driver.quit()

    df = pd.DataFrame(data)
    df.to_excel('movie_Rating.xlsx', index=False)

# GUI
root = tk.Tk()
root.title("영화 평점 및 리뷰")

def start_crawling():
    output.insert(tk.END, "크롤링 시작\n")
    threading.Thread(target=crawl_data).start()

output = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=75, height=30)
output.grid(column=0, row=0, columnspan=2)

start_button = tk.Button(root, text="크롤링 시작", command=start_crawling)
start_button.grid(column=0, row=1)

exit_button = tk.Button(root, text="종료", command=root.destroy)
exit_button.grid(column=1, row=1)

root.mainloop()
