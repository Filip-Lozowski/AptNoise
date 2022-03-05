import pickle

import numpy as np
import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
from sklearn.tree import DecisionTreeRegressor


encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=999)
cat_cols = ['author', 'source_name']
bogus_df = pd.DataFrame([['John Doe', 'RandomNews.com']], columns=cat_cols)
encoder.fit(bogus_df)
pickle.dump(encoder, open(f'source_encoder.pkl', 'wb'))

bogus_df = encoder.transform(bogus_df)
model = DecisionTreeRegressor()
model.fit(bogus_df, pd.Series([50]))
pickle.dump(model, open(f'ml_model.pkl', 'wb'))