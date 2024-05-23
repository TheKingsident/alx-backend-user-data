#!/usr/bin/env python3
""" Module of Session Auth views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from api.v1.app import auth
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session():
    """ POST /auth_session/login
    """
    user_email = request.form.get("email")
    user_pwd = request.form.get("password")

    if user_email is None:
        return jsonify({"error": "email missing"}), 400
    if user_pwd is None:
        return jsonify({"error": "password missing"}), 400

    from models.user import User

    users = User.search({'email': user_email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    user = users[0]

    if not user.is_valid_password(user_pwd):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.auth.session_auth import SessionAuth

    session_auth = SessionAuth()
    session_id = session_auth.create_session(user.id)
    if session_id is None:
        return jsonify({"error": "unable to create session"}), 500

    response = make_response(jsonify(user.to_json()))
    response.set_cookie(os.getenv("SESSION_NAME"), session_id)

    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """ DELETE /auth_session/logout
    """
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
