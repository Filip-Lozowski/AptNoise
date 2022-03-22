import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from model_training import model_training
from dataprep import download_articles, prepare_articles, derive_content_length
from config import api_key
import pickle

api_url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey='


def test_model_training_finishes():
    model_training(test=True)

    raw_articles = download_articles(api_url, api_key)
    data_into_model = prepare_articles(raw_articles)
    data_into_model = data_into_model[['author', 'source_name', 'content']]
    data_into_model.dropna(subset='content', inplace=True)

    cat_cols = ['author', 'source_name']
    encoder = pickle.load(open('source_encoder_test.pkl', 'rb'))
    data_into_model[cat_cols] = encoder.transform(data_into_model[cat_cols])

    data_into_model['content_length_chars'] = data_into_model.apply(derive_content_length, axis=1)
    data_into_model.dropna(subset='content_length_chars', inplace=True)
    data_into_model.drop(columns='content', inplace=True)

    ml_model = pickle.load(open('ml_model_test.pkl', 'rb'))
    predicted_scores = ml_model.predict(data_into_model)

    assert predicted_scores.any()
