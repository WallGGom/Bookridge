import pandas as pd

df = pd.read_excel("./data/publisher.xlsx")
publishers = df["사업장명"]
# 출판사 명 저장하기
pd.to_pickle(publishers, "./data/publisher.pkl")