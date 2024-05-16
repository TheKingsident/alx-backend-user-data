#!/usr/bin/env python3
"""  5. Encrypting passwords
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """ returns a salted, hashed password, which is a byte string
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed
