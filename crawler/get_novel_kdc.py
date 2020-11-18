import os
import json
import requests
import pandas as pd
from tqdm import tqdm
import numpy as np
from selenium import webdriver

driver = webdriver.Chrome('./chromedriver/chromedriver.exe')
url = 'https://www.nl.go.kr/nation/seoji/search.jsp'
driver.get(url)

fname = 'novel2'
novel = pd.read_pickle(f'./{fname}.pkl')

# isbn_list = temp["isbn"].values
temp_index = novel.index

for idx in tqdm(range(0, len(temp_index))):
    index = temp_index[idx]
    isbn = novel.loc[index]["isbn"]
    try:
        driver.find_element_by_name("isbn_code").send_keys(isbn)
        li = driver.find_element_by_class_name('fn')
        li.click()
        driver.implicitly_wait(1)

        selector = "#searchResultForm > div > div > div > div.itemTitle > a"
        driver.find_element_by_css_selector(selector).click()
        driver.implicitly_wait(1)

        selector2 = '//a[contains(text(), "한국십진")]'
        kdc = driver.find_element_by_xpath(selector2).text.split("->")[1].strip()
        kdc_split = kdc.split(".")
        kdc = kdc_split[0].zfill(3) + "." + kdc_split[1]

        novel.loc[index, "kdc_original"] = kdc

    except:
        pass
    finally:
        driver.find_element_by_name("isbn_code").clear()

driver.close()

n_data = novel[novel["kdc_original"].isna() == False]
data = n_data[n_data["kdc_original"].str.len() < 7]
pd.to_pickle(data, './novel_data2.pkl')

def book_dataframe_to_json_list(dataframe, desc=""):
    indexes = list(dataframe.index)
    columns = list(dataframe.columns)

    books = []
    for i in tqdm(range(0, len(indexes)), desc=desc):
        d = dataframe.loc[indexes[i]]
        # books_book 테이블에 도서정보가 있으면 패스
        f = {}
        # pk를 None 으로 하면, DB 에 저장될 때 알아서 primary key 가 부여된다.
        f["pk"] = None
        f["model"] = "books.book"
        f["fields"] = {}

        fi = f["fields"]

        for c in columns:
            fi[c] = d[c]
        
        books.append(f)
            
    return books
class npEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.int32):
            return int(obj)

        if isinstance(obj, np.int64):
            return int(obj)
        
        return json.JSONEncoder.default(self, obj)

def create_json_file(jsondata, url):
    with open(url, "w", encoding="utf-8") as f:
        json.dump(jsondata, f, cls=npEncoder)

backend_dir = "C:/Users/dogma/Desktop/Program/specialPJT/s03p23d103/backend/backend/"
backend_dir_json_fname = f'{backend_dir}{fname}_db.json'

jsondata = book_dataframe_to_json_list(data)
create_json_file(jsondata, backend_dir_json_fname)
create_json_file(jsondata, f'./{fname}_db.json')
print("insert data ...")
os.system(f"python {backend_dir}manage.py loaddata -v 3 {backend_dir_json_fname}")
print("Done!\n")
