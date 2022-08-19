#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import libraries
import unittest
import pandas as pd
from utils.currency_enum import Currency
from utils.currency_const import (
    DEFAULT_EUR_USD,
    DEFAULT_GBP_USD,
    DEFAULT_CNY_USD,
    DEFAULT_HKD_USD,
)


# Import testing files
from utils.currency import (
    save_currency,
    update_currency,
    read_currency,
    get_exchange_rate_usd,
    CURRENCY_TABLE_NAME,
)
from utils.database import database_connect, database_execute
from utils.date import is_date, convert_date, convert_date_data_frame
from utils.logger import get_logger
from utils.revenue import update_revenue, convert_revenue
from ad_network import save_ad_network, read_ad_network, AD_NETWORK_TABLE_NAME
from daily_report import (
    save_daily_report,
    read_daily_report,
    daily_report,
    DAILY_REPORT_TABLE_NAME,
)


# Get test logger
logger_test = get_logger("Test")
logger_test.setLevel("CRITICAL")  # don't log anything


class Test(unittest.TestCase):
    # Tests the currency methods
    def test_currency(self):
        # Test the save_currency
        self.assertTrue(save_currency(("SIT", "1"), False))

        # Test the update_currency
        self.assertTrue(update_currency(Currency.USD, 1))

        # Test the read_currency
        result = read_currency(Currency.USD)
        self.assertTrue(result, (1, "2000-01-01"))

        result = read_currency(Currency.EUR)
        self.assertTrue(result[0], DEFAULT_EUR_USD)

        # Test the get_exchange_rate_usd
        # Test the USD/USD exchange rate
        exchange_rate = get_exchange_rate_usd(Currency.USD, logger_test)
        self.assertEqual(exchange_rate, 1)

        # Test the EUR/USD exchange rate
        exchange_rate = get_exchange_rate_usd(Currency.EUR, logger_test)
        self.assertAlmostEqual(exchange_rate, DEFAULT_EUR_USD, places=1)
        self.assertNotEqual(exchange_rate, 1)

        # Test the GBP/USD exchange rate
        exchange_rate = get_exchange_rate_usd(Currency.GBP, logger_test)
        self.assertAlmostEqual(exchange_rate, DEFAULT_GBP_USD, places=1)
        self.assertNotEqual(exchange_rate, 1)

        # Test the CNY/USD exchange rate
        exchange_rate = get_exchange_rate_usd(Currency.CNY, logger_test)
        self.assertAlmostEqual(exchange_rate, DEFAULT_CNY_USD, places=1)
        self.assertNotEqual(exchange_rate, 1)

        # Test the HKD/USD exchange rate
        exchange_rate = get_exchange_rate_usd(Currency.HKD, logger_test)
        self.assertAlmostEqual(exchange_rate, DEFAULT_HKD_USD, places=1)
        self.assertNotEqual(exchange_rate, 1)

        return

    # Tests the database methods
    def test_database(self):
        # Test the database_connect
        connection = database_connect()
        self.assertIsNotNone(connection)
        connection.close()

        # Test the database_execute
        # Insert into database
        data = [
            [1, "test", "test"],
            [2, "test", "test"],
            [3, "test", "test"],
        ]
        query = "INSERT INTO test (id, name, description) VALUES (%s, %s, %s)"
        result = database_execute(
            data, query, logger_test, "Test database execution", True
        )
        self.assertTrue(result)

        query = "SELECT * FROM test"
        result = database_execute(
            (), query, logger_test, "Test database execution", False
        )
        self.assertEqual(list(result), data[0])

        query = ""
        result = database_execute(
            (), query, logger_test, "Test database execution", False
        )
        self.assertFalse(result)

        return

    # Tests the date methods
    def test_date(self):
        # Test the is_date
        self.assertTrue(is_date("2022-01-01"))
        self.assertFalse(is_date("date"))

        # Test the convert_date
        self.assertEqual(convert_date("01/01/2022", "%Y-%m-%d"), "2022-01-01")
        self.assertIsNone(convert_date("date", "%Y-%m-%d"))

        # Test tje convert_date_data_frame
        data = convert_date_data_frame(
            pd.DataFrame(["01/01/2022", "01/01/2022", "01/01/2022"], columns=["Date"])
        )
        self.assertEqual(
            data["Date"].values.tolist(),
            ["2022-01-01", "2022-01-01", "2022-01-01"],
        )

        return

    # Tests the logger methods
    def test_logger(self):
        # Test the get_logger
        logger = get_logger("Test")
        self.assertIsNotNone(logger)

        return

    # Tests the revenue methods
    def test_revenue(self):
        # Test the update_revenue
        data = update_revenue(
            pd.DataFrame(["$1.74", "$0.85", "$1.54"], columns=["Revenue"]),
            Currency.USD,
            logger_test,
        )
        self.assertEqual(data.values.tolist(), [1.74, 0.85, 1.54])

        # Test the convert_revenue
        data, _ = convert_revenue(
            pd.DataFrame(["$1.74", "$0.85", "$1.54"], columns=["Revenue (usd)"]),
            logger_test,
        )
        self.assertEqual(data["Revenue"].values.tolist(), [1.74, 0.85, 1.54])

        return

    # Tests the add_network methods
    def test_ad_network(self):
        # Test the save_ad_network
        self.assertTrue(save_ad_network(("AdNetwork", "...", "%Y-%m-%d"), False))

        # Test the read_ad_network
        data = read_ad_network("AdNetwork")
        self.assertEqual(data, (None, "...", "%Y-%m-%d"))

        return

    # Test the daily_report methods
    def test_daily_report(self):
        # Test the save_daily_report
        self.assertTrue(
            save_daily_report(
                ("2017-09-15", "Talking Ginger", "iOS", 8934, 248, 1.74, 1, 1), False
            )
        )

        # Test the read_daily_report methods
        self.assertIsNone(read_daily_report("http://..."))
        self.assertIsNotNone(
            read_daily_report(
                "https://storage.googleapis.com/expertise-test/supernetwork/report/daily/2017-09-15.csv"
            )
        )

        # Test the daily_report
        self.assertIsNone(daily_report("...", "2017-09-15", logger_test))
        self.assertIsNone(daily_report("AdNetwork", "...", logger_test))
        self.assertIsNone(daily_report("AdNetwork", "2017-09-15", logger_test))
        self.assertIsNotNone(daily_report("SuperNetwork", "2017-09-15", logger_test))

        return


