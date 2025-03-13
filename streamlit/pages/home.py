import streamlit as st


def view_home():
    username = st.session_state.get("username", None)
    if username:
        st.title(f"Hello, :red[{username}]!")
    else:
        st.title("Hello!")
