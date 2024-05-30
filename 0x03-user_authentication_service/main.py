#!/usr/bin/env python3
"""
main.py

This module contains functions that interact with a Flask web server to perform
various user authentication operations such as registering users, logging in,
checking profiles, logging out, and resetting passwords. Each function uses the
requests module to query the server and validates the responses using
assertions.

Functions:
    register_user(email: str, password: str) -> None
    log_in_wrong_password(email: str, password: str) -> None
    log_in(email: str, password: str) -> str
    profile_unlogged() -> None
    profile_logged(session_id: str) -> None
    log_out(session_id: str) -> None
    reset_password_token(email: str) -> str
    update_password(email: str, reset_token: str, new_password: str) -> None
"""

import requests

BASE_URL = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """
    Registers a new user.

    Sends a POST request to the /users endpoint with email and password as form
    data.

    Asserts that the response status code is 200 and the JSON payload matches:
    {"email": email, "message": "user created"}

    Args:
        email (str): The user's email address.
        password (str): The user's password.
    """
    response = requests.post(f"{BASE_URL}/users",
                             data={"email": email, "password": password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Attempts to log in with an incorrect password.

    Sends a POST request to the /sessions endpoint with email and wrong
    password as form data.

    Asserts that the response status code is 401.

    Args:
        email (str): The user's email address.
        password (str): The incorrect password.
    """
    response = requests.post(f"{BASE_URL}/sessions",
                             data={"email": email, "password": password})
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Logs in a user with the correct password.

    Sends a POST request to the /sessions endpoint with email and password as
    form data.

    Asserts that the response status code is 200 and the JSON payload matches:
    {"email": email, "message": "logged in"}

    Returns the session ID from the response cookies.

    Args:
        email (str): The user's email address.
        password (str): The user's password.

    Returns:
        str: The session ID.
    """
    response = requests.post(f"{BASE_URL}/sessions",
                             data={"email": email, "password": password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """
    Attempts to access the profile without being logged in.

    Sends a GET request to the /profile endpoint.

    Asserts that the response status code is 403.
    """
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Accesses the profile while logged in.

    Sends a GET request to the /profile endpoint with the session ID as a
    cookie.

    Asserts that the response status code is 200 and the response JSON contains
    the email field.

    Args:
        session_id (str): The session ID of the logged-in user.
    """
    response = requests.get(f"{BASE_URL}/profile",
                            cookies={"session_id": session_id})
    assert response.status_code == 200
    assert "email" in response.json()


def log_out(session_id: str) -> None:
    """
    Logs out a user.

    Sends a DELETE request to the /sessions endpoint with the session ID as a
    cookie.

    Asserts that the response status code is 200.

    Args:
        session_id (str): The session ID of the logged-in user.
    """
    response = requests.delete(f"{BASE_URL}/sessions",
                               cookies={"session_id": session_id})
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """
    Requests a password reset token.

    Sends a POST request to the /reset_password endpoint with email as form
    data.

    Asserts that the response status code is 200.

    Returns the reset token from the response JSON.

    Args:
        email (str): The user's email address.

    Returns:
        str: The reset token.
    """
    response = requests.post(f"{BASE_URL}/reset_password",
                             data={"email": email})
    assert response.status_code == 200
    return response.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Updates the user's password using a reset token.

    Sends a PUT request to the /reset_password endpoint with email,
    reset token, and new password as form data.

    Asserts that the response status code is 200 and the JSON payload matches:
    {"email": email, "message": "Password updated successfully"}

    Args:
        email (str): The user's email address.
        reset_token (str): The password reset token.
        new_password (str): The new password.
    """
    response = requests.put(f"{BASE_URL}/reset_password", data={
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    })
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
