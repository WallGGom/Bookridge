# python manage.py loaddata 를 해주기 위해서
# 형식에 맞는 json 을 생성해줌.

import pandas as pd
import json
from pprint import pprint
import numpy as np
df = pd.read_pickle('./data/books.pkl')
df.head()
df['pub_date']
df.isna().sum(axis = 0)

df # 3178417
df = df[(df['seq'].notna() & df['isbn'].notna() & df['title'].notna() & df['author'].notna() & df['isbn_add'].notna())]  # 3175140
df.isna().sum(axis = 0)
df["seq"] = df["seq"].astype(int)
indexes = list(df.index)
columns = list(df.columns)
columns.pop(0)  # seq 정보 삭제해줌.

books = []
for i in range(0, len(indexes)):
    f = {}
    f["pk"] = i + 1
    f["model"] = "books.book"
    f["fields"] = {}

    fi = f["fields"]
    d = df.loc[indexes[i]]

    for c in columns:
        fi[c] = d[c]
    
    books.append(f)
pprint(books[0])

# TypeError: Object of type int32 is not JSON serializable
# 위 에러를 피하기 위해 클래스 생성
# 단순히 np.int32 를 int 로 바꿔주는 것이다.
class npEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.int32):
            return int(obj)
        return json.JSONEncoder.default(self, obj)

with open('./data/books.json', 'w', encoding='utf-8') as f:
    json.dump(books, f, cls=npEncoder)
