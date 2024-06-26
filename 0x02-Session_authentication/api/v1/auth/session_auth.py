#!/usr/bin/env python3
""" Module for Session Authorization
"""

from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """ Session Authentication class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session ID for a user_id

        Args:
            user_id (str): The user ID for which the session ID is created

        Returns:
            str: The created session ID, or None if user_id is invalid
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid4())
        self.__class__.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a user ID based on a session ID

        Args:
            session_id (str): The session ID

        Returns:
            str: The user ID associated with the session ID, or None if invalid
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.__class__.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ current_user method
        """
        if request is None:
            return None
        session_id = self.session_cookie(request)
        if session_id is None:
            return None
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None
        return User.get(user_id)

    def destroy_session(self, request=None):
        """ destroy_session method
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_by_session_id[session_id]
        if user_id is None:
            return False

        del self.user_id_by_session_id[session_id]
        return True
