import streamlit as st
from time import sleep
from service import request, URLS, cache


def register_and_auth():
    st.title("Welcome to :red[Library]")
    choice = st.selectbox("Log in/Sign up", ["Log in", "Sign up"])
    functions = {
        "Log in": log_in,
        "Sign up": sign_up
    }
    response, username, role = functions[choice]()
    if response:
        st.session_state["username"] = username
        st.session_state["role"] = role
        st.session_state["headers"] = {"Authorization": "Bearer " + response.json()["access"]}
        st.session_state["refresh"] = response.json()["refresh"]
        cache.clear()
        cache("headers")
        cache("username")
        cache("role")
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
            role = None
            users_response = request("get", URLS["all_users"])
            if users_response:
                users = users_response.json()
                for user in users:
                    if username == user["username"]:
                        role = user["role"]
                        break
            return response, username, role
    return None, None, None


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
            return response, username, "reader"
    return None, None, None
