import streamlit as st
import httpx

access = None
refresh = None

st.title('Registration')
username = st.text_input("Username", key=1)
email = st.text_input("Email", key=2)
password = st.text_input("Password", key=3)
if st.button("Sign up"):
    data = {
        "username": username,
        "email": email,
        "password": password,
    }
    response = httpx.post("http://127.0.0.1:8000/api/register/", json=data)

    if "token" in response.json():
        access = response.json()["token"]["access"]
        refresh = response.json()["token"]["refresh"]
        st.write("Hello,", username)
    else:
        st.write("Error:", response.text)

st.title('Authorization')
username2 = st.text_input("Username", key=4)
password2 = st.text_input("Password", key=5)
if st.button("Log in"):
    data = {
        "username": username2,
        "password": password2,
    }
    response = httpx.post("http://127.0.0.1:8000/api/token/", json=data)
    if "access" in response.json():
        access = response.json()["access"]
        refresh = response.json()["refresh"]
        st.write("Hello,", username2)
    else:
        st.write("Error:", response.text)
