#!/usr/bin/env python3
""" Module for Authorization
"""

from flask import request
from typing import List, TypeVar
import fnmatch
import os


class Auth:
    """ Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require_auth method
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        path = path.rstrip('/') + '/'

        for excluded_path in excluded_paths:
            excluded_path = excluded_path.rstrip('/') + '/'
            if fnmatch.fnmatch(path, excluded_path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ authorization_header method
        """
        if request is None:
            None
        if 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ current_user method
        """
        return None

    def session_cookie(self, request=None):
        """ session_cookie method
        """
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME', '_my_session_id')
        return request.cookies.get(session_name)
