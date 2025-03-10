import streamlit as st
import httpx


def app():
    st.title("Email :red[notifications]")
    headers = {
        "Authorization": "Bearer " + st.session_state["access"]
    }
    if st.button('Start'):
        try:
            response = httpx.post("http://127.0.0.1:8000/api/notify/", headers=headers)
        except Exception as e:
            st.error(f"Error: {type(e)}, {e}")
        else:
            if response.status_code == 200:
                st.success("Started successfully")
            else:
                st.error(f"Error {response.status_code}: {response.text}")
