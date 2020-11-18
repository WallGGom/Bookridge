import requests
import xmltodict
import math
import pandas as pd
import crawler.info as info

libSrchUrl = info.library_info["requestUrl"]
res = requests.get(libSrchUrl)
data = xmltodict.parse(res.text)
data = data["response"]
# 검색조건으로 가지고 온 데이터가 pageSize 보다 큰지 확인
cond = int(data["numFound"]) / int(data["pageSize"])
# pageNo 1 에서 가지고 온 데이터
records = [d for d in data["libs"]["lib"]]

if 1 < cond:
    for idx in range(2, math.ceil(cond) + 1):
        resquest_url = libSrchUrl + f"&pageNo={idx}"
        tmp = requests.get(resquest_url)
        tmp_data = xmltodict.parse(tmp.text)
        tmp_data = tmp_data["response"]
        temp = [d for d in tmp_data["libs"]["lib"]]
        records.extend(temp)

# 가지고 온 참여 도서관 정도 dataframe 으로 변경
dfItem = pd.DataFrame.from_records(records)
print(dfItem.columns)

# BookCount -> bookCount 로 변경하기
dfItem = dfItem.rename(columns={"BookCount": "bookCount"})
print(dfItem.columns)

# pickle data로 변경하기
pd.to_pickle(dfItem, './data/librarys.pkl')
