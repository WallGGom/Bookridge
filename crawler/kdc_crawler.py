import json
import requests
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from crawler.connect_db import MysqlController
import re
# books = pd.read_pickle("books.pkl")
# books = books[
#     (books["isbn"].isna() == False) & (books["isbn_add"].isna() == False) 
#     & (books["title"].isna() == False) & (books["author"].isna() == False)
# ]

# books["kdc_original"] = None
# values = books["isbn"].values

# for i, book in tqdm(books.iterrows()):
#     isbn = book["isbn"]

# for idx in tqdm(range(0, len(values))):
    
#     isbn = values[idx]
#     # isbn = "9788958945116"
#     url = f"https://www.nl.go.kr/NL/contents/search.do?pageNum=1&pageSize=30&srchTarget=total&kwd={isbn}"

#     req = requests.get(url)

#     soup = BeautifulSoup(req.text, 'html.parser')
#     cont = soup.find("div", "section_cont_wrap")
#     try:
#         kdc_info = cont.find_all("span", "mr txt_grey")[-1].text
#         books.iloc[idx]["kdc_original"] = kdc_info.split(":")[-1].strip().split("-")[0]
#     except:
#         pass

db = MysqlController()
sql = "SELECT * FROM books_book WHERE kdc_original = ''"
rows = db.execute(sql)

driver = webdriver.Chrome('./chromedriver/chromedriver.exe')
driver.implicitly_wait(3)
url = 'https://www.nl.go.kr/nation/seoji/search.jsp'
driver.get(url)

# idx=1
len(rows)
for idx in tqdm(range(0, len(rows))):
    row = rows[idx]
    # url = f"https://www.nl.go.kr/NL/contents/search.do?pageNum=1&pageSize=30&srchTarget=total&kwd={row['isbn']}"
    try:
        driver.find_element_by_name("isbn_code").send_keys(row['isbn'])
        li = driver.find_element_by_class_name('fn')
        li.click()
        driver.implicitly_wait(1)

        selector = "#searchResultForm > div > div > div > div.itemTitle > a"
        driver.find_element_by_css_selector(selector).click()
        driver.implicitly_wait(1)
        # selector2 = '#contents_view > div.srchView > div.viewContents > dl:nth-child(5) > dd > a'
        selector2 = '//a[contains(text(), "한국십진")]'
        kdc = driver.find_element_by_xpath(selector2).text.split("->")[1].strip()
        kdc_split = kdc.split(".")
        kdc = kdc_split[0].zfill(3) + "." + kdc_split[1]

        update_sql = f"UPDATE books_book SET kdc_original = {kdc} WHERE id = {row['id']}"
        db.execute(update_sql)
        db.commit()
        # table_row.click()
        # cls_selector2 = "#divSeoji > div.more_info_wrap > p:nth-child(5) > a"
        # kdc_info = driver.find_element_by_css_selector(cls_selector2)
        # kdc_original = kdc_info.text

        # update_sql = f"UPDATE books_book SET kdc_original = {kdc_original} WHERE id = {row['id']}"
        # db.execute(update_sql)
        # db.commit()
    except:
        pass
    finally:
        driver.find_element_by_name("isbn_code").clear()
else:
    db.disconnect()
    driver.close()
