import pickle
import sqlite3
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeRegressor

con = sqlite3.connect('site.db')
cur = con.cursor()

cur.execute("SELECT * FROM record")
articles = cur.fetchall()

articles_df = pd.DataFrame(articles, columns=['id', 'source_name', 'score'])
articles_df.set_index('id', inplace=True)

encoder = LabelEncoder()
encoder.fit(articles_df['source_name'])

training_data = articles_df.copy()
training_data['source_name'] = encoder.transform(training_data['source_name'])
x_train = training_data.drop(columns=['score'])
y_train = training_data['score']

model = DecisionTreeRegressor()
model.fit(x_train, y_train)

pickle.dump(encoder, open('source_encoder.pkl', 'wb'))
pickle.dump(model, open('ml_model.pkl', 'wb'))
