import streamlit as st
from streamlit_option_menu import option_menu
from pages import home, register_and_auth, take_the_book, debt, return_the_book, assign_a_role


class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })

    def run():
        role = st.session_state.get("role", None)

        if role == "admin":
            options = ["Home", "Take a book", "Debts", "Return a book", "Assign a role", "Log out"]
            icons = ["house-fill", "plus-circle", "journal-text", "backspace", "person-up", "door-closed"]
        elif role == "librarian":
            options = ["Home", "Take a book", "Debts", "Return a book", "Log out"]
            icons = ["house-fill", "plus-circle", "journal-text", "backspace", "door-closed"]
        elif role == "reader":
            options = ["Home", "Take a book", "Debts", "Log out"]
            icons = ["house-fill", "plus-circle", "journal-text", "door-closed"]
        elif not role:
            options = ["Home", "Account", "Take a book", "Debts"]
            icons = ["house-fill", "person-circle", "plus-circle", "journal-text"]

        manual_select = st.session_state.get('menu_option', None)

        with st.sidebar:
            app = option_menu(
                menu_title="Library",
                options=options,
                icons=icons,
                manual_select=manual_select,
                menu_icon="book",
                default_index=1,
                styles={}
            )

        if app == "Home":
            home.app()
        elif app == "Account":
            register_and_auth.app()
        elif app == "Take a book":
            take_the_book.app()
        elif app == "Debts":
            debt.app()
        elif app == "Return a book":
            return_the_book.app()
        elif app == "Assign a role":
            assign_a_role.app()
        elif app == "Log out":
            st.session_state["role"] = None
            st.session_state["username"] = None
            st.session_state["access"] = None
            st.session_state["refresh"] = None
            st.session_state["menu_option"] = 1
            st.rerun()
    run()
