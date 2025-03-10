import streamlit as st
import httpx
import datetime
from datetime import datetime
import time


def app():
    role = st.session_state.get("role", None)
    if not role:
        st.title("You need to log in first")
    else:
        headers = {
            "Authorization": "Bearer " + st.session_state["access"]
        }
        error = False
        if not role == "reader":
            st.title(":red[Debts]")
            user_pk = None
            users = st.session_state["users"]
            choice = st.selectbox("User", [user["username"] for user in users], index=None)
            for user in users:
                if choice and choice in user.values():
                    user_pk = user["pk"]
                    break
            if user_pk:
                try:
                    response = httpx.get(f"http://127.0.0.1:8000/api/debt/{user_pk}/", headers=headers)
                except Exception as e:
                    st.error(f"Error: {type(e)}, {e}")
                    error = True
                no_debts_message = "User has no debts:ok_hand:"
            else:
                try:
                    response = httpx.get("http://127.0.0.1:8000/api/debt/", headers=headers)
                except Exception as e:
                    st.error(f"Error: {type(e)}, {e}")
                    error = True
                no_debts_message = "You have no debts:thumbsup:"
        else:
            st.title("Your :red[debts]")
            try:
                response = httpx.get("http://127.0.0.1:8000/api/debt/", headers=headers)
            except Exception as e:
                st.error(f"Error: {type(e)}, {e}")
                error = True
            no_debts_message = "You have no debts:thumbsup:"

        if not error:
            if response.status_code == 204:
                st.header(no_debts_message)
            elif response.status_code >= 400:
                st.error(f"Error {response.status_code}: {response.text}")
            else:
                st.divider()
                debts = eval(response.text)["List of debts"]
                for debt in debts:
                    pk = debt["book"]
                    try:
                        book = httpx.get(f"http://127.0.0.1:8000/api/book/{pk}/").json()
                    except Exception as e:
                        st.error(f"Error: {type(e)}, {e}")
                        break
                    return_date = datetime.strptime(debt["date_of_return"], '%Y-%m-%dT%H:%M:%SZ')
                    return_date_pretty = time.asctime(return_date.timetuple())
                    remaining = return_date - datetime.now()
                    st.html(f"<p style=\"font-size: 205%; font-weight: 600\">\"{book['name']}\"<br>"
                            f"Return date: {return_date_pretty}<br>Time remaining: {remaining.days} days</p>")
                    st.divider()
