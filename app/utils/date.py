#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import libraries
from dateutil.parser import parse
from utils.date_format_const import DATE_FORMAT


def is_date(date):
    """
    Checks if a string is a valid date.

    @date: string to be checked
    @return: True if date is valid, False otherwise
    """
    try:
        parse(date)
        return True
    except ValueError:
        return False


def convert_date(date, date_format):
    """
    Converts a date to a specific format.

    @date: date to be converted to a specific format
    @date_format: format to convert the date to
    @return: date in the specified format
    """
    try:
        return parse(date).strftime(date_format)
    except ValueError:
        return None


def convert_date_data_frame(data):
    """
    Converts the date in data frame column to a YYYY-MM-DD format.

    @data: is a data frame containing the data to be converted
    @return: a data frame with the converted date
    """
    data["Date"] = [
        convert_date(date, DATE_FORMAT) if convert_date(date, DATE_FORMAT) else ""
        for date in data["Date"]
    ]
    return data
