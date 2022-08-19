<p align="center">
  <a href="https://outfit7.com/" target="blank"><img src="./docs/images/outfit7_logo.png" 
  width="420" alt="Outfit7 Logo" /></a>
</p>
  
<p align="center">
  Documentation about Apps7 project. This documentation covers the deployment of
  the Apps7 application and all of its needed components. <br />
  <i>This project is an expertise test for the data engineer position at Outfit7.</i>
</p>

### Table of Contents

- [About](#about-the-project)
  - [Used Technologies](#used-technologies)
    - [Python](#1-python)
    - [Docker](#2-docker)
    - [Docker Compose](#3-docker-compose)
    - [PostgreSQL](#4-postgresql)
  - [Database Structure](#database-structure)
  - [Analyzing Data](#analyzing-data)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [How to use Application?](#how-to-use-application)
    - [Command Line Interface (CLI)](#1-command-line-interface-cli)
    - [Web Application](#2-web-application)
    - [Script Application](#3-script-application)
  - [Testing](#testing)
  - [Analysis](#analysis)
  - [Cleanup](#cleanup)
  - [Local Installation](#local-installation)
- [Contributing](#contributing)
- [License](#license)
- [Authors](#authors)
- [Gallery](#gallery)
- [Instructions](./docs/instructions.md)
- [Answers](./docs/answers.md)

# About The Project

The project was created as an expertise test for the data engineer position at
Outfit7 (Slovenian subsidiary Ekipa2 d.o.o.).

The main functionality of the Apps7 application is to take Ad Network and date as
input parameters and retrieve each report for these input parameters from URLs
provided in from the user (or in our case instructions) and store it in a database.

All data reported by Ad Networks is stored in a uniform way in a database so that
data can later be used for various analytical purposes.

Application is currently interested in ad performance, so each Ad Network
provides us with daily reports which come in the form of CSV files. Each report
contains the following data: `Date`, `App`, `Platform`, `Requests`, `Impressions`,
and `Revenue`.

## Used Technologies

In general, the development of the Apps7 application is consisted of one main
technology i.e. [Python](https://www.python.org/) programming language. We have
also used [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)
for containerization, and [PostgresSQL](https://www.postgresql.org/) as database.

### 1. Python

Python is an interpreted, object-oriented, high-level programming language with
dynamic semantics. Its high-level built-in data structures, combined with
dynamic typing and dynamic binding, make it very attractive for Rapid Application
Development, as well as for use as a scripting or glue language to connect
existing components together. Python's simple, easy-to-learn syntax emphasizes
readability and therefore reduces the cost of program maintenance. Python
supports modules and packages, which encourages program modularity and code
reuse. The Python interpreter and the extensive standard library are available
in source or binary form without charge for all major platforms and can be
freely distributed.

Most of the Apps7 application is written in the Python programming language.

### 2. Docker

Docker is an open platform, for shipping, and running applications. Docker enables us
to separate our applications from our infrastructure, which means we can deliver
software quickly. With Docker, we can manage our infrastructure in the same ways
we manage our applications.

Every component needed to run the Apps7 application can be run inside Docker
containers.

### 3. Docker Compose

Docker Compose is a tool that was developed to help define and share multi-container
applications. With Compose, we can create a YAML file to define the services and
with a single command, can spin everything up or tear it all down.

`docker-compose` is used to run all of the needed components in a container with
simple rules in YAML files.

### 4. PostgreSQL

PostgreSQL is a powerful, open source object-relational database system with
over 30 years of active development that has earned it a strong reputation for
reliability, feature robustness, and performance.

## Database Structure

The database of the application consists of three tables, namely the main table
where the daily reports are stored: `daily_report`, the table where the
Ad Networks are stored: `ad_network`, and the table where the used currency
conversions to USD are stored `currency_usd`.

The `ad_network` table serves us to enter new Ad Networks and then make it
easier to use only these.

Due to the ever-increasing inflation in the past months and the resulting
fluctuations in currency conversion, we decided to convert all data into USD.
The mobile application company Apps7 is located in six different cities, namely
Ljubljana, London, Barcelona, Limassol, Hong Kong, and Beijing. Precisely
because most cities use different currencies, we decided to convert all daily
reports into a single currency, namely **USD**. The application, therefore,
enables the conversion of currencies: **EUR**, **BGP**, **CNY**, and **HKD** to
USD. On the following [link](https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=EUR),
we can see an ever-increasing fluctuation between e.g. EUR and USD, which means
that we cannot accurately determine a fixed rate for converting Revenue from one
currency to another. The application every week checks how much the conversion
amount has changed and then updates it in the database, which enables a more
accurate conversion of currencies into USD.

In the `daily_report` table, we store all the data about the reports that we
created above. We also added a column for the report's unique identifier,
the abbreviation of the currency in which the profit is (if the report contains
Revenue in an unsupported currency), and the date the report was entered into the
database, which enables us to better track the application's work in the database.

More about the composition of the database and its components can be found in
the following file: [database.sql](./database/init_database.sql).

At this point, we would like to mention that we have hardcoded the names of
Apps7 applications and the existing platforms that these applications support.
This could be done better with new tables in the database and programs that
enable CRUD operations on these tables.

## Analyzing Data

During the data analysis, we found that potential errors can occur in several
places. The requirements that we asked in our "sanity check" for the daily
report to be acceptable for storage in the database are:

- the date must be of type string and in the appropriate format (DD/MM/YYYY),
- the app must be of type string and the app must also be an existing app name created
  by Apps7,
- the platform must be of type string, and the platform must also exist,
- requests must be of numeric type,
- impressions must be of numeric type and impressions must be less than or equal
  to requests,
- revenue must be of numeric type, and if it contains a unit, we must convert it
  to USD and leave it out.

We must also pay attention that all the columns in the CSV file are named
correctly. If the file contains an additional summary line, we must omit it.

In the data analysis, we also implemented functionality that, if
the number of impressions is greater than the number of requests for all cases
in a given report, determines exactly in which applications and on which
platforms the error occurs.

We could also try to build a machine learning model from the data, which would
be able to correctly predict the number of requests or impressions for a given
day, application, platform, and revenue. The model could be used if the number
of requests or impressions in the data was not correct.

It would also make sense to build a simple model that could be used to predict
the number of impressions based on the number of requests.

From the data, we could probably learn quite a few things, which we could then
use to correct the files, if only they were wrong, and we wouldn't be able to
get a new or correct report.

# Getting started

## Prerequisites

To host the Apps7 application on your machine you will need **Docker** and
**Docker-Compose** installed. You can find documentation on how to install
Docker here: [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)
and docker-compose here: [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/).

> **_NOTE:_** You can also use the application without Docker. You will need to
> download the PostgreSQL database and follow the instructions [below](#local-installation).
> Documentation on how to install PostgreSQL is available here: [https://www.postgresql.org/download/](https://www.postgresql.org/download/)

## Installation

The folder structure in this project is like the following:

```
.
├── app
│   ├── analyze.py
│   ├── daily_report.py
│   ├── main.py
│   ├── seed.py
│   └── server.py
│   └── test.py
├── docs
|   └── answers.md
|   └── instructions.md
├── .env
├── docker-compose.yml
├── Dockerfile
├── README.md
├── requirements.conda.txt
└── requirements.pip.txt
```

First, we clone the repo to download and extract the compressed archive.

```bash
git clone git@github.com:mokot/outfit7-expertise-test.git
cd outfit7-expertise-test
```

<span id="env"></span>
Next, create a `.env` file and set the environment variables.

```bash
# SERVER
SERVER=127.0.0.1
SERVER_PORT=8080

# DATABASE
DATABASE_USER=apps7
DATABASE_PASSWORD=apps7
DATABASE_DB=apps7
DATABASE_HOST=127.0.0.1
DATABASE_PORT=5432

# EXCHANGE RATE API
APILAYER_API_KEY=
```

You can create your `APILAYER_API_KEY` here: [https://apilayer.com/](https://apilayer.com/).
If you don't want to create your account and API key, you can use ours:
**LNDnJpNdlXUUu6lXc3rVUFtWNOnRKbhP**, just be sure not to exceed the
250 requests per month limit.

You can read the example `.env` file from the code above or from the
[.example.env](./.example.env) file.

After that, we are ready to build the image.

```bash
sudo docker build --tag apps7 .
```

<span id="database"></span>
Next, we want to pull the database image and run it.

```bash
sudo docker-compose up [-d]
```

We can access the database with the following command:

```bash
psql "postgresql://DATABASE_USER:DATABASE_PASSWORD@DATABASE_HOST:DATABASE_PORT/DATABASE_DB"
```

If your environment variables are the same as the above, you can use:

```bash
psql "postgresql://apps7:apps7@127.0.0.1:5432/apps7"
```

We also want to fill the database with initial Ad Networks and currencies. That
means we need to run seeds:

```bash
sudo docker run -it --network=host apps7 python3 ./app/seed.py
```

## How to use application?

The application can be used in more than two different ways, namely, it can be
used as a console application or a web application.

### 1. Command Line Interface (CLI)

Using the command line interface is very simple. First, let's start the
application with the following command:

```bash
sudo docker run -it --network=host apps7 python3 ./app/main.py
```

The application started when the command was started and it expects us to enter
the ad network and the date for which we want to obtain and optionally save the
daily report. The application also asks us to confirm the entered data or,
if we wish, to change it.

The application can be closed by pressing `Ctrl + C` or `Ctrl + D` or just
typing the letter `q` or the word `quit`.

### 2. Web Application

The application can also be used as a web application in a browser. First, let's
run the following command:

```bash
sudo docker run -it --network=host apps7 python3 ./app/server.py
```

The above command starts a local web server, which gives us access to a page
where we can enter Ad Networks and dates and see if the program was executed
successfully.

After we have started the server, the page is accessible at the address of the
following form: `http://SERVER:SERVER_PORT`. If your environment variables are
the same as the above, you can use `http://127.0.0.1:8080`.

The web application can also be used as API. You must add the suffix `/api` to the
address written above (`http://SERVER:SERVER_PORT/api`) and send a request to
this address that has the JSON format written below in its body.

```
{
    "ad_network": "AD_NETWORK",
    "date": "DATE"
}
```

If the call was successful, the API returns the saved daily log, but if there is
any error, the API returns the error written in JSON format.

If you use [Postman](https://www.postman.com/), you can import the environment with the
[Apps7 Postman Collection](./apps7.postman_collection.json) file.

You can also make the call using the [curl](https://curl.se/) tool. An example
of a command to retrieve, process, and store a daily report is written below.

```bash
curl --location --request POST 'http://SERVER:SERVER_PORT/api' \
--header 'Content-Type: application/json' \
--data-raw '{
    "ad_network": "AD_NETWORK",
    "date": "DATE"
}'
```

The application can be closed by pressing `Ctrl + C`.

### 3. Script Application

The application can also be used as a simple script that is executed only when
we want it to. The script can be run in the following way:

```bash
sudo docker run -it --network=host apps7 python3 ./app/daily_report.py AD_NETWORK DATE [SAVE]
```

In the above command, `AD_NETWORK` represents the name of the Ad Network for
which we want to obtain and save the daily report, `DATE` is the date of the
report, and `SAVE` is an optional variable that tells us if we want to save the
daily report or just print it out.

For example, a command to save the SuperNetwork daily report for
September 15, 2017, would look like this:

```bash
sudo docker run -it --network=host apps7 python3 ./app/daily_report.py SuperNetwork 2017-09-15 TRUE
```

## Testing

If you want to test the application with a written unit test, you can do that as
follows:

```bash
sudo docker run -it --network=host apps7 python3 ./app/test.py
```

## Analysis

The application also contains a script that checks whether the resulting report
makes sense. The script does a _"sanity check"_ on the daily report. The
techniques used in the analysis are described above.

The report analysis is currently only partially in use, but if you would like to use it
meaningfully, everything is ready for it.

The analysis can be used with the following command on the data of SuperNetwork
and AdUmbrella for the dates September 15 and 16, 2017.

```bash
sudo docker run -it --network=host apps7 python3 ./app/analyze.py
```

## Cleanup

To stop Docker Compose press `Ctrl + C` if you run it in the console or run the 
following command:

```bash
sudo docker-compose stop
```

If you want to remove all containers, networks, volumes, and images created by
the `docker-compose up` command run the following command:

```bash
sudo docker-compose down
```

The command above also completely deletes the database, so be cautious!

To remove created image run:

```bash
sudo docker image rm apps7 [-f]
```

## Local Installation

It is also possible to run the application locally. If you don't want to use
Docker, check the link above about installing PostgreSQL locally.

Firstly, if you are installing an application locally, you should install it in a [virtual environment](https://docs.python.org/3/library/venv.html). If you're unfamiliar with Python virtual environments check out the
[user guide](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/).

Secondly, create a virtual environment with the version of Python you're going to
use and activate it.

> **_NOTE:_** This application is tested on Python 3.10.

Then you will need to install all required libraries, using pip as follows:

```bash
pip3 install -r requirements.pip.txt
```

If you are using [conda](https://docs.conda.io), install requirements as follows:

```bash
conda install --file requirements.conda.txt
```

Next, we have to create a **.env** file and set the environment variables. You
can find a more detailed explanation [here](#env).

If we want to run the database inside a container, we first need to pull an image
and run it. A more detailed explanation for installing the database and
accessing it is available [here](#database).

> **_NOTE:_** If you are using a database inside a Docker container, don't forget
> to stop Docker Compose, and remove all containers, networks, volumes and images
> by running the commands [above](#cleanup).

To run the database locally, check the PostgreSQL wiki here: [https://wiki.postgresql.org/wiki/Main_Page]()
and follow the instructions about how to install and set up database locally.

Now that we have everything ready to launch the application, we can start using
the application.

All of the above commands for running the application, testing it, and analyzing
it can be used by just omitting the `sudo docker run -it --network=host apps7`.

Above commands are written below which will work locally without using the Docker
image. A more detailed description of the commands can be found above.

```bash
python3 ./app/seed.py   # run seeds

# 1. Command Line Interface (CLI)
python3 ./app/main.py

# 2. Web Application
python3 ./app/server.py

# 3. Script Application
python3 ./app/daily_report.py AD_NETWORK DATE [SAVE]

python3 ./app/test.py   # run tests
python3 ./app/analyze.py   # run analysis
```

# Contributing

Contributions are what makes the open source community such an amazing place to
learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature`)
4. Push to the Brach (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

# License

Distributed under the **CLOSED** License. See `LICENSE` for more information.

```
Copyright (C) 2022 Rok Mokotar <mokotar.rok@gmail.com>

This file is part of expertise test for data engineer position at Outfit7.

Apps7 project can not be copied and/or distributed without the express
permission of Outfit7.
```

# Authors

- [Rok Mokotar](https://www.linkedin.com/in/mokot/) - mokotar.rok@gmail.com

# Gallery

The image below shows the appearance of the command line interface version of the application.

<p align="center">
  <img src="./docs/images/cli_example.png" alt="Command Line Interface Example" style="border-radius: 15px" />
</p>

The image below shows the appearance of the web version of the application.

<p align="center">
  <img src="./docs/images/server_example.png" alt="Web Application Example" style="border-radius: 15px" />
</p>
