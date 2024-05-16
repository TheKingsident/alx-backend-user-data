#!/usr/bin/env python3
""" 0. Regex-ing
"""

import csv
import re
import logging
from typing import List

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Initialization
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ format method
        """
        message = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            message, self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ filter_datum that returns the log message obfuscated"""
    value = message.split(separator)

    for field in fields:
        for i in range(len(value)):
            if value[i].startswith(field):
                subst = field + '=' + redaction
                value[i] = re.sub(value[i], '', value[i])
                value[i] = subst
    return separator.join(value)

def get_logger() -> logging.Logger:
    user_data_logger = logging.getLogger("user_data")
    user_data_logger.setLevel(logging.INFO)
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    user_data_logger.addHandler(stream_handler)

    return user_data_logger