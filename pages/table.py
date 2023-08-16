from pandas.api.types import (
    is_int64_dtype,
    is_float_dtype,
)
import pandas as pd
import streamlit as st


class ShowTable:
    def __init__(self, path='data/titanic_dataset_train.csv') -> None:
        self.df = pd.read_csv(path)

    def run(self) -> None:
        self.show_main_page()
        self.show_dataframe()

    def show_main_page(self) -> None:
        st.set_page_config(
            page_title='Titanic dataset',
            page_icon=':see_no_evil:',
            layout='wide',
            initial_sidebar_state='auto',
        )
        st.write(
            """
            # Таблица для обучения модели
            Поиграемся с ней
            """
        )

    def filter_dataframe(self) -> None:
        modification_container = st.container()
        with modification_container:
                columns_to_filter = st.multiselect('Добавить фильтры', self.df.columns)

                for column in columns_to_filter:
                    left, right = st.columns((1, 20))
                    left.write('↳')

                    if column == 'Survived':
                        user_radio_input = right.radio('Выжил или погиб в катастрофе' ,('Выжил', 'Погиб'))
                        data = {'Выжил': 1,'Погиб': 0}

                        self.df = self.df[self.df[column] == data[user_radio_input]]

                        continue

                    if is_int64_dtype(self.df[column]):
                        _min = int(self.df[column].min())
                        _max = int(self.df[column].max())
                        user_int_input = right.slider(
                            f'Значения для колонки {column}',
                            min_value=_min,
                            max_value=_max,
                            value=(_min, _max),
                        )
                        self.df = self.df[self.df[column].between(*user_int_input)]

                    elif is_float_dtype(self.df[column]):
                        _min = float(self.df[column].min())
                        _max = float(self.df[column].max())
                        user_int_input = right.slider(
                            f'Значения для колонки {column}',
                            min_value=_min,
                            max_value=_max,
                            value=(_min, _max),
                        )
                        self.df = self.df[self.df[column].between(*user_int_input)]

                    else:
                        user_text_input = right.text_input(
                            f'Substring or regex in {column}',
                        )
                        if user_text_input:
                            self.df = self.df[self.df[column].astype(str).str.contains(user_text_input)]

    def hide_columns(self) -> None:
        visible_columns = list(self.df.columns.values)
        modification_container = st.container()

        with modification_container:
            columns_to_hide = st.multiselect('Спрятать колонки', self.df.columns.values)

            for column in columns_to_hide:
                if column in visible_columns:
                    visible_columns.remove(column)

            self.df = self.df[visible_columns]

    def show_dataframe(self) -> None:
        hide_columns = st.checkbox('Убрать лишние колонки')
        
        if hide_columns:
            self.hide_columns()
        
        modify = st.checkbox('Добавить фильтры')
        
        if modify:
            self.filter_dataframe()
        
        st.dataframe(self.df)


if __name__ == '__main__':
    app = ShowTable()
    app.run()
