#!/usr/bin/env python3
""" 0. Regex-ing
"""

import re



def filter_datum(fields, redaction, message, separator):
    """ filter_datum that returns the log message obfuscated"""
    value = message.split(separator)
    for field in fields:
        for i in range(len(value)):
            if value[i].startswith(field):
                subst = field + '=' + redaction
                value[i] = re.sub(value[i], '', value[i])
                value[i] = subst
    return separator.join(value)
