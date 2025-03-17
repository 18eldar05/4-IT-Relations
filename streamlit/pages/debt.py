import streamlit as st
import datetime
from datetime import datetime
import time
from service import request, users_selectbox, URLS, cache


def view_debts():
    role = cache("role")
    if not role:
        st.title("You need to log in first")
    else:
        if not role == "reader":
            st.title(":red[Debts]")
            user_pk = users_selectbox()
            if user_pk:
                response = request("get", f'{URLS["debt"]}{user_pk}/', headers=cache("headers"))
                no_debts_message = "User has no debts:ok_hand:"
            else:
                response = request("get", URLS["debt"], headers=cache("headers"))
                no_debts_message = "You have no debts:thumbsup:"
        else:
            st.title("Your :red[debts]")
            response = request("get", URLS["debt"], headers=cache("headers"))
            no_debts_message = "You have no debts:thumbsup:"

        if response:
            if response.status_code == 204:
                st.header(no_debts_message)
            else:
                st.divider()
                debts = eval(response.text)["List of debts"]
                for debt in debts:
                    pk = debt["book"]
                    book_response = request("get", f'{URLS["book"]}{pk}/')
                    if not book_response:
                        break
                    book = book_response.json()
                    return_date = datetime.strptime(debt["date_of_return"], '%Y-%m-%dT%H:%M:%SZ')
                    return_date_pretty = time.asctime(return_date.timetuple())
                    remaining = return_date - datetime.now()
                    st.html(f"<p style=\"font-size: 205%; font-weight: 600\">\"{book['name']}\"<br>"
                            f"Return date: {return_date_pretty}<br>Time remaining: {remaining.days} days</p>")
                    st.divider()
