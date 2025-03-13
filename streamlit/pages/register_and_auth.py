import streamlit as st
from time import sleep
from service import request, URLS


def register_and_auth():
    st.title("Welcome to :red[Library]")
    choice = st.selectbox("Log in/Sign up", ["Log in", "Sign up"])
    if choice == "Log in":
        response = log_in()
    else:
        response = sign_up()
    if response:
        st.session_state["headers"] = {"Authorization": "Bearer " + response.json()["access"]}
        st.session_state["refresh"] = response.json()["refresh"]
        st.session_state["menu_option"] = 0
        st.switch_page("main.py")


def log_in():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Enter"):
        data = {
            "username": username,
            "password": password,
        }
        response = request("post", URLS["token"], data=data)
        if response:
            st.success("Logged in successfully!")
            # st.session_state["headers"] = {"Authorization": "Bearer " + response.json()["access"]}
            # st.session_state["refresh"] = response.json()["refresh"]
        st.session_state["username"] = username
        users_response = request("get", URLS["all_users"])
        if users_response:
            users = users_response.json()
            for user in users:
                if username == user["username"]:
                    st.session_state["role"] = user["role"]
                    break
        return response
        # st.session_state["menu_option"] = 0
        # st.switch_page("main.py")


def sign_up():
    username = st.text_input("Username")
    email = st.text_input("Email")
    first_name = st.text_input("First name")
    last_name = st.text_input("Last name")
    password = st.text_input("Password", type="password")
    if st.button("Create my account"):
        data = {
            "username": username,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
        }
        response = request("post", URLS["register"], data=data)
        if response:
            st.success("Account created successfully!")
            st.balloons()
            sleep(1)
            # st.session_state["headers"] = {"Authorization": "Bearer " + response.json()["token"]["access"]}
            # st.session_state["refresh"] = response.json()["token"]["refresh"]
        st.session_state["username"] = username
        st.session_state["role"] = "reader"
        return response
        # st.session_state["menu_option"] = 0
        # st.switch_page("main.py")
