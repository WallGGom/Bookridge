# KAKAO_API 사용
# https://developers.kakao.com/docs/latest/ko/daum-search/dev-guide
import requests
import pandas as pd
import crawler.info as info

publishers = pd.read_pickle("./data/publisher.pkl")
kakao_url = info.kakao_book["requestUrl"]
headers = info.kakao_book["headers"]
publishers = publishers.values.tolist()

records = []
for pub in publishers:
    
    page = 1
    is_end = False
    req = requests.get(kakao_url + pub + "&page=" + str(page), headers=headers).json()
    records.extend(req["documents"])
    is_end = req["meta"]["is_end"]

    while not is_end:
        page += 1
        req = requests.get(kakao_url + pub + "&page=" + str(page), headers=headers).json()
        records.extend(req["documents"])
        is_end = req["meta"]["is_end"]
