#!/usr/bin/env python3
"""Flask App module
"""

from flask import Flask, jsonify, request, abort, make_response
from flask import redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def welcome():
    """Return a JSON payload with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """Register a new user.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """User login
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if AUTH.valid_login(email=email, password=password) is False:
        abort(401)
    session_id = AUTH.create_session(email)
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)

    return response


@app.route('/sessions', methods=['DELETE'])
def logout():
    """Logs the user out
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id=session_id)
    if user is None:
        return abort(403)

    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route('/profile', methods=['GET'])
def profile():
    """Profile route
    """
    session_id = request.cookies.get("session_id")
    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id=session_id)
    if user is None:
        abort(403)

    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'])
def reset_password():
    """Handles the generation of reset password token
    """
    email = request.form.get("email")

    if not email:
        abort(400)

    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token})
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """Handles the update of user's password
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify(
            {"email": email, "message": "Password updated"}
            ), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
