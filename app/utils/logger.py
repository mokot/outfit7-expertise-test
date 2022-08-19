#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import libraries
import logging


def get_logger(logger_name):
    """
    Configures the logger and returns it.

    @logger_name: name of the logger
    @return: a logger object
    """
    # Config logger
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - {}: %(message)s".format(logger_name),
        level=logging.INFO,
        datefmt="%d-%b-%y %H:%M:%S",
    )

    logger = logging.getLogger()
    return logger
