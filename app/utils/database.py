#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import libraries
import os
import psycopg2
from dotenv import load_dotenv


# Load the .env file
load_dotenv()

# Database
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_DB = os.getenv("DATABASE_DB")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")


def database_connect():
    """
    This function creates a connection to the database.

    @return: connection to PostgreSQL database
    """
    # Establishing the connection
    connection = psycopg2.connect(
        database=DATABASE_DB,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT,
    )

    # Setting auto commit false
    connection.autocommit = True
    return connection


def database_execute(data, query, logger, logger_message, many=False):
    """
    Executes a query on the database and returns the result.

    @data: data to be used in the query (list or a list of lists)
    @query: query to be executed (string)
    @logger: logger object
    @logger_message: message to be logged
    @many: is a boolean which indicates if data is a list of lists or a list
    @return: result of the query (boolean, list or a list of lists)
    """
    try:
        # Create a PostgreSQL connection
        connection = database_connect()

        # Creating a cursor object using the cursor() method
        cursor = connection.cursor()

        # Executing the SQL query
        cursor.executemany(
            query,
            data,
        ) if many else cursor.execute(query, data)

        try:
            # Fetch the results from the database
            result = cursor.fetchmany() if many else cursor.fetchone()
        except (Exception, psycopg2.DatabaseError) as error:
            result = True

        # Close open connections
        cursor.close()
        connection.close()

        logger.info(logger_message)
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        # Print the error message
        logger.error(error)
        return False
    finally:
        # Close the connection to the database if it is open
        if connection is not None:
            connection.close()
