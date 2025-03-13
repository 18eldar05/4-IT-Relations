import streamlit as st
from streamlit_option_menu import option_menu
from pages import home, register_and_auth, take_the_book, debt, return_the_book, assign_a_role, logout

FUNCTIONS = {
    "Home": home.view_home,
    "Account": register_and_auth.register_and_auth,
    "Take a book": take_the_book.take_the_book,
    "Debts": debt.view_debts,
    "Return a book": return_the_book.return_the_book,
    "Assign a role": assign_a_role.assign_a_role,
    "Log out": logout.logout
}

OPTIONS = {
    "admin": ["Home", "Take a book", "Debts", "Return a book", "Assign a role", "Log out"],
    "librarian": ["Home", "Take a book", "Debts", "Return a book", "Log out"],
    "reader": ["Home", "Take a book", "Debts", "Log out"],
    None: ["Home", "Account", "Take a book", "Debts"]
}

ICONS = {
    "admin": ["house-fill", "plus-circle", "journal-text", "backspace", "person-up", "door-closed"],
    "librarian": ["house-fill", "plus-circle", "journal-text", "backspace", "door-closed"],
    "reader": ["house-fill", "plus-circle", "journal-text", "door-closed"],
    None: ["house-fill", "person-circle", "plus-circle", "journal-text"]
}


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
        manual_select = st.session_state.get('menu_option', None)
        with st.sidebar:
            app = option_menu(
                menu_title="Library",
                options=OPTIONS[role],
                icons=ICONS[role],
                manual_select=manual_select,
                menu_icon="book",
                default_index=1,
                styles={}
            )
        FUNCTIONS[app]()
    run()
