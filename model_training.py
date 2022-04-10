import pickle
from sklearn.preprocessing import OrdinalEncoder
from sklearn.tree import DecisionTreeRegressor
from dataprep import db_into_ml


def model_training(test):
    training = db_into_ml(set_type='training')
    y_train = training['assigned_score']

    feature_cols = ['author', 'source_name', 'content_length_chars']
    cat_cols = ['author', 'source_name']
    x_train = training[feature_cols].copy()
    encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=999)
    encoder.fit(x_train[cat_cols])
    x_train[cat_cols] = encoder.transform(x_train[cat_cols])

    model = DecisionTreeRegressor(max_depth=1, random_state=23)
    model.fit(x_train, y_train)

    if test:
        suffix = '_test'
    else:
        suffix = ''

    pickle.dump(encoder, open(f'source_encoder{suffix}.pkl', 'wb'))
    pickle.dump(model, open(f'ml_model{suffix}.pkl', 'wb'))

    return None


if __name__ == '__main__':
    model_training(test=False)
