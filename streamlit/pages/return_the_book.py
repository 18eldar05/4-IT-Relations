import streamlit as st
import httpx


def app():
    st.title("Return a :red[book]")
    books = httpx.get("http://127.0.0.1:8000/api/all_books/").json()
    taken_books = []
    for book in books:
        if book["is_taken"]:
            taken_books.append(book)
    choice = st.selectbox("Taken books", [book["name"] for book in taken_books])
    pk = None
    for book in taken_books:
        if choice == book["name"]:
            pk = book["id"]
            break
    headers = {
        "Authorization": "Bearer " + st.session_state["access"]
    }
    if st.button('Return'):
        response = httpx.post(f"http://127.0.0.1:8000/api/return_the_book/{pk}/", headers=headers)
        if response.status_code == 200:
            st.success(response.text)
        else:
            st.error(f"Error {response.status_code}: {response.text}")
