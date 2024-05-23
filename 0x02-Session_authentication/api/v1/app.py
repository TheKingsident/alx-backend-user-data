#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error):
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


def get_auth_instance():
    """ get_auth_instance support method
    """
    auth_type = getenv("AUTH_TYPE")
    if auth_type:
        if auth_type == 'auth':
            auth_module = __import__(f"api.v1.auth.{auth_type}",
                                     fromlist=[f"{auth_type}"])
            return auth_module.Auth()
        elif auth_type == "basic_auth":
            basic_auth_module = __import__(f"api.v1.auth.{auth_type}",
                                           fromlist=[f"{auth_type}"])
            return basic_auth_module.BasicAuth()
        elif auth_type == 'session_auth':
            session_auth_module = __import__(f"api.v1.auth.{auth_type}",
                                             fromlist=[f"{auth_type}"])
            return session_auth_module.SessionAuth()
        elif auth_type == 'session_exp_auth':
            session_auth_module = __import__(f"api.v1.auth.{auth_type}",
                                             fromlist=[f"{auth_type}"])
            return session_auth_module.SessionExpAuth()
    return None


auth = get_auth_instance()


@app.before_request
def before_request():
    """ before_request method
    """
    if auth is None:
        return

    excluded_paths = ["/api/v1/status/",
                      "/api/v1/unauthorized/",
                      "/api/v1/forbidden/",
                      "/api/v1/auth_session/login/"
                      ]

    if not auth.require_auth(request.path, excluded_paths):
        return

    auth_header = auth.authorization_header(request)
    if auth_header is None and auth.session_cookie(request) is None:
        abort(401)

    if not auth.current_user(request):
        abort(403)

    request.current_user = auth.current_user(request)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    auth_type = getenv("AUTH_TYPE")
    app.run(host=host, port=port, debug=True)
