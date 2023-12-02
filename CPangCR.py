#1961053 전성욱
import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import re
import webbrowser

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
}

def get_product_info(url, search_keyword, sort_by):
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    items = soup.find_all("li", attrs={"class": re.compile("^search-product")})

    results = []
    for item in items:
        ad_badge = item.find("span", attrs={"class": "ad-badge-text"})
        if ad_badge:
            continue

        name = item.find("div", attrs={"class": "name"}).get_text()
        if "Apple" in name:
            continue

        if search_keyword and search_keyword not in name:
            continue

        price_elem = item.find("strong", attrs={"class": "price-value"})
        if price_elem:
            price = price_elem.get_text()
        else:
            continue

        rate = item.find("em", attrs={"class": "rating"})
        if rate:
            rate = rate.get_text()
        else:
            continue

        rate_cnt = item.find("span", attrs={"class": "rating-total-count"})
        if rate_cnt:
            rate_cnt = rate_cnt.get_text()[1:-1]
        else:
            continue

        link = item.find("a", attrs={"class": "search-product-link"})["href"]

        if float(rate) >= 4.5 and int(rate_cnt) >= 100:
            result = {
                "제품명": name,
                "가격": price,
                "평점": f"{rate}점 ({rate_cnt}개)",
                "바로가기": "https://www.coupang.com/" + link
            }
            results.append(result)

    # 가격을 오름차순 또는 내림차순으로 정렬
    if sort_by == "오름차순":
        results = sorted(results, key=lambda x: float(x["가격"].replace(",", "").replace("원", "")))
    elif sort_by == "내림차순":
        results = sorted(results, key=lambda x: float(x["가격"].replace(",", "").replace("원", "")), reverse=True)

    return results

def search():
    search_keyword = entry.get()
    sort_by = sort_combobox.get()

    url = f"https://www.coupang.com/np/search?q={search_keyword}&channel=user&component=&eventCategory=SRP&trcid=&traid=&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType=&listSize=36&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page=1&rocketAll=false&searchIndexingToken=1=6&backgroundColor="

    results = get_product_info(url, search_keyword, sort_by)

    tree.delete(*tree.get_children())

    for result in results:
        name = result["제품명"]
        price = result["가격"]
        rate = result["평점"]
        link = result["바로가기"]

        tree.insert("", tk.END, text="", values=(name, price, rate, link))

def open_link(event):
    item = tree.selection()[0]
    link = tree.item(item, "values")[3]
    webbrowser.open(link)

# GUI 설정
root = tk.Tk()
root.title("제품 검색")
root.geometry("800x600")

# 검색 입력창
entry = tk.Entry(root, font=("Arial", 14))
entry.pack(pady=10)

# 정렬 옵션 콤보박스
sort_combobox = ttk.Combobox(root, values=["가격", "오름차순", "내림차순"], state="readonly", font=("Arial", 14))
sort_combobox.current(0)
sort_combobox.pack(pady=10)

# 검색 버튼
search_button = tk.Button(root, text="검색", command=search, font=("Arial", 14))
search_button.pack(pady=10)

# 검색 결과 표시할 트리뷰
tree = ttk.Treeview(root, columns=("제품명", "가격", "평점", "바로가기"), show="headings")
tree.column("제품명", width=300)
tree.column("가격", width=100)
tree.column("평점", width=100)
tree.column("바로가기", width=200)
tree.heading("제품명", text="제품명")
tree.heading("가격", text="가격")
tree.heading("평점", text="평점")
tree.heading("바로가기", text="바로가기")
tree.pack()

tree.bind("<Double-1>", open_link)

root.mainloop()