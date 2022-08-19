#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import libraries
from utils.currency_enum import Currency
from utils.currency import get_exchange_rate_usd


def update_revenue(data, currency, logger, update=True):
    """
    Converts the revenue value from currency to USD.

    @data: is a data frame containing the data to be converted
    @currency: is a Currency enum which indicates the currency to be converted
    @logger: is the logger object
    @update: is a boolean to indicate if the data should be updated or not
    @return: a data frame with the converted revenue
    """
    return (
        data[data.keys()[-1]]
        .str.replace("[^0-9|.]", "", regex=True)
        .astype(float)
        .multiply(
            get_exchange_rate_usd(currency=currency, logger=logger, update=update)
        )
        .round(2)
    )


def convert_revenue(data, logger, update=True):
    """
    Converts the revenue value from currency to USD.
    Currently supported currencies are: USD, EUR, GBP, CNY, HKD (locations where
    company Apps7 is located)

    @data: is a data frame containing the data, where Revenue columns will be
    converted to USD and the currency code will be stored in the last column
    (default data columns are: Date, App, Platform, Requests, Impressions, Revenue)
    @logger: is the logger object
    @return: a data frame with the converted revenue and the currency code
    """
    # Flag to indicate if the report revenue is in USD currency
    currency = None

    # If revenue is in USD, don't convert it
    if data[data.keys()[-1]].str.contains("\$").any() or "(usd)" in data.keys()[-1]:
        currency = Currency.USD
        # Remove any unusual USD symbols
        data[data.keys()[-1]] = update_revenue(data, Currency.USD, logger, update)

    # If revenue is in EUR, convert it to USD
    elif data[data.keys()[-1]].str.contains("\€").any() or "(eur)" in data.keys()[-1]:
        currency = Currency.USD
        # Remove any unusual EUR symbols and convert to USD
        data[data.keys()[-1]] = update_revenue(data, Currency.EUR, logger, update)

    # If revenue is in GBP, convert it to USD
    elif data[data.keys()[-1]].str.contains("\£").any() or "(gbp)" in data.keys()[-1]:
        currency = Currency.USD
        # Remove any unusual GBP symbols and convert to USD
        data[data.keys()[-1]] = update_revenue(data, Currency.GBP, logger, update)

    # If revenue is in CNY, convert it to USD
    elif data[data.keys()[-1]].str.contains("\¥").any() or "(cny)" in data.keys()[-1]:
        currency = Currency.USD
        # Remove any unusual CNY symbols and convert to USD
        data[data.keys()[-1]] = update_revenue(data, Currency.CNY, logger, update)

    # If revenue is in HKD, convert it to USD
    elif data[data.keys()[-1]].str.contains("HK\$").any() or "(hkd)" in data.keys()[-1]:
        currency = Currency.USD
        # Remove any unusual HKD symbols and convert to USD
        data[data.keys()[-1]] = update_revenue(data, Currency.HKD, logger, update)

    # Rename columns to Revenue
    data.rename(columns={data.keys()[-1]: "Revenue"}, inplace=True)

    return data, currency
