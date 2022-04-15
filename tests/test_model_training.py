import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from model_training import model_training
from dataprep import new_data_into_ml_features
import pickle


def test_model_training_finishes():
    model_training(test=True)

    data_into_model = new_data_into_ml_features()
    ml_model = pickle.load(open('ml_model_test.pkl', 'rb'))
    predicted_scores = ml_model.predict(data_into_model)

    assert predicted_scores.any()
