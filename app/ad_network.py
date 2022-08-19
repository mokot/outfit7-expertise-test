#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import libraries
from utils.logger import get_logger
from utils.app_name_const import APP_NAME
from utils.database import database_execute


# Get app logger
logger_app = get_logger(APP_NAME)


# Constants
AD_NETWORK_TABLE_NAME = "ad_network"


def save_ad_network(data, many=False):
    """
    Saves the Ad Network data into the database.

    If many is True, then data is a list of lists. -> [(name, url, date), ...]
    If many is False, then data is a list. -> (name, url, date)

    @data: is a list or a list of lists (depending on the value of many) which
    contains the data to be saved
    @many: is a boolean which indicates if data is a list of lists or a list
    @return: True if the data was saved successfully, False otherwise
    """
    return database_execute(
        data=data,
        query="INSERT INTO {} (ad_network_name, ad_network_url, ad_network_date_format) \
                VALUES (%s, %s, %s)".format(
            AD_NETWORK_TABLE_NAME
        ),
        logger=logger_app,
        logger_message="Data was saved successfully",
        many=many,
    )


def read_ad_network(ad_network_name):
    """
    Reads the Ad Network URL and date format from database.

    @network_name: is the name of the network to be retrieved
    @return: a tuple of the id, URL and date format
    """
    return database_execute(
        data=(ad_network_name,),
        query="SELECT ad_network_id, ad_network_url, ad_network_date_format FROM \
            {} WHERE ad_network_name = %s".format(
            AD_NETWORK_TABLE_NAME
        ),
        logger=logger_app,
        logger_message="Data was retrieved from database",
        many=False,
    )
