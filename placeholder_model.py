import pickle

import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
from sklearn.tree import DecisionTreeRegressor

from dataprep import FEATURE_COLS


encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=999)
bogus_df = pd.DataFrame([['John Doe', 'RandomNews.com', 1000]], columns=FEATURE_COLS)
encoder.fit(bogus_df)
pickle.dump(encoder, open(f'source_encoder.pkl', 'wb'))

bogus_df = encoder.transform(bogus_df)
model = DecisionTreeRegressor()
model.fit(bogus_df, pd.Series([50]))
pickle.dump(model, open(f'ml_model.pkl', 'wb'))
