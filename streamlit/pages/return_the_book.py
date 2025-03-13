import streamlit as st
from service import request, books_selectbox, URLS


def return_the_book():
    st.title("Return a :red[book]")
    pk = books_selectbox(is_taken=True)
    headers = st.session_state["headers"]
    if st.button('Return'):
        response = request("post", f'{URLS["return_the_book"]}{pk}/', headers=headers)
        if response:
            st.success(response.text)
