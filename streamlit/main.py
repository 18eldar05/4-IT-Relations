import streamlit as st
from streamlit_option_menu import option_menu
from pages import home, register_and_auth


class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })

    def run():
        manual_select = st.session_state.get('menu_option', None)

        if not manual_select == 0:
            options = ["Home", "Account"]
        else:
            options = ["Home",]

        with st.sidebar:
            app = option_menu(
                menu_title="Library",
                options=options,
                icons=["house-fill", "person-circle"],
                manual_select=manual_select,
                menu_icon="book",
                default_index=1,
                styles={}
            )

        if app == "Home":
            home.app()
        if app == "Account":
            register_and_auth.app()
    run()
