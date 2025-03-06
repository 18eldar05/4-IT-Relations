import streamlit as st


def app():
    username = st.session_state.get("username", None)
    if username:
        st.title(f"Hello, :red[{username}]!")
    else:
        st.title("Hello!")
