#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import libraries
from utils.app_name_const import APP_NAME
from utils.logger import get_logger
from daily_report import daily_report


# Get app logger
logger_app = get_logger(APP_NAME)


def read_main():
    """
    Reads the input from the user.
    """
    try:
        data = input("::: ")
        return data
    except EOFError:
        print("")
        return ""


def exit_main(code):
    """
    Return a boolean value to indicate if the program should exit.

    @code: is the exit code of the program
    @return: True if the program should exit, False otherwise
    """
    if code == "" or code == " " or code == "q" or code == "quit":
        logger_app.info("Exiting program")
        return True

    return False


def main():
    """
    Main function of the application. It reads the input from the user and
    saves the data into the database.
    """
    # Start the application
    logger_app.info("Starting Apps7 Data Engineer Application ...")
    logger_app.info("If you want to exit, press 'q'")

    confirmation_flag = True  # this flag is used to confirm the input
    while True:
        if confirmation_flag:
            # Read the Ad Network data
            logger_app.info("Enter the Ad Network:")
            ad_network = read_main()
            # Check if the input is exit
            if exit_main(ad_network):
                break
            logger_app.info("Ad Network: {}".format(ad_network))

            # Read the date
            logger_app.info("Enter the Date:")
            date = read_main()
            # Check if the input is exit
            if exit_main(date):
                break
            logger_app.info("Date: {}".format(date))

            # Read the date update option
            logger_app.info("Would you like to update exchange currency rate? (y/n)")
            update = read_main().lower()
            # Check if the input is exit
            if exit_main(update):
                break
            update = update == "y" or update == "yes"

            # Read the date save option
            logger_app.info("Would you like to save daily report? (y/n)")
            save = read_main().lower()
            # Check if the input is exit
            if exit_main(save):
                break
            save = save == "y" or save == "yes"

        # Confirm user's input
        logger_app.info('Confirm your choices of data with "yes" or "no": (y/n)')
        confirmation = read_main().lower()
        # Check if the input is exit
        if exit_main(confirmation):
            break
        elif confirmation == "y" or confirmation == "yes":
            # Execute the app function
            confirmation_flag = True
            logger_app.info("Starting the program ...")
            try:
                data = daily_report(ad_network, date, logger_app, update, save)
            except:
                data = None
            if data is not None and len(data):
                logger_app.info("Program has finished successfully")
            else:
                logger_app.info("Program has finished unsuccessfully")

            logger_app.info("Press any key to continue ...")
            key = read_main()
            # Check if the input is exit
            if key == "q" or key == "quit":
                break
        elif confirmation == "n" or confirmation == "no":
            # Repeat the process again
            confirmation_flag = True
        else:
            # Invalid input
            confirmation_flag = False
            logger_app.info("Invalid input")

    # Stop the application
    logger_app.info("Stopping Apps7 Data Engineer Application ...")

    return


if __name__ == "__main__":
    main()
