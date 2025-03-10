import streamlit as st
import httpx


def app():
    role = st.session_state.get("role", None)
    if not role:
        st.title("You need to log in first")
    else:
        st.title("Take a :red[book]")
        try:
            books = httpx.get("http://127.0.0.1:8000/api/all_books/").json()
        except Exception as e:
            st.error(f"Error: {type(e)}, {e}")
        else:
            choice = st.selectbox("Book", [book["name"] for book in books])
            date = st.date_input("Return date")
            pk = None
            for book in books:
                if choice in book.values():
                    pk = book["id"]
                    break
            data = {
                "date_of_return": str(date) + "T12:00:00"
            }
            headers = {
                "Authorization": "Bearer " + st.session_state["access"]
            }
            if not role == "reader":
                users = st.session_state["users"]
                whom_choice = st.selectbox("To whom", [user["username"] for user in users])
                whom_pk = None
                for user in users:
                    if whom_choice in user.values():
                        whom_pk = user["pk"]
                        break
                data.update({"reader": whom_pk})

            if st.button('Take'):
                try:
                    response = httpx.post(f"http://127.0.0.1:8000/api/take_the_book/{pk}/", json=data, headers=headers)
                except Exception as e:
                    st.error(f"Error: {type(e)}, {e}")
                else:
                    if response.status_code == 201:
                        st.success("Book has been issued")
                    else:
                        st.error(f"Error {response.status_code}: {response.text}")
