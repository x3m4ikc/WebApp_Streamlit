import pandas as pd
import streamlit as st
from PIL import Image
from model import TitanicSurvivalClassifier

class TitanicApp:
    def __init__(self) -> None:
        self.classifier = TitanicSurvivalClassifier()

    def run(self) -> None:
        self.show_main_page()
        self.proccess_side_inputs()

    def show_main_page(self) -> None:
        image = Image.open('data/image.jpg')
        st.set_page_config(
            page_title='Titanic Survivors ML_Classifier',
            page_icon=':ship:',
            layout='wide',
            initial_sidebar_state='auto',
            menu_items={
                'About': 'Pet-project для обучения возможностям streamlit'
            }
        )

        st.write(
            """
            # Классификация пассажиров Титаника
            Определим, кто из пассажирова выживет, а кто - нет 
            """
        )

        st.image(image)

    def proccess_side_inputs(self) -> None:
        st.sidebar.header('Задайте параметры пассажира')
        user_input_df = self.sidebar_input_features()

        train_df = self.classifier.open_data()
        train_X_df, _ = self.classifier.split_data(train_df)
        full_X_df = pd.concat((user_input_df, train_X_df), axis=0)
        preprocessed_X_df = self.classifier.preprocess_data(full_X_df, test=False)

        user_X_df = preprocessed_X_df[:1]
        self.write_user_data(user_X_df)

        prediction, prediction_probas = self.classifier.load_model_and_predict(user_X_df)
        self.write_prediction(prediction, prediction_probas)

    def sidebar_input_features(self) -> pd.DataFrame:
        sex = st.sidebar.selectbox('Пол', ('Мужской', 'Женский'))
        embarked = st.sidebar.selectbox('Порт посадки', (
            'Шербур-Октевиль', 'Квинстаун', 'Саутгемптон'))
        pclass = st.sidebar.selectbox('Класс', (
            'Первый', 'Второй', 'Третий'))
        age = st.sidebar.slider('Возраст', min_value=1, max_value=80, value=20, step=1)
        sib_sp = st.sidebar.slider('Количество братьев / сестер / супругов на борту')
        par_ch = st.sidebar.slider('Количество детей / родителей на борту',
                                   min_value=0, max_value=10, value=0, step=1)
        
        translation = {
            "Мужской": "male",
            "Женский": "female",
            "Шербур-Октевиль": "C",
            "Квинстаун": "Q",
            "Саутгемптон": "S",
            "Первый": 1,
            "Второй": 2,
            "Третий": 3,
        }

        data = {
        "Pclass": translation[pclass],
        "Sex": translation[sex],
        "Age": age,
        "SibSp": sib_sp,
        "Parch": par_ch,
        "Embarked": translation[embarked]
    }
        df = pd.DataFrame(data, index=[0])

        return df

    def write_user_data(self, df) -> pd.DataFrame:
        st.write("## Ваши данные")
        st.write(df)

    def write_prediction(self, prediction, prediction_probas):
        st.write("## Вероятность предсказания")
        st.write(prediction)

        st.write('## Вероятность предсказания')
        st.write(prediction_probas)
    
if __name__ == '__main__':
    app = TitanicApp()
    app.run()
