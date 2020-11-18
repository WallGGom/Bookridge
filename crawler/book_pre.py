import pandas as pd

df = pd.read_csv("./data/book_info.csv", error_bad_lines=False, encoding="utf-8", low_memory=False)
df.head()
df = df.rename(columns={'?master_seq': 'seq', 'isbn13': 'isbn', 'add_code': 'isbn_add'})
df.columns
# new_df = df[df["description"].isna() == False]["description"]
pd.to_pickle(df, './data/books.pkl')