#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import libraries
import os
import json
import socketserver
import pandas as pd
from dotenv import load_dotenv
from utils.logger import get_logger
from daily_report import daily_report
from utils.app_name_const import APP_NAME
from http.server import BaseHTTPRequestHandler


# Get app logger
logger_app = get_logger(APP_NAME)

# Load the .env file
load_dotenv()

# Database
SERVER = os.getenv("SERVER")
SERVER_PORT = int(os.getenv("SERVER_PORT"))


class Server(BaseHTTPRequestHandler):
    def _set_response(self):
        """
        Sets the response to the request and returns the filename of HTML file.
        """
        # Combine a absolute path for the file
        root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
        filename = root + "/index.html"

        self.send_response(200)  # send response code
        if filename[-4:] == ".css":
            # Check if the file is a CSS file
            self.send_header("Content-type", "text/css")
        elif filename[-5:] == ".json":
            # Check if the file is a JSON file
            self.send_header("Content-type", "application/json")
        elif filename[-3:] == ".js":
            # Check if the file is a JS file
            self.send_header("Content-type", "application/javascript")
        elif filename[-4:] == ".ico":
            # Check if the file is an ICO file
            self.send_header("Content-type", "image/x-icon")
        else:
            # Check if the file is a HTML file
            self.send_header("Content-type", "text/html")
        self.end_headers()

        return filename

    def do_GET(self):
        """
        Returns the HTML file.
        """
        # Set the response
        filename = self._set_response()

        with open(filename, "rb") as file:
            # Read the file and replace the address
            html_file = (
                file.read()
                .decode("utf-8")
                .replace("SERVER_ADDRESS", "http://{}:{}".format(SERVER, SERVER_PORT))
                .encode("utf-8")
            )
            self.wfile.write(html_file)

        return

    def do_POST(self):
        """
        Handles the POST request and returns the HTML file.
        """
        content_length = int(
            self.headers["Content-Length"]
        )  # get the length of the data
        post_data = self.rfile.read(content_length)  # get data

        # Check if it is a api request or a html request
        if self.path == "/api":
            # Api request
            self.send_response(200)  # send response code
            self.send_header("Content-type", "application/json")  # send header
            self.end_headers()

            post_data = json.loads(post_data.decode("utf-8"))

            try:
                # Call the daily report function
                data = daily_report(
                    post_data["ad_network"], post_data["date"], logger_app, True, True
                )
                # Convert data to json
                data = data.to_json(orient="table")
            except:
                # If the function fails, return an error json
                data = json.dumps({"error": "Error"})

            # Return the data
            self.wfile.write(data.encode("utf-8"))

        else:
            # HTML request
            post_data = post_data.decode("utf-8").split("&")

            # Cal the daily report function
            data = daily_report(
                post_data[0].split("=")[-1],
                post_data[1].split("=")[-1],
                logger_app,
                True,
                True,
            )

            response_status = '<i class="fa-solid fa-xmark"></i>'
            if data is not None and len(data):
                response_status = '<i class="fa-solid fa-check"></i>'

            # Set the response
            filename = self._set_response()
            with open(filename, "rb") as file:
                # Read the file and replace the address
                html_file = (
                    file.read()
                    .decode("utf-8")
                    .replace(
                        "SERVER_ADDRESS", "http://{}:{}".format(SERVER, SERVER_PORT)
                    )
                    .replace("form { height: 470px; }", "form { height: 520px; }")
                    .replace(
                        '<div class="output"></div>',
                        '<div class="output"><div>Status:</div><div id="status">{}</div></div>'.format(
                            response_status
                        ),
                    )
                    .encode("utf-8")
                )
                self.wfile.write(html_file)

        return


if __name__ == "__main__":
    # Create an object of the Server class
    Handler = Server

    # Create a server
    server = socketserver.TCPServer((SERVER, SERVER_PORT), Handler)
    logger_app.info("Server started http://%s:%s" % (SERVER, SERVER_PORT))

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger_app.info("Stopping server ...")
    except Exception as error:
        logger_app.error("Error: %s" % error)
    finally:
        server.shutdown()
        server.server_close()
        logger_app.info("Server stopped")
