import streamlit as st
import httpx


def app():
    st.title("Assign a :red[role]")
    pk = None
    users = st.session_state["users"]
    choice = st.selectbox("User", [user["username"] for user in users], index=None)
    for user in users:
        if choice == user["username"]:
            pk = user["pk"]
            break
    role_choice = st.selectbox("Role", ["librarian", "admin", "reader"], format_func=lambda s: s.title())
    data = {
        "role": role_choice
    }
    headers = {
        "Authorization": "Bearer " + st.session_state["access"]
    }
    if st.button('Assign'):
        try:
            response = httpx.patch(f"http://127.0.0.1:8000/api/role/{pk}/", json=data, headers=headers)
        except Exception as e:
            st.error(f"Error: {type(e)}, {e}")
        else:
            if response.status_code == 200:
                st.success("Role changed successfully")
            else:
                st.error(f"Error {response.status_code}: {response.text}")
