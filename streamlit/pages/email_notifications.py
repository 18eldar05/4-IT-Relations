import streamlit as st
from service import request, URLS


def email_notifications():
    st.title("Email :red[notifications]")
    headers = st.session_state["headers"]
    if st.button('Start'):
        response = request("post", URLS["notify"], headers=headers)
        if response:
            st.success("Started successfully")
