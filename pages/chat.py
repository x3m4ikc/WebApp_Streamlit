import streamlit as st
import smtplib

class SupportChat:
    def __init__(self) -> None:
        self.EMAIL_PASS = st.secrets['EMAIL_PASS']
        self.EMAIL_FROM = st.secrets['EMAIL_LOGIN']
        self.EMAIL_TO = st.secrets['EMAIL_TO']

    def run(self):
        self.show_main_page()
        self.init_chat_history()
        self.get_user_message()
        self.send_email_to_support()
        self.give_user_answer()

    def show_main_page(self):
        st.set_page_config(
            page_title='Чат поддержки',
            page_icon=':speak_no_evil:',
            layout='wide',
            initial_sidebar_state='auto',
        )
        st.write(
            """
            # Чат поддержки
            """
        )
        
        hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    def init_chat_history(self):
        if 'messages' not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message['role']):
                st.markdown(message['content'])

    def get_user_message(self):
        if prompt := st.chat_input('Слова поддержке'):
            st.chat_message('user').markdown(prompt)
            st.session_state.messages.append({'role': 'user', 'content': prompt})

    def send_email_to_support(self):            # TODO: имейл для бота
        if st.session_state.messages:
            msg = st.session_state.messages[-1]['content']
            letter = 'Subject: {}\n\n{}'.format('SUBJECT', msg)
            letter = letter.encode('UTF-8')

            server = smtplib.SMTP_SSL('smtp.mail.ru:465')
            server.login(self.EMAIL_FROM, self.EMAIL_PASS)
            server.sendmail(self.EMAIL_FROM, self.EMAIL_TO, letter)
            server.quit()

    def give_user_answer(self):
        if st.session_state.messages:
            response = 'Ваше обращение принято в обработку'
            with st.chat_message('assistant'):
                    st.markdown(response)

            st.session_state.messages.append({'role': 'assistant', 'content': response})

if __name__ == '__main__':
    app = SupportChat()
    app.run()
