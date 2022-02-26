import pickle
from sklearn.preprocessing import OrdinalEncoder
from sklearn.tree import DecisionTreeRegressor
from dataprep import db_to_df


def model_training(test):
    articles_df = db_to_df()

    encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=999)
    cat_cols = ['author', 'source_name']
    encoder.fit(articles_df[cat_cols])

    training_data = articles_df.copy()
    training_data.dropna(how='any', inplace=True)

    training_data[cat_cols] = encoder.transform(training_data[cat_cols])
    x_train = training_data[['author', 'source_name']]
    y_train = training_data['assigned_score']

    model = DecisionTreeRegressor()
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
