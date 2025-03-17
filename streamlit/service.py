import streamlit as st
import httpx

URLS = {
    "token": "http://127.0.0.1:8000/api/token/",
    "register": "http://127.0.0.1:8000/api/register/",
    "all_users": "http://127.0.0.1:8000/api/all_users/",
    "all_books": "http://127.0.0.1:8000/api/all_books/",
    "book": "http://127.0.0.1:8000/api/book/",
    "take_the_book": "http://127.0.0.1:8000/api/take_the_book/",
    "return_the_book": "http://127.0.0.1:8000/api/return_the_book/",
    "debt": "http://127.0.0.1:8000/api/debt/",
}


def request(method: str, url: str, **kwargs):
    try:
        if method == "get":
            response = httpx.get(url, headers=kwargs.get("headers"))
        elif method == "post":
            response = httpx.post(url, json=kwargs.get("data"), headers=kwargs.get("headers"))
        elif method == "patch":
            response = httpx.patch(url, json=kwargs.get("data"), headers=kwargs.get("headers"))
        else:
            raise NameError("Unknown method")
        response.raise_for_status()
        return response
    except httpx.ReadTimeout:
        st.error("Error: The server did not send any data in the allowed amount of time")
    except httpx.TimeoutException:
        st.error("Error: An operation has timed out. The server is probably sick. You can retry in several seconds")
    except httpx.ConnectError:
        st.error("Error: Couldn't connect to the server")
    except httpx.NetworkError:
        st.error("An error occurred while interacting with the network")
    except httpx.HTTPStatusError:
        st.error("Error " + str(response.status_code) + ": " + response.text)
    except httpx.InvalidURL:
        st.error("Error: URL is improperly formed or cannot be parsed")
    except httpx.TooManyRedirects:
        st.error("Error: Too many redirects. Your URL was bad. Try a different one")
    except httpx.DecodingError:
        st.error("Error: Couldn't decode the text into json")
    except httpx.RequestError as e:
        st.error(f"Error: There was an ambiguous exception that occurred while handling your request - {e}")


def users_selectbox(**kwargs):
    response = request("get", URLS["all_users"])
    if response:
        users = response.json()
        choice = st.selectbox(kwargs.get("label", "User"), [user["username"] for user in users], index=None)
        for user in users:
            if choice == user["username"]:
                return user["pk"]


def books_selectbox(**kwargs):
    response = request("get", URLS["all_books"])
    if response:
        books = response.json()
        shortened_books = []
        for book in books:
            if book["is_taken"] == kwargs.get("is_taken", False):
                shortened_books.append(book)
        choice = st.selectbox("Books", [book["name"] for book in shortened_books])
        for book in shortened_books:
            if choice == book["name"]:
                return book["id"]


@st.cache_data
def cache(string: str):
    return st.session_state.get(string)
