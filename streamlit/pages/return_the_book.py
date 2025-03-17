import streamlit as st
from service import request, books_selectbox, URLS, cache


def return_the_book():
    st.title("Return a :red[book]")
    pk = books_selectbox(is_taken=True)
    if st.button('Return'):
        response = request("post", f'{URLS["return_the_book"]}{pk}/', headers=cache("headers"))
        if response:
            st.success(response.text)
