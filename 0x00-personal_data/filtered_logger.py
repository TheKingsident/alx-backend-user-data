#!/usr/bin/env python3
""" 0. Regex-ing
"""

import logging
import mysql.connector
import os
import re
from typing import List
from mysql.connector import Error

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
    """ returns a logging.Logger object
    """
    user_data_logger = logging.getLogger("user_data")
    user_data_logger.setLevel(logging.INFO)
    user_data_logger.propagate = False
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    user_data_logger.addHandler(stream_handler)

    return user_data_logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ returns a connector to the database
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    if not db_name:
        raise ValueError(
            "PERSONAL_DATA_DB_NAME environment variable is not set")

    return mysql.connector.connect(user=username,
                                   password=password,
                                   host=host,
                                   database=db_name)


def main():
    logger = get_logger()
    try:
        db_connection = get_db()
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        for row in rows:
            msg = "name={}; email={}; phone={}; ssn={}; password={};\
            ip={}; last_login={}; user_agent={}; ".format(
                row[0], row[1], row[2], row[3], row[4], row[5], row[6],
                row[7]
                )
            filtered_msg = filter_datum(list(PII_FIELDS), '***', msg, '; ')
            logger.info(filtered_msg)
    except Error as e:
        logger.error("Error connecting to the database: %s", e)
    finally:
        if 'db_connection' in locals() and db_connection.is_connected():
            cursor.close()
            db_connection.close()


if __name__ == "__main__":
    main()
