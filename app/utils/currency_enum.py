#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import libraries
from enum import Enum, unique


@unique
class Currency(Enum):
    USD = "USD"  # United States Dollar
    EUR = "EUR"  # Euro
    GBP = "GBP"  # British Pound
    CNY = "CNY"  # Chinese Yuan
    HKD = "HKD"  # Hong Kong Dollar
