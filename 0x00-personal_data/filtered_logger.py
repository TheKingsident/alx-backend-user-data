#!/usr/bin/env python3
""" 0. Regex-ing
"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ filter_datum that returns the log message obfuscated"""
    return re.sub(r'(?:^|{})({})(?:$|{})'.format(
        separator, '|'.join(fields), separator), redaction, message)
