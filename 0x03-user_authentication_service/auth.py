#!/usr/bin/env python3
"""Auth module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hashes a password and returns the hashed password as bytes

    Args:
        password (str): The password to hash

    Returns:
        bytes: The salted and hashed password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
