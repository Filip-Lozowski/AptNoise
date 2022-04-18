import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import pickle
import pandas as pd
from placeholder_model import generate_placeholder_model
from dataprep import new_data_into_ml_features


def test_model_generates_predictions():
    generate_placeholder_model(test=True)
    data_into_model = new_data_into_ml_features()
    ml_model = pickle.load(open('ml_model_test.pkl', 'rb'))
    predicted_scores = ml_model.predict(data_into_model)

    assert predicted_scores.any()
    assert (predicted_scores == 50).all()


def test_placeholder_model_on_bogus_data():
    generate_placeholder_model(test=True)
    data_into_model = {
        'int_col1': [1, 2, 3, 4],
        'str_col1': ['ab', 'cd', 'ef', 'gh']
    }

    data_into_model = pd.DataFrame(data_into_model)
    ml_model = pickle.load(open('ml_model_test.pkl', 'rb'))
    predicted_scores = ml_model.predict(data_into_model)

    assert predicted_scores.any()
    assert (predicted_scores == 50).all()
