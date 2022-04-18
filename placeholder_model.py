import pickle
import numpy as np


class PlaceholderEncoder:
    def transform(self, input_data):
        return input_data


class PlaceholderModel:
    def predict(self, input_data):
        n_predictions = len(input_data)
        return np.full(n_predictions, 50)


def generate_placeholder_model(test):
    if test:
        suffix = '_test'
    else:
        suffix = ''

    encoder = PlaceholderEncoder()
    model = PlaceholderModel()

    pickle.dump(encoder, open(f'cat_cols_encoder{suffix}.pkl', 'wb'))
    pickle.dump(model, open(f'ml_model{suffix}.pkl', 'wb'))
