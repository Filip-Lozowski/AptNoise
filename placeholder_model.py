import pickle
import numpy as np


class PlaceholderModel:
    def predict(self, input_data):
        n_predictions = len(input_data)
        return np.full(n_predictions, 50)


def generate_placeholder_model(test):
    if test:
        suffix = '_test'
    else:
        suffix = ''

    model = PlaceholderModel()
    pickle.dump(model, open(f'ml_model{suffix}.pkl', 'wb'))
