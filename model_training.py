import pickle
from sklearn.preprocessing import OrdinalEncoder
from sklearn.tree import DecisionTreeRegressor
from dataprep import db_to_df


def model_training(test):
    articles = db_to_df()
    articles = articles[articles['assigned_score'] != -999]
    articles = articles.drop_duplicates(subset=['title', 'published_at'])

    training = articles[articles['is_test_record'] == 0]
    y_train = training['assigned_score']

    feature_cols = ['author', 'source_name']
    x_train = training[feature_cols]
    encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=999)
    encoder.fit(x_train)
    x_train = encoder.transform(x_train)

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
