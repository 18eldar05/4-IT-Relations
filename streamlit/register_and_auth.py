import streamlit as st
import httpx


def app():
    access = None
    refresh = None

    st.title('Welcome to :red[Library]')

    choice = st.selectbox("Log in/Sign up", ["Log in", "Sign up"])
    if choice == "Log in":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button('Enter'):
            data = {
                "username": username,
                "password": password,
            }
            response = httpx.post("http://127.0.0.1:8000/api/token/", json=data)
            if "access" in response.json():
                access = response.json()["access"]
                refresh = response.json()["refresh"]
                st.success("Hello, " + username)
            else:
                st.warning("Error: " + response.text)
    else:
        username2 = st.text_input("Username")
        email = st.text_input("Email")
        password2 = st.text_input("Password", type="password")
        if st.button('Create my account'):
            data = {
                "username": username2,
                "email": email,
                "password": password2,
            }
            response = httpx.post("http://127.0.0.1:8000/api/register/", json=data)
            if "token" in response.json():
                access = response.json()["token"]["access"]
                refresh = response.json()["token"]["refresh"]
                st.success("Account created successfully!")
                st.balloons()
            else:
                st.warning("Error: " + response.text)
