import sys
import os

import pytest

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import pickle
import pandas as pd
from placeholder_model import generate_placeholder_model
from dataprep import get_new_articles_df, prepare_new_articles, create_features, CAT_COLS, new_data_into_ml_features


class TestPlaceholderModel:
    @pytest.fixture
    def generate_test_model(self):
        yield generate_placeholder_model(test=True)

    def test_placeholder_encoder_works_on_real_data(self, generate_test_model):
        articles_df = get_new_articles_df()
        articles_df = prepare_new_articles(articles_df)
        articles_df = create_features(articles_df)

        encoder = pickle.load(open('cat_cols_encoder_test.pkl', 'rb'))
        articles_df[CAT_COLS] = encoder.transform(articles_df[CAT_COLS])

        assert articles_df[CAT_COLS].any().any()

    def test_model_generates_predictions(self, generate_test_model):
        data_into_model = new_data_into_ml_features()
        ml_model = pickle.load(open('ml_model_test.pkl', 'rb'))
        predicted_scores = ml_model.predict(data_into_model)

        assert predicted_scores.any()
        assert (predicted_scores == 50).all()

    def test_placeholder_model_on_bogus_data(self, generate_test_model):
        data_into_model = {
            'int_col1': [1, 2, 3, 4],
            'str_col1': ['ab', 'cd', 'ef', 'gh']
        }

        data_into_model = pd.DataFrame(data_into_model)
        ml_model = pickle.load(open('ml_model_test.pkl', 'rb'))
        predicted_scores = ml_model.predict(data_into_model)

        assert predicted_scores.any()
        assert (predicted_scores == 50).all()