def create_duplicate_database(name, test_name):
    """
    Duplicates the database with the given name and renames it to the given test name.
    """
    database_execute(
        (),
        "ALTER TABLE {table_name} RENAME TO {test_table_name}; CREATE TABLE \
            {table_name} AS TABLE {test_table_name}".format(
            table_name=name, test_table_name=test_name
        ),
        logger_test,
        "Rename existing tables and create new ones",
        False,
    )

    return


def delete_duplicate_database(name, test_name):
    """
    Deletes the database with the given test name and renames it to the given name.
    """
    database_execute(
        (),
        "DROP TABLE {table_name}; ALTER TABLE {test_table_name} RENAME TO {table_name}".format(
            test_table_name=test_name, table_name=name
        ),
        logger_test,
        "Rename existing tables back and drop new ones",
        False,
    )

    return


if __name__ == "__main__":
    # Create a test table
    database_execute(
        (),
        "CREATE TABLE test (id INTEGER, name VARCHAR(255), description VARCHAR(255))",
        logger_test,
        "Create test table",
        False,
    )

    # Rename existing tables and create new tables
    create_duplicate_database(CURRENCY_TABLE_NAME, "test_currency_usd")
    create_duplicate_database(AD_NETWORK_TABLE_NAME, "test_ad_network")
    create_duplicate_database(DAILY_REPORT_TABLE_NAME, "test_daily_report")

    # Run tests (unittest.main() exits when tests are finished)
    unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(Test))

    # Rename back existing tables and drop new tables
    delete_duplicate_database(CURRENCY_TABLE_NAME, "test_currency_usd")
    delete_duplicate_database(AD_NETWORK_TABLE_NAME, "test_ad_network")
    delete_duplicate_database(DAILY_REPORT_TABLE_NAME, "test_daily_report")

    # Drop the test table
    database_execute(
        (),
        "DROP TABLE test",
        logger_test,
        "Drop test table",
        False,
    )
