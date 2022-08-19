#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import libraries
import daily_report
import pandas as pd
from utils.logger import get_logger
from utils.app_const import DEFAULT_APP
from utils.app_name_const import APP_NAME
from utils.platform_const import DEFAULT_PLATFORM


# Get analyze logger
logger_analyze = get_logger(APP_NAME)


# Constants
DEFAULT_DATE_FORMAT = "%d/%m/%Y"
DEFAULT_COLUMNS = ["Date", "App", "Platform", "Requests", "Impressions", "Revenue"]


def analyze_date(data):
    """
    Analyzes the date in data and returns the result.

    @data: is a data frame with a list of dates to be analyzed
    @return: True if the data is valid, False otherwise
    """
    # Check if all dates are the same
    if not (data["Date"] == data["Date"][0]).all():
        logger_analyze.warning("Dates are not the same")
        return False

    try:
        # Check if all dates are in the correct format (DD/MM/YYYY)
        pd.to_datetime(data["Date"], format=DEFAULT_DATE_FORMAT)
    except ValueError:
        logger_analyze.warning("Dates are not in the correct format")
        return False

    return True


def analyze_requests_impressions(data):
    """
    Analyzes the requests and impressions in data and returns the result.

    @data: is a data frame with the data to be analyzed
    @return: True if the data is valid, False otherwise and the corrected data
    """
    flag_data = True

    # Check if requests are numeric
    requests = pd.to_numeric(data["Requests"], errors="coerce").isna()

    if len(requests):
        logger_analyze.warning("Requests are not numeric")
        flag_data &= False

    # Remove requests with NaN
    data = data[~requests].reset_index(drop=True)

    # Check if impressions are numeric
    impressions = pd.to_numeric(data["Impressions"], errors="coerce").isna()

    if len(impressions):
        logger_analyze.warning("Impressions are not numeric")
        flag_data &= False

    # Remove impressions with NaN
    data = data[~impressions].reset_index(drop=True)

    # Update values of requests and impressions
    data["Requests"] = data["Requests"].astype(int)
    data["Impressions"] = data["Impressions"].astype(int)

    # Check if impressions are greater than requests
    if (data["Impressions"] > data["Requests"]).any():
        logger_analyze.warning("Impressions are greater than requests:")

        # Analyze which apps on which platforms have this problem
        data_problem = (
            data[data["Impressions"] > data["Requests"]][["App", "Platform"]]
            .drop_duplicates()
            .values.tolist()
        )
        for app, platform in data_problem:
            logger_analyze.warning(
                "Problem occurs in application {} ({})".format(app, platform)
            )

        # Remove all rows with impressions greater than requests (keep impressions is equal to requests)
        data = data[~(data["Impressions"] > data["Requests"])].reset_index(drop=True)

        return False, data

    return True, data


def analyze_app_platform(data):
    """
    Analyzes the app and platform in data and returns the result.

    @data: is a data frame with the data to be analyzed
    @return: True if the data is valid, False otherwise and the corrected data
    """
    flag_data = True
    drop_data = []
    # Check if app and platform is valid, if not, remove it
    for temp_data in data.itertuples():
        # [Index, Date, App, Platform, Requests, Impressions, Revenue]
        if not temp_data[2] in DEFAULT_APP:
            # Check if app is valid
            drop_data.append(temp_data[0])
        elif not temp_data[3] in DEFAULT_PLATFORM:
            # Check if platform is valid
            drop_data.append(temp_data[0])

    if len(drop_data):
        logger_analyze.warning("Data contains invalid apps and platforms")
        # Remove useless data
        data.drop(drop_data, inplace=True)
        flag_data = False

    return flag_data, data


def analyze(data):
    """
    Gets the data from URL and analyzes it and returns True if the data is
    valid, False otherwise. Function analyzes the column names, dates, requests
    and impressions, and revenue. Function also corrects the invalid data.

    @data: is a data frame with the data to be analyzed
    @return: corrected data and True if the data is valid, False otherwise
    """
    global logger_analyze
    logger_analyze = get_logger("Analyze")

    if data is None or not len(data):
        logger_analyze.error("Invalid daily report")
        return None, False

    flag_data = True  # a flag that indicates if the data is valid

    # Check if all columns are named correctly
    if not list(data.keys()[:-1]) == DEFAULT_COLUMNS[:-1]:
        logger_analyze.warning("Columns are not named correctly")
        try:
            # Rename columns
            data.rename(
                columns=dict(zip(list(data.keys()), DEFAULT_COLUMNS)), inplace=True
            )
        except:
            flag_data &= False

    # Check if last row is Totals
    temp_data = (data[data["Date"] != data["Date"][0]] == data.iloc[-1]).all(axis=1)
    if temp_data.all() and len(temp_data) == 1 and len(data) - 1 == temp_data.index[0]:
        logger_analyze.warning("Last row is Totals")
        # Remove last row
        data.drop(len(data) - 1, inplace=True)

    # Analyze date
    flag_data &= analyze_date(data)

    # Analyze requests and impressions
    temp_flag_data, temp_data = analyze_requests_impressions(data)
    flag_data &= temp_flag_data
    # Check if data is valid, than update it
    if temp_data is not None and len(temp_data):
        data = temp_data

    # Analyze app and platform
    temp_flag_data, data = analyze_app_platform(data)
    flag_data &= temp_flag_data

    # Check if revenue is positive
    if data[data.keys()[-1]].str.contains("-").any():
        logger_analyze.warning("Revenue is negative")
        flag_data &= False

    try:
        # Check if revenue is numeric
        pd.to_numeric(data[data.keys()[-1]])
        # Convert revenue to numeric, because we want to analyze it
        # Don't convert revenue to numeric, because we want to keep it as string
    except ValueError:
        logger_analyze.warning("Revenue is not numeric")
        # flag_data &= False # ignore revenue error, handled in utils.revenue

    return data, flag_data


if __name__ == "__main__":
    ad_networks = ["SuperNetwork", "AdUmbrella"]
    dates = ["2017-09-15", "2017-09-16"]

    for temp_ad_network in ad_networks:
        for temp_date in dates:
            data = daily_report.daily_report(
                temp_ad_network,
                temp_date,
                logger=logger_analyze,
                update=True,
                save=False,
            )
            _, temp_result = analyze(data)
            logger_analyze.info(
                "Daily report {} ({}) is {}".format(
                    temp_ad_network, temp_date, "valid" if temp_result else "invalid"
                )
            )
