import streamlit as st
from service import request, users_selectbox, URLS, cache


def assign_a_role():
    st.title("Assign a :red[role]")
    pk = users_selectbox()
    role_choice = st.selectbox("Role", ["librarian", "admin", "reader"], format_func=lambda s: s.title())
    data = {
        "role": role_choice
    }
    if st.button('Assign'):
        response = request("patch", f'{URLS["role"]}{pk}/', data=data, headers=cache("headers"))
        if response:
            st.success("Role changed successfully")
