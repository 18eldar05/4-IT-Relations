import streamlit as st
from service import request, books_selectbox, users_selectbox, URLS, cache


def take_the_book():
    role = cache("role")
    if not role:
        st.title("You need to log in first")
    else:
        st.title("Take a :red[book]")
        pk = books_selectbox()
        date = st.date_input("Return date")
        data = {
            "date_of_return": str(date) + "T12:00:00"
        }
        if not role == "reader":
            whom_pk = users_selectbox(label="To whom")
            data.update({"reader": whom_pk})

        if st.button("Take"):
            response = request("post", f"{URLS['take_the_book']}{pk}/", data=data, headers=cache("headers"))
            if response:
                st.success("Book has been issued")
