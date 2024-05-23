#!/usr/bin/env python3
""" Module for Basic Authorization
"""

from api.v1.auth.auth import Auth
from uuid import uuid4


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
