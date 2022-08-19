#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import libraries
from utils.logger import get_logger
from ad_network import save_ad_network
from utils.currency import save_currency
from utils.app_name_const import APP_NAME
from utils.currency_const import (
    DEFAULT_EUR_USD,
    DEFAULT_GBP_USD,
    DEFAULT_CNY_USD,
    DEFAULT_HKD_USD,
)


# Get app logger
logger_app = get_logger(APP_NAME)

# Constants
SEED_CURRENCY_DATA = [
    ("USD", 1),
    ("EUR", DEFAULT_EUR_USD),
    ("GBP", DEFAULT_GBP_USD),
    ("CNY", DEFAULT_CNY_USD),
    ("HKD", DEFAULT_HKD_USD),
]
SEED_AD_NETWORK_DATA = [
    (
        "SuperNetwork",
        "https://storage.googleapis.com/expertise-test/supernetwork/report/daily/{}.csv",
        "%Y-%m-%d",
    ),
    (
        "AdUmbrella",
        "https://storage.googleapis.com/expertise-test/reporting/adumbrella/adumbrella-{}.csv",
        "%-d_%-m_%Y",
    ),
]


def seed():
    """
    Seed the database with data.
    """
    logger_app.info("Seeding the database ...")
    currency = save_currency(data=SEED_CURRENCY_DATA, many=True)
    ad_network = save_ad_network(data=SEED_AD_NETWORK_DATA, many=True)

    # Check if seeding was successful
    if currency and ad_network:
        logger_app.info("Seeding the database was successful")
    else:
        logger_app.info("Seeding the database was unsuccessful")

    return


if __name__ == "__main__":
    seed()
