#!/usr/bin/env python3
""" 0. Regex-ing
"""

import re


def filter_datum(fields, redaction, message, separator):
    """ filter_datum that returns the log message obfuscated"""
    return re.sub(r'(?:^|{})({})(?:$|{})'.format(
        separator, '|'.join(fields), separator), redaction, message)
