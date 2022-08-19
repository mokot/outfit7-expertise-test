#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import libraries
import sys
import analyze
import requests
import pandas as pd
from datetime import datetime
from ad_network import read_ad_network

# Import from utils
from utils.logger import get_logger
from utils.currency import read_currency
from utils.app_name_const import APP_NAME
from utils.revenue import convert_revenue
from utils.database import database_execute
from utils.date_format_const import DATE_FORMAT
from utils.date import is_date, convert_date, convert_date_data_frame


# Get app logger
logger_app = get_logger(APP_NAME)


# Constants
DAILY_REPORT_TABLE_NAME = "daily_report"


def save_daily_report(data, many=False):
    """
    Saves daily reports into the database.

    If many is True, then data is a list of lists. -> [(date, app, platform, ...), ...]
    If many is False, then data is a list. -> (date, app, platform, ...)

    @data: is a list or a list of lists (depending on the value of many) which
    contains the data to be saved
    @many: is a boolean which indicates if data is a list of lists or a list
    @return: True if the data was saved successfully, False otherwise
    """
    return database_execute(
        data=data,
        query="INSERT INTO {} (report_date, report_app, \
                report_platform, report_requests, report_impressions, \
                report_revenue, currency_usd_id, ad_network_id) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)".format(
            DAILY_REPORT_TABLE_NAME
        ),
        logger=logger_app,
        logger_message="Data was saved successfully",
        many=many,
    )


def read_daily_report(url):
    """
    Reads the data from the URL and returns it.

    @url: is the URL of the data to be read
    @return: a data frame of the data
    """
    try:
        # Get the data from URL
        response = requests.get(url)
        status_code = response.status_code
    except:
        logger_app.error("There was an error while reading the data from URL")
        return None

    # Check if the request was successful
    if not status_code == 200:
        logger_app.info("Google Storage request was unsuccessful")
        return None

    logger_app.info("Google Storage request was successful")
    data = response.text.splitlines()

    df_columns = data[0].split(",")
    df_rows = [report.split(",") for report in data[1:]]

    df = pd.DataFrame(df_rows, columns=df_columns)
    return df


def fix_daily_report(data, update=True):
    """
    Finds out the revenue currency and converts it
    to the USD. Function returns a data frame of the data, adding the revenue
    code as a new column.

    @url: is the URL of the data to be read
    @update: is a boolean which indicates if the data should be updated
    @return: a data frame of the data and the currency code
    """
    # Drop last row if it is not date type
    if not is_date(data.iloc[-1]["Date"]):
        data.drop(index=data.index[-1], axis=0, inplace=True)

    # Convert date to format: YYYY-MM-DD
    data = convert_date_data_frame(data)
    logger_app.info("Convert date to format: YYYY-MM-DD")

    # Convert revenue value to USD
    data, currency = convert_revenue(data, logger_app, update)
    logger_app.info("Convert revenue value to USD")

    return data, currency


def cluster_daily_report(data):
    """
    Clusters the data by app and platform.

    @data: is a data frame of the data
    @return: a data frame of the data
    """
    # Cluster by app and platform
    temp_data = data.groupby(["Date", "App", "Platform"]).sum()

    # Create a combination for each app and platform
    cluster_data = []
    for combination in temp_data.itertuples():
        cluster_data.append([*combination[0], *combination[1:]])
        
    try:
        # Convert data back to data frame
        data = pd.DataFrame(cluster_data, columns=data.keys())
        logger_app.info("Cluster by app and platform")
    except:
        logger_app.error("There was an error while clustering the data")
        return None

    return data


def daily_report(ad_network, date, logger=None, update=True, save=True):
    """
    Takes ad_network and date as input, creates a valid URL, reads the data from
    created URL, edits the data (converts date to format YYYY-MM-DD,
    converts revenue value to USD if possible), saves the data into the database
    and returns the data.

    @ad_network: is the name of the ad network to be retrieved
    @date: is the date to be retrieved
    @logger: is the logger object
    @update: is a boolean which indicates if the currency data should be updated
    @save: is a boolean which indicates if the data should be saved into the database
    @return: a data frame of the retrieved data
    """
    # Replace the logger if it is provided
    if logger:
        # Get app logger
        global logger_app
        logger_app = logger

    # If date is not a valid date, return None
    try:
        # Check if date is valid and check if it is in present or future
        if datetime.strptime(date, DATE_FORMAT).date() > datetime.now().date():
            logger_app.error("Date is not valid because it is in the future")
            return None
    except:
        logger_app.error("Date is not valid")
        return None

    # Get the ad network and date format
    ad_network = read_ad_network(ad_network)

    # Check if the ad_network was found
    if not ad_network or len(ad_network) != 3:
        logger_app.error("Ad Network does not exist")
        return None

    ad_network_id, url, date_format = ad_network
    date = convert_date(date, date_format)

    # Check if date or date format is valid
    if not date:
        logger_app.error("Date format is not valid")
        return None

    # Format the ad network URL for a specific date
    url = url.format(date)

    # Read the data from the URL
    data = read_daily_report(url)
    if data is None:
        logger_app.error("Data was not read from URL")
        return None

    # Don't save data and return it
    if not save:
        return data

    # Data analysis from problem 2 (ignore if data is not valid)
    data, _ = analyze.analyze(data)

    # Fix the data and prepare it to be saved
    data, currency = fix_daily_report(data, update)

    # Check if data exists
    if data is None:
        logger_app.error("There is no data for the given date")
        return None

    # Get the currency id
    currency_id = None
    if currency:
        currency_id = read_currency(currency)[0]

    # Cluster the data into groups of apps and platforms
    data = cluster_daily_report(data)

    # Check if the data is valid
    try:
        temp_data = data.copy()
        # Set new columns for data frame
        temp_data["currency"] = currency_id
        temp_data["ad_network"] = ad_network_id

        # Save data to the database
        save_daily_report(temp_data.to_numpy(), True)
    except:
        logger_app.error("Data is not valid")
        return None

    return data


if __name__ == "__main__":
    try:
        ad_network = sys.argv[1]
        date = sys.argv[2]
        # Check if the user wants to update the data
        update = False
        if len(sys.argv) == 4:
            update = sys.argv[3].lower() == "update" or sys.argv[3].lower() == "true"

        daily_report(ad_network, date, save=update)
    except:
        logger_app.info("Usage: python app.py <ad_network> <date> <save>")
        sys.exit(1)
