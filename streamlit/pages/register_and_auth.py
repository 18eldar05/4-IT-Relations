import streamlit as st
import httpx
from time import sleep


def app():
    access = None
    refresh = None

    st.title('Welcome to :red[Library]')

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
            access = response.json()["access"]
            refresh = response.json()["refresh"]
            st.success("Hello, " + username)
            st.session_state['menu_option'] = 0
            st.switch_page("main.py")
        else:
            st.warning("Error " + str(response.status_code) + ": " + response.text)


def sign_up():
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button('Create my account'):
        data = {
            "username": username,
            "email": email,
            "password": password,
        }
        response = httpx.post("http://127.0.0.1:8000/api/register/", json=data)
        if response.status_code == 201:
            access = response.json()["token"]["access"]
            refresh = response.json()["token"]["refresh"]
            st.success("Account created successfully!")
            st.balloons()
            st.session_state['menu_option'] = 0
            sleep(1.3)
            st.switch_page("main.py")
        else:
            st.warning("Error " + str(response.status_code) + ": " + response.text)
