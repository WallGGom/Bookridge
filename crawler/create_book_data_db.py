import os
import re
import json
import pandas as pd
import numpy as np
from tqdm import tqdm

from crawler.connect_db import MysqlController
from selenium import webdriver

with open("./data/isbn_pk_info.json", "r", encoding="utf-8") as f:
    isbn_pk_info = json.load(f)

with open("./data/kdc_pk_info.json", "r", encoding="utf-8") as f:
    kdc_pk_info = json.load(f)

def nan_to_none(dataframe):
    """
    np.nan 타입을 None 으로 변경해줌
    """
    return dataframe.where(pd.notnull(dataframe), None)

def set_isbn_add1_pk(isbn_add):
    
    if isbn_add:
        if len(isbn_add) == 4:
            return 1
        elif len(isbn_add) == 5:
            return isbn_pk_info["isbn_add1"][isbn_add[0]]
        else:
            return None
    else:
        return None

def set_isbn_add2_pk(isbn_add):

    if isbn_add:
        if len(isbn_add) == 4:
            return isbn_pk_info["isbn_add2"][isbn_add[0]]
        elif len(isbn_add) == 5:
            return isbn_pk_info["isbn_add2"][isbn_add[1]]
        else:
            return None
    else:
        return None

def set_isbn_add3_pk(isbn_add):

    if isbn_add:
        if len(isbn_add) == 4:
            return isbn_pk_info["isbn_add3"][isbn_add[1:3]]
        elif len(isbn_add) == 5:
            return isbn_pk_info["isbn_add3"][isbn_add[2:4]]
        else:
            return None
    else:
        return None

def set_kdc_type(kdc):
    if kdc:
        # kdc pk 값을 리턴하기
        key = str(int(float(kdc))).zfill(3)
        return kdc_pk_info[key]
    return kdc

def organize_book_columns(dataframe):
    cols = [
        "title", "author", "publisher", "vol", "pub_date", "isbn",
        "price", "img_url", "description", "isbn_add"
    ]
    new_df = dataframe.loc[:, cols]

    new_df["isbn_add1"] = new_df["isbn_add"].apply(set_isbn_add1_pk)
    new_df["isbn_add2"] = new_df["isbn_add"].apply(set_isbn_add2_pk)
    new_df["isbn_add3"] = new_df["isbn_add"].apply(set_isbn_add3_pk)

    new_df = new_df.rename(columns={"isbn_add": "isbn_add_original"})
    
    return nan_to_none(new_df)

def select_novel_dataframe(row):
    novels = ["1", "2", "3", "4"]
    if row["isbn_add_original"][2] == "8":
        if row["isbn_add_original"][3] in novels:
            return True
    return False

db = MysqlController()
db_books = pd.DataFrame(db.execute("SELECT * FROM books_book"))

books_url = './data/books.pkl'

books = pd.read_pickle(books_url)

cond1 = (books["isbn"].isna() == False)
cond2 = (books["title"].isna() == False)
cond3 = (books["author"].isna() == False)
cond4 = (books["isbn_add"].isna() == False)
cond5 = (books["isbn"].isin(db_books["isbn"].values) == False)  # 이미 db에 들어간 책은 제외하자
cond = (cond1) & (cond2) & (cond3) & (cond4) & (cond5)

books = books[cond]

books = books[books["isbn_add"].str.len() < 6]
books = books[books["isbn_add"].str.isnumeric()]
books = books[(books["isbn_add"].str.len() == 5) | (books["isbn_add"].str.len() == 4)]
books["isbn_add"] = books["isbn_add"].apply(lambda x: "0"+x if len(x) < 5 else x)

df = organize_book_columns(books)

filtering = df.apply(select_novel_dataframe, axis=1)

new_df = df[filtering]

new_df["kdc_original"] = None

pd.to_pickle(new_df.iloc[:50000], './novel1.pkl')
pd.to_pickle(new_df.iloc[50000:100000], './novel2.pkl')
pd.to_pickle(new_df.iloc[100000:150000], './novel3.pkl')
pd.to_pickle(new_df.iloc[150000:200000], './novel4.pkl')
pd.to_pickle(new_df.iloc[200000:350000], './novel5.pkl')
pd.to_pickle(new_df.iloc[350000:400000], './novel6.pkl')