import streamlit as st
from service import cache


def view_home():
    username = cache("username")
    if username:
        st.title(f"Hello, :red[{username}]!")
    else:
        st.title("Hello!")
