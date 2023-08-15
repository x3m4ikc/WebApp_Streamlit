from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from pickle import dump, load
import pandas as pd
from typing import Tuple


class TitanicSurvivalClassifier:
    def __init__(self) -> None:
        self.model = RandomForestClassifier()

    def open_data(self, path='data/titanic_dataset_train.csv') -> pd.DataFrame:
        df = pd.read_csv(path)
        df = df[['Survived', 'Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Embarked']]
        return df
    
    def split_data(self, df) -> Tuple[pd.DataFrame, pd.DataFrame]:
        y = df['Survived'] # Target variable
        X = df[['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Embarked']]
        return X, y

    def preprocess_data(self, df, test=True) -> Tuple[pd.DataFrame, pd.DataFrame] | pd.DataFrame:
        """Prepare data to train model"""
        df.dropna(inplace=True)

        if test:
            X_df, y_df = self.split_data(df)
        else:
            X_df = df

        to_encode = ['Sex', 'Embarked']
        for column in to_encode:
            dummy = pd.get_dummies(X_df[column], prefix=column)
            X_df = pd.concat([X_df, dummy], axis=1)
            X_df.drop(column, axis=1, inplace=True)

        if test:
            return X_df, y_df
        return X_df
    
    def fit_and_save_model(self, X_df, y_df, path='data/model_weights.mw') -> None:
        self.model.fit(X_df, y_df)

        test_prediction = self.model.predict(X_df)
        accuracy = accuracy_score(test_prediction, y_df)

        print(f'Model accuracy is {accuracy}')

        with open(path, 'wb') as file:
            dump(self.model, file)

        print(f'Model was saved to {path}')

    def load_model_and_predict(self, df, path='data/model_weights.mw') -> Tuple[pd.DataFrame, pd.DataFrame]:
        with open(path, 'rb') as file:
            self.model = load(file)
            
        prediction = self.model.predict(df)[0]
        prediction_proba = self.model.predict_proba(df)[0]

        encode_prediction_proba = {
            0: 'Вам не повезло с вероятностью',
            1: 'Вы выживите с вероятностью'
        }

        encode_prediction = {
            0: 'Вам не повезло',
            1: 'Вы будете жить'
        }

        prediction_data = {}
        for key, value in encode_prediction_proba.items():
            prediction_data.update({value: prediction_proba[key]})

        prediction_df = pd.DataFrame(prediction_data, index=[0])
        prediction_result = encode_prediction[prediction]

        return prediction_result, prediction_df
            

if __name__ == "__main__":
    classifier = TitanicSurvivalClassifier()
    df = classifier.open_data()
    X_df, y_df = classifier.preprocess_data(df)
    classifier.fit_and_save_model(X_df, y_df)
