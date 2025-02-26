import streamlit as st

from streamlit_option_menu import option_menu

import home, register_and_auth

# st.set_page_config(
#     page_title="Pondering"
# )


class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })

    def run():
        with st.sidebar:
            app = option_menu(
                menu_title="Library",
                options=["Home", "Account"],
                icons=["house-fill", "person-circle"],
                menu_icon="book",
                default_index=1,
                styles={}
            )

        if app == "Home":
            home.app()
        if app == "Account":
            register_and_auth.app()
    run()
