#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import libraries
import os
import json
import requests
import datetime
from dotenv import load_dotenv
from utils.logger import get_logger
from utils.app_name_const import APP_NAME
from utils.database import database_execute
from utils.date_format_const import DATE_FORMAT


# Get app logger
logger_app = get_logger(APP_NAME)


# Load the .env file
load_dotenv()

# APILayer api key
APILAYER_API_KEY = os.getenv("APILAYER_API_KEY")

# Constants
CURRENCY_TABLE_NAME = "currency_usd"
APILAYER_API_URL = (
    "https://api.apilayer.com/exchangerates_data/convert?to={}&from={}&amount={}"
)


def save_currency(data, many=False):
    """
    Saves the currency usd exchange rate into the database.

    If many is True, then data is a list of lists. -> [(name, url, date), ...]
    If many is False, then data is a list. -> (name, url, date)

    @data: is a list or a list of lists (depending on the value of many) which
    contains the data to be saved
    @many: is a boolean which indicates if data is a list of lists or a list
    @return: True if the data was saved successfully, False otherwise
    """
    return database_execute(
        data=data,
        query="INSERT INTO {} (currency_usd_name, currency_usd_value) \
                VALUES (%s, %s)".format(
            CURRENCY_TABLE_NAME
        ),
        logger=logger_app,
        logger_message="Data was saved successfully",
        many=many,
    )


def update_currency(currency, value):
    """
    Updates the currency exchange rate and date in database.

    @currency: is a Currency enum which indicates the currency to be updated
    @value: is the value of the currency exchange rate
    @return: True if the data was updated successfully, False otherwise
    """
    return database_execute(
        data=(value,),
        query="UPDATE {} SET currency_usd_value=%s, \
                currency_usd_updated_at = NOW() \
                WHERE currency_usd_name = '{}'".format(
            CURRENCY_TABLE_NAME, currency.value
        ),
        logger=logger_app,
        logger_message="Data was updated successfully",
        many=False,
    )


def read_currency(currency):
    """
    Reads the USD currency exchange rate from database.

    @currency: is the name of the currency
    @return: a tuple with the id, value of the currency exchange rate and the date
    """
    currency = database_execute(
        data=(currency.value,),
        query="SELECT currency_usd_id, currency_usd_value, currency_usd_updated_at FROM \
            {} WHERE currency_usd_name = %s".format(
            CURRENCY_TABLE_NAME
        ),
        logger=logger_app,
        logger_message="Data was retrieved from database",
        many=False,
    )

    if not currency or len(currency) != 3:
        logger_app.warning("The currency is not supported")
        return 1, datetime.datetime(2000, 1, 1).date().strftime(DATE_FORMAT)

    return currency[0], float(currency[1]), currency[2].date().strftime(DATE_FORMAT)


def get_exchange_rate_usd(currency, logger, update=True):
    """
    Gets the value of the currency/USD exchange rate from the APILayer API.

    @currency: is a Currency enum which indicates the currency to be converted
    @logger: is the logger object
    @update: is a boolean which indicates if the exchange rate should be updated
    @return: the value of the currency/USD exchange rate
    """
    # Get the currency/USD exchange rate and date from database
    _, result, date = read_currency(currency)

    # Check if currency/USD exchange rate is not to old (1 week)
    currency_date = datetime.datetime.strptime(date, DATE_FORMAT).date()
    week_date = (
        datetime.datetime.now() - datetime.timedelta(days=7)
    ).date()  # 1 week ago

    # If the currency/USD exchange rate is not to old, return the value
    if not week_date > currency_date or not update:
        return result

    headers = {"apikey": APILAYER_API_KEY}

    # Convert amount from EUR to USD
    response = requests.request(
        "GET", APILAYER_API_URL.format("USD", currency.value, 1), headers=headers
    )

    status_code = response.status_code

    # Check if the request was successful
    if status_code == 200:
        logger.info("APILayer request was successful")
        result = float(json.loads(response.text)["result"])

        # Update the currency/USD exchange rate and date
        if update_currency(currency, result):
            logger.info("Currency exchange rate was updated")

    return result
