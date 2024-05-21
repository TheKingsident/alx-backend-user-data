#!/usr/bin/env python3
""" Module for Basic Authorization
"""

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Basic Authorization class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str
                                            ) -> str:
        """ extract_base64_authorization_header method
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[len("Basic "):]
