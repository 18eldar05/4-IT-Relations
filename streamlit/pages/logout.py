import streamlit as st


def logout():
    st.session_state["role"] = None
    st.session_state["username"] = None
    st.session_state["headers"] = None
    st.session_state["refresh"] = None
    st.session_state["menu_option"] = 1
    st.rerun()
