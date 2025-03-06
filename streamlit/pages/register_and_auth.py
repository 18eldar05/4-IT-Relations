import streamlit as st
import httpx
from time import sleep


def app():
    st.title("Welcome to :red[Library]")
    choice = st.selectbox("Log in/Sign up", ["Log in", "Sign up"])
    if choice == "Log in":
        log_in()
    else:
        sign_up()


def log_in():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Enter"):
        data = {
            "username": username,
            "password": password,
        }
        response = httpx.post("http://127.0.0.1:8000/api/token/", json=data)
        if response.status_code == 200:
            st.success("Logged in successfully!")
            st.session_state["access"] = response.json()["access"]
            st.session_state["refresh"] = response.json()["refresh"]
            st.session_state["username"] = username
            users = httpx.get("http://127.0.0.1:8000/api/all_users/").json()
            st.session_state["users"] = users
            for user in users:
                if username in user.values():
                    st.session_state["role"] = user["role"]
                    break
            st.session_state["menu_option"] = 0
            st.switch_page("main.py")
        else:
            st.error("Error " + str(response.status_code) + ": " + response.text)


def sign_up():
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Create my account"):
        data = {
            "username": username,
            "email": email,
            "password": password,
        }
        response = httpx.post("http://127.0.0.1:8000/api/register/", json=data)
        if response.status_code == 201:
            st.success("Account created successfully!")
            st.balloons()
            st.session_state["access"] = response.json()["token"]["access"]
            st.session_state["refresh"] = response.json()["token"]["refresh"]
            st.session_state["username"] = username
            st.session_state["role"] = "reader"
            st.session_state["menu_option"] = 0
            st.session_state["users"] = httpx.get("http://127.0.0.1:8000/api/all_users/").json()
            sleep(1)
            st.switch_page("main.py")
        else:
            st.error(f"Error {response.status_code}: {response.text}")
