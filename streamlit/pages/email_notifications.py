import streamlit as st
from service import request, URLS, cache


def email_notifications():
    st.title("Email :red[notifications]")
    if st.button('Start'):
        response = request("post", URLS["notify"], headers=cache("headers"))
        if response:
            st.success("Started successfully")
