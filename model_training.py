import sqlite3
import pandas as pd

con = sqlite3.connect('site.db')
cur = con.cursor()

cur.execute("SELECT * FROM record")
articles = cur.fetchall()

articles_df = pd.DataFrame(articles, columns=['id', 'source_name', 'score'])
articles_df.set_index('id', inplace=True)
print(articles_df.head())
